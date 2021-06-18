import sqlite3
from api_update import update
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SOURCE_DB = str(BASE_DIR / "fsd.db")
TARGET_DB = str(BASE_DIR / "../../../api/api/db.sqlite3")


conn = sqlite3.connect(SOURCE_DB)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS distinct_coinfo_in_db;")
c.execute(
    "CREATE TABLE distinct_coinfo_in_db AS SELECT DISTINCT ticker, name, industry, sub_industry FROM annual_full_formatted ORDER BY ticker, name, industry, sub_industry"
)

SOURCE_TABLE = "distinct_coinfo_in_db"
TARGET_TABLE = "distinct_coinfo_in_db"

update(SOURCE_DB, SOURCE_TABLE, TARGET_DB, TARGET_TABLE)
print("Backend pushed to frontend.")