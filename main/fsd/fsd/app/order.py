import pandas as pd
import sqlite3

SOURCE_DB = "/home/david/fsd/fsd/fsd/fsd/app/fsd.db"
SOURCE_TABLE = "annual_full_formatted"
TARGET_DB = "/home/david/fsd/api/api/db.sqlite3"
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

conn = sqlite3.connect(SOURCE_DB)
df = pd.read_sql_query("SELECT DISTINCT * from annual_full_formatted")
