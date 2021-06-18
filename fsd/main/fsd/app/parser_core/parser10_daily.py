from bs4 import BeautifulSoup
import requests
import sys
import time
import re
import sqlite3
from parser_core.helpers import day_format, day_diff, quarterCheck
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
from parser_core.engine10 import (
    tagGrab,
    contextBuild,
    tag_load,
    redundancy_check,
    idFromUrl,
    daily_check,
    daily_update,
)
from parser_core.indexreader import idxStoreDaily
from time import strftime
from datetime import datetime
from pytz import timezone


def main(DATABASE, SUBSET_TABLE, PRIMARY_TABLE):

    # Specify the database connection
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Create a Master Table
    c.execute("DROP TABLE IF EXISTS daily_update")
    c.execute(
        """CREATE TABLE IF NOT EXISTS """
        + SUBSET_TABLE
        + """
				 (Ticker TEXT, Company_Name TEXT, CIK TEXT, SIC TEXT, Report_Type TEXT, Report_id TEXT, Data_Link TEXT, Submission_Date INT, Instant_Date TEXT, Start_Date TEXT, End_Date TEXT, Tag TEXT, Value REAL)"""
    )

    today = time.strftime("%Y%m%d")
    last_day = daily_check(DATABASE)

    if last_day == []:
        days = []
    else:
        days = day_diff(last_day, today)

    print(days)

    # Pull Data for each company
    for day in days:
        date = day_format(day)
        rows = idxStoreDaily(date["year"], date["month"], date["day"])

        for row in rows:
            print(row)
            report = tagGrab(row)
            if report == None:
                continue

            cik = report[0]
            tag_list = report[1]
            interactiveDataLink = report[2]
            report_type = report[3]
            submission_date = report[4]
            report_id = report[5]
            ticker = report[6]
            SIC = report[7]
            name = report[8]

            contextReference = contextBuild(cik, date["year"], tag_list)
            contexts = contextReference[0]
            # store each top level tag and value for a company
            tag_load(
                DATABASE,
                SUBSET_TABLE,
                cik,
                date["year"],
                tag_list,
                contexts,
                interactiveDataLink,
                report_type,
                submission_date,
                report_id,
                ticker,
                SIC,
                name,
            )
            tag_load(
                DATABASE,
                PRIMARY_TABLE,
                cik,
                date["year"],
                tag_list,
                contexts,
                interactiveDataLink,
                report_type,
                submission_date,
                report_id,
                ticker,
                SIC,
                name,
            )

    conn.close()
    print("scrape process finished!")


if __name__ == "__main__":
    main(DATABASE, SUBSET_TABLE, PRIMARY_TABLE)
