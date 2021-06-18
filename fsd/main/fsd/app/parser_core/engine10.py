from bs4 import BeautifulSoup
import requests
import sys
import time
import re
import sqlite3
from parser_core.helpers import RepresentsNum, dateFormat
from parser_core.cikgrab import (
    tickertocompany,
    cikgrab,
    tickerload,
    cikdump,
    cikSwitch,
    cikread,
)
from parser_core.pivot import tagflip, taggrab, tagQueryBuild
import psutil
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from time import strftime, sleep


def tagGrab(row):

    name = row[0]
    report_type = row[1]
    cik = row[2]
    submission_date = row[3]
    link = row[4]
    # Obtain HTML for document page
    doc_str = ""

    headers = {
        "User-Agent": "Friendly XBRL Scraper. Contact: FinancialStatementData@Protonmail.com",
    }
    sleep(.1)
    with (requests.get(link, headers=headers)) as doc_resp:
        doc_str = doc_resp.text

    # Find the XBRL link
    xbrl_link = ""
    soup = BeautifulSoup(doc_str, "html.parser")
    try:
        interactiveDataLink = "https://www.sec.gov" + soup.find(
            id="interactiveBtn"
        ).get("href")
    except AttributeError:
        try:
            interactiveDataLink = "https://www.sec.gov" + soup.find(
                id="interactiveDataBtn"
            ).get("href")
        except AttributeError:
            interactiveDataLink = "N/A"

    report_id = reportIdFind(soup)
    SIC = SICFind(soup)

    table_tag = soup.find("table", class_="tableFile", summary="Data Files")
    if table_tag is None:
        print(
            f"No data table found for {name}, report date {submission_date}. Report link: {link}"
        )

        return None

    rows = table_tag.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 3:
            if "INS" in cells[3].text or "EXTRACTED" in cells[1].text.upper():
                xbrl_link = "https://www.sec.gov" + cells[2].a["href"]

    # Obtain XBRL text from document

    if xbrl_link == "":
        print(
            f"No XBRL files found in the data table for {name}, report date {submission_date}. Report link: {link}"
        )
        return None

    xbrl_str = ""
    sleep(.1)
    with requests.get(xbrl_link) as xbrl_resp:
        xbrl_str = xbrl_resp.text.encode("utf-8")
    soup = BeautifulSoup(xbrl_str, "lxml")
    ticker = tickerFind(soup)
    tag_list = soup.find_all()
    # Debug 3.1 - Time to download xbrl soup from SEC website
    report_list = [
        cik,
        tag_list,
        interactiveDataLink,
        report_type,
        submission_date,
        report_id,
        ticker,
        SIC,
        name,
    ]
    # print("Debug 3.1 - Time to load soup for company",cik,"and year",year,"was", (time.time()- start_time),"seconds.")
    return report_list


def contextBuild(cik, year, tag_list):

    contexts = {}
    prefixes = []
    for tag in tag_list:
        if tag.name.endswith("context"):
            # This section of code finds the start date of the context if it exists.
            start_date_tag = tag.find(name=re.compile("startdate"))
            start_date = ""
            if start_date_tag != None:
                try:
                    start_date = int(start_date_tag.text.replace("-", ""))
                except ValueError:
                    start_date = 0

            # This section of code finds the end date of the context if it exists.
            end_date_tag = tag.find(name=re.compile("enddate"))
            end_date = ""
            if end_date_tag != None:
                try:
                    end_date = int(end_date_tag.text.replace("-", ""))
                except ValueError:
                    end_date = 0
                datetype = "period"
            # This section of code finds the instant date of the context if it exists.
            instant_date_tag = tag.find(name=re.compile("instant"))
            instant_date = ""
            if instant_date_tag != None:
                try:
                    instant_date = int(instant_date_tag.text.replace("-", ""))
                except ValueError:
                    instant_date = 0
                datetype = "instant"

            explicitmembertags = tag.find_all(name=re.compile("explicitmember"))
            explicitmember_dimension = {}
            for explicitmembertag in explicitmembertags:
                explicitmember_dimension[
                    explicitmembertag.attrs["dimension"]
                ] = explicitmembertag.text
                tag_breakdown = explicitmembertag.text.split(":")
                tag_prefix = tag_breakdown[0]
                if tag_prefix not in prefixes:
                    prefixes.append(tag_prefix)

            # Build a dictionary of date information within a dictionary of context titles
            contextinfo = {
                "cik": cik,
                "explicitmember_dimension": explicitmember_dimension,
                "datetype": datetype,
                "instantdate": instant_date,
                "start_date": start_date,
                "end_date": end_date,
            }
            contexts[tag.attrs["id"]] = contextinfo
            # print('context table length for cik ' + cik+ 'and year ' + str(year) + ' is '+ str(len(contexts)))

    return [contexts, prefixes]


def tag_load(
    DATABASE,
    table_name,
    cik,
    year,
    tag_list,
    contexts,
    interactiveDataLink,
    report_type,
    submission_date,
    report_id,
    ticker,
    SIC,
    company_name,
):
    conn = sqlite3.connect(DATABASE)
    conn.execute("pragma journal_mode=WAL")
    c = conn.cursor()

    for tag in tag_list:
        # isolate the prefixes and names
        tag_components = tag.name.split(":")
        # adjust to include company specific tags if needed
        if (
            tag_components[0] == "us-gaap"
            # only concerned with tags that report numbers
            and RepresentsNum(tag.text)
            # only want top level entries
            and len(contexts[tag.attrs["contextref"]]["explicitmember_dimension"]) == 0
        ):
            # only want current year values
            # and contexts[tag.attrs['contextref']]['year'] == str(year)):

            # adjust for tag names that are so long that their end is stored in an attribute name. These attributes have a null value.
            name = tag_components[1]
            for a in tag.attrs:
                if tag.attrs[a] == "":
                    name = name + a

            row = [
                ticker,
                company_name,
                cik,
                SIC,
                report_type,
                report_id,
                interactiveDataLink,
                submission_date,
                contexts[tag.attrs["contextref"]]["instantdate"],
                contexts[tag.attrs["contextref"]]["start_date"],
                contexts[tag.attrs["contextref"]]["end_date"],
                name,
                tag.text,
            ]
            c.execute(
                "INSERT INTO " + table_name + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", row
            )
    conn.commit()
    conn.close()


def redundancy_check(DATABASE):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    try:
        id_list = c.execute("select distinct Report_id from main").fetchall()
        return id_list
    except sqlite3.OperationalError:
        return []


def interactiveBtn(id):
    return id and re.compile("interactiveDataBtn").search(id)


def secNum(id):
    return id and re.compile("secNum").search(id)


def reportIdFind(soup):
    a = []

    try:
        b = soup.find(id=secNum).stripped_strings
    except AttributeError:
        return "No report id found"
    for text in b:
        a.append(text)
    report_id = []
    if a:
        report_id = a[-1]
    if RepresentsNum(report_id.replace("-", "")):
        return report_id
    else:
        return "No report id found"


# url = 'https://www.sec.gov/Archives/edgar/data/1706524/000168316818003495/none-20180930.xml'
# r = requests.get(url)
# rString = r.text
# soup = BeautifulSoup(rString)


def SICFind(soup):
    a = soup.find_all("a")
    for row in a:
        if "SIC=" in row.get("href"):
            return int(row.text)
    return 0


def tickerFind(soup):
    dei = soup.find("dei:tradingsymbol")
    if dei == None:
        return "N/A"
    else:
        return dei.text


def idFromUrl(url):
    a = url.split("/")[-1]
    b = a[:-10]
    return b


def daily_check(DATABASE):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    day = c.execute("select max(submission_date) from main").fetchall()
    return str(day[0])


def daily_update(DATABASE):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS daily_update_meta AS
				 id INTEGER PRIMARY KEY AUTOINCREMENT,
				 day TEXT, 
				 datetime_loaded TEXT"""
    )

    day = time.strftime("%Y-%m-%d")
    datetime = time.strftime("%Y-%m-%d %H:%M:%S")

    row = (day, datetime)
    c.execute("INSERT INTO daily_update_meta(day,datetime_loaded) VALUES (?,?)", row)
