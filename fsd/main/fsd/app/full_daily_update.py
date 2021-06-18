from parser_core import (
    tickers_currently_listed_by_exchange,
    cikgrab,
    annual_daily_update_complete,
)
from api_update.update import update
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SOURCE_DB = str(BASE_DIR / "fsd.db")
SOURCE_TABLE = "annual_full_formatted"
TARGET_DB = str(BASE_DIR / "../../../api/api/db.sqlite3")
TARGET_TABLE = "annual_full_formatted_distinct"
TARGET_FIELDS = [
    "Data_Link",
    "ticker",
    "name",
    "end_date",
    "earningspersharediluted",
    "earningspersharebasic",
    "earningspersharebasicanddiluted",
    "cashandcashequivalentsatcarryingvalue",
    "cash",
    "cashandduefrombanks",
    "netincomeloss",
    "profitloss",
    "operatingincomeloss",
    "assetscurrent",
    "assets",
    "liabilities",
    "stockholdersequity",
    "stockholdersequityincludingportionattributabletononcontrollinginterest",
    "liabilitiesandstockholdersequity",
    "accountspayablecurrent",
    "accountsreceivablenetcurrent",
    "inventorynet",
    "researchanddevelopmentexpense",
]


def full_update(back_db):
    # Get tickers currently on NASDAQ and NYSE exchanges
    tickers_currently_listed_by_exchange.main(back_db)

    # Get CIK and company info
    cikgrab.tickertocompany(back_db)

    # Collect raw data and clean into presentation table
    annual_daily_update_complete.simpleUpdate(back_db)

    # Move updated presentation table to API
    update(back_db, SOURCE_TABLE, TARGET_DB, TARGET_TABLE, TARGET_FIELDS)
    print("Backend update completed.")


if __name__ == "__main__":
    full_update(SOURCE_DB)