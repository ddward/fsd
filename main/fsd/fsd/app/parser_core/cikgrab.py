from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import random
from datetime import datetime
import os
from random import randint
from time import sleep
import sys

dirname = os.path.dirname(__file__)

# TODO: need a segment to handle companies that have changed their CIK i.e. GOOG (could search by ticker symbol to begin with??)


def tickerload(ticker_file):
    tickerlist = []
    with open(ticker_file, "r") as tf:
        content = tf.readlines()
        tickerlist = [x.strip("\n") for x in content]
    return tickerlist


def tickertocompany(DATABASE):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
        "Host": "www.sec.gov",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.sec.gov/edgar/searchedgar/companysearch.html",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    conn = sqlite3.connect(str(str(DATABASE)))
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()

    c.execute(
        """create table if not exists coinfo
			 (ticker TEXT, cik TEXT, name TEXT, sic TEXT, sic_desc TEXT)"""
    )

    with open(str(os.path.join(dirname, "coinfo_build_helper.sql")), "r") as file:
        c.executescript(file.read())
        conn.commit()

    tickers = []
    try:
        tickers = c.execute(
            "select distinct ticker from omitted_tickers WHERE cik_pull_date IS NULL"
        ).fetchall()

    except sqlite3.OperationalError:
        pass

    print(f"New tickers: {tickers}")
    average_time_ary = []
    total_tickers = len(tickers)
    tickers_processed = 0

    random.seed(datetime.now())
    random.shuffle(tickers)
    for ticker in tickers:
        print("processing... " + ticker)
        start_time = time.time()

        sleep(randint(8, 21))

        c.execute(
            """UPDATE omitted_tickers 
				SET cik_pull_date = CURRENT_TIMESTAMP
				WHERE ticker = ? """,
            (ticker,),
        )
        conn.commit()
        url = (
            "https://www.sec.gov/cgi-bin/browse-edgar?CIK="
            + ticker
            + "&owner=exclude&action=getcompany&Find=Search"
        )

        with requests.get(url, headers=headers) as html:
            html_txt = html.text

        soup = BeautifulSoup(html_txt, "lxml")
        coinfo = soup.find(class_="companyName")

        try:
            name = coinfo.contents[0]
            cik = coinfo.contents[3].contents[0][0:10]
            coinfo2 = soup.find(class_="identInfo")

            try:
                sic = coinfo2.contents[2].contents[0]
            except IndexError:
                sic = "IndexError"
            try:
                sic_desc = coinfo2.contents[3][3:]
            except TypeError:
                sic_desc = "TypeError"  # TODO - better exception handling
            except IndexError:
                sic_desc = "IndexError"  # TODO - better exception handling

            row = [ticker, cik, name, sic, sic_desc]
            c.execute("INSERT INTO coinfo VALUES (?,?,?,?,?)", row)
            c.execute(
                """UPDATE omitted_tickers
				     SET cik_pull_success = 'yes',
				         cik = ?
				     WHERE ticker = ?""",
                (cik, ticker),
            )
            conn.commit()

        except AttributeError:
            tickers_processed = tickers_processed + 1
            continue  # TODO: put these in an error list to test

        tickers_processed = tickers_processed + 1
        end_time = time.time()
        average_time_ary.append(time.time() - start_time)
        avg_time = sum(average_time_ary) / len(average_time_ary)
        percent_completed = round((tickers_processed / total_tickers) * 100)
        seconds_left = round((avg_time * (total_tickers - tickers_processed)))

        print(
            "Company Information is %"
            + str(percent_completed)
            + " loaded. "
            + str(seconds_left)
            + " seconds remaining."
        )
    conn.close()
    # with open (output_file, 'w+') as file:
    # 	for row in infolist:
    # 		for field in row:
    # 			file.write("%s," % field)
    # 		file.write("\n")

    # return infolist


def cikgrab(infolist):
    ciklist = []
    for co in infolist:
        ciklist.append(co[1])
    return ciklist


def cikread(cik_txt):
    ciklist = []
    with open(cik_txt, "r") as file:
        ciklist = file.read().splitlines()
    return ciklist


def cikdump(infolist, database_file):
    conn = sqlite3.connect(str(database_file))
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS tickerandsic""")
    c.execute(
        """CREATE TABLE tickerandsic 
			(Ticker Text, CIK TEXT, Name TEXT, SIC INT, SIC_Definition TEXT)"""
    )
    for row in infolist:
        c.execute("INSERT INTO tickerandsic VALUES (?,?,?,?,?)", row)
    conn.commit()
    conn.close()


def cikSwitch(soup, current_cik):
    cik = None
    info_list = soup.find_all(class_="companyName")
    if info_list == False or len(info_list) == 1:
        return None
    else:
        alternate_ciks = []
        for a in info_list:
            cik = a.contents[3].contents[0][0:10]
            alternate_ciks.append(cik)
            return alternate_ciks


if __name__ == "__main__":
    tickertocompany(sys.argv[1])
