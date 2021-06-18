import requests
import re
from parser_core.helpers import dateFormat, quarterCheck
import cchardet
from time import sleep

# given a year and quarter returns a table of company information as follows:
# tabular_data[*][0]: Company Name
# tabular_data[*][1]: Report Type - filtered to only include reports that START WTIH 10-K or 10-Q
# tabular_data[*][2]: CIK with no leading zeros
# tabular_data[*][3]: Year in yyyymmdd int format
# tabular_data[*][4]: URL of report files (can pull EX-101.INS from here)
# all data except date is returned in string format

# reference url shortcut: https://www.sec.gov/Archives/edgar/full-index/
headers = {
    "User-Agent": "Friendly XBRL Scraper. Contact: FinancialStatementData@Protonmail.com",
}

def idxStoreHistoric(year, quarter):
    sleep(1)
    tabular_data = []
    url = "https://www.sec.gov/Archives/edgar/full-index/{}/QTR{}/crawler.idx"
    with requests.get(url.format(year, quarter), headers=headers, stream=True) as r:
        for line in r.iter_lines():
            c = cchardet.detect(line)
            decoded_line = line.decode(c["encoding"])
            row = re.split(r"\s{2,}", decoded_line)
            if len(row) > 1 and (
                row[1].startswith("10-K")
                or row[1].startswith("10-Q")
                or row[1].startswith("20-F")
                or row[1].startswith("40-F")
            ):
                row[3] = dateFormat(row[3])
                tabular_data.append(row)
    print("loaded index table for " + str(year) + ", Q" + str(quarter))
    return tabular_data


def idxStoreDaily(yyyy, mm, dd):
    sleep(1)
    tabular_data = []
    quarter = quarterCheck(mm)
    url = "https://www.sec.gov/Archives/edgar/daily-index/{}/QTR{}/crawler.{}.idx"
    fullDate = yyyy + mm + dd
    print(url.format(yyyy, quarter, fullDate))
    with requests.get(url.format(yyyy, quarter, fullDate), headers=headers, stream=True) as r:
        for line in r.iter_lines():
            print(line)
            if not line:
                continue
            c = cchardet.detect(line)
            decoded_line = line.decode(c["encoding"])
            row = re.split(r"\s{2,}", decoded_line)
            if len(row) > 1 and (
                row[1].startswith("10-K")
                or row[1].startswith("10-Q")
                or row[1].startswith("20-F")
                or row[1].startswith("40-F")
            ):
                row[3] = dateFormat(row[3])
                tabular_data.append(row)
    return tabular_data
