import sqlite3
import sys
import os


DATABASE = "/home/david/fsd/fsd/fsd/fsd/app/fsd.db"

dirname = os.path.dirname(__file__)

scripts = []
scripts.append(
    os.path.join(dirname, "annual_full_build_sql/schema_annual_build_full.sql")
)
scripts.append(os.path.join(dirname, "annual_full_build_sql/pivot_script.sql"))
scripts.append(
    os.path.join(dirname, "annual_full_build_sql/schema_annual_build_post_pivot.sql")
)

conn = sqlite3.connect(str(DATABASE))
conn.execute("pragma journal_mode=WAL")
c = conn.cursor()

for script in scripts:
    with open(str(script), "r") as file:
        c.executescript(file.read())
        conn.commit()

conn.close()
