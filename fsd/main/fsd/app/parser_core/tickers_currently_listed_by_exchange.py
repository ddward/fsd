import requests
import sqlite3
from bs4 import BeautifulSoup
import datetime
import csv
import pandas as pd
from requests.api import request

# Nasdaq: https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ
# NYSE: https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE

DATABASE = "/home/david/fsd/fsd/fsd/fsd/app/fsd.db"


def main(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS ticker_by_exchange
			 (ticker TEXT, exchange TEXT, Last_Price TEXT, date_confirmed TEXT)"""
    )
    conn.commit()
    current_time = datetime.datetime.now()
    # headers = {
    # 	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
    # }

    url_shell = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&exchange={}&download=true"
    exchange_ary = {"NASDAQ", "NYSE"}

    for exchange in exchange_ary:
        headers = {
            "Host": "api.nasdaq.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": "https://www.nasdaq.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": f"https://www.nasdaq.com/market-activity/stocks/screener?exchange={exchange}&render=download",
            "TE": "Trailers",
        }
        with requests.get(url_shell.format(exchange), headers=headers) as r:
            content = r.content.decode("utf-8")
            request_json = r.json()
            print(f"Updating {exchange} tickers...")
            for row in request_json["data"]["rows"]:
                c.execute(
                    "DELETE FROM ticker_by_exchange where ticker = (?)",
                    [row["symbol"]],
                )
                conn.commit()
                replacement_row = [
                    row["symbol"],
                    exchange,
                    row["lastsale"],
                    current_time,
                ]
                c.execute(
                    "INSERT INTO ticker_by_exchange VALUES (?,?,?,?)",
                    replacement_row,
                )
                conn.commit()
    print("Tickers updated.")


# ['ZNGA', 'Zynga Inc.', '3.93', '3387195529.02', 'n/a', '2011', 'Technology', 'EDP Services', 'https://www.nasdaq.com/symbol/znga', '']

if __name__ == "__main__":
    main(DATABASE)
