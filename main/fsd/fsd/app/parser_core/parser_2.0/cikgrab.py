import requests
import sqlite3
import sys

TICKER_CIK_MAP_ADDRESS = "https://www.sec.gov/include/ticker.txt"


def cikgrab():
    with requests.get(TICKER_CIK_MAP_ADDRESS) as response:
        response_str = response.content.decode("utf-8")

    row_list = []
    for row in response_str.splitlines():
        row_list.append(row.split("\t"))

    # ticker to cik mapping eg.
    # {'znogw': '1131312', 'zsl': '1415311', ...}
    return dict(row_list)


def cikload(DATABASE, ticker_cik_dict):
    conn = sqlite3.connect(str(str(DATABASE)))
    c = conn.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS ticker_to_cik
    (ticker TEXT, cik TEXT)"""
    )


if __name__ == "__main__":
    cikgrab()
    # cikload(sys.argv[1])
