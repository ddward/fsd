import sqlite3
from parser_core.cikgrab import tickertocompany
import os
import parser_core.daily_annual_build

dirname = os.path.dirname(os.path.abspath(__file__))

DATABASE = "test_4.db"

script_files = []
script_files.append(
    os.path.join(dirname, "new_ticker_update_sql/schema_annual_build_daily.sql")
)
script_files.append(os.path.join(dirname, "new_ticker_update_sql/pivot_script.sql"))
script_files.append(
    os.path.join(
        dirname, "new_ticker_update_sql/schema_annual_build_post_pivot_daily.sql"
    )
)
script_files.append(
    os.path.join(dirname, "new_ticker_update_sql/schema_annual_daily_append.sql")
)

INPUT_FILE = "annual_formatted"
OUTPUT_FILE = "/var/www/flaskr/flaskr/annual.csv"


def update(DATABASE, INPUT_FILE, OUTPUT_FILE):

    script_files = []
    script_files.append(
        os.path.join(dirname, "new_ticker_update_sql/schema_annual_build_daily.sql")
    )
    script_files.append(os.path.join(dirname, "new_ticker_update_sql/pivot_script.sql"))
    script_files.append(
        os.path.join(
            dirname, "new_ticker_update_sql/schema_annual_build_post_pivot_daily.sql"
        )
    )
    script_files.append(
        os.path.join(dirname, "new_ticker_update_sql/schema_annual_daily_append.sql")
    )

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # TODO check for new tickers -> update coinfo
    tickertocompany(DATABASE)

    # TODO build extended coinfo

    script_file = os.path.join(dirname, "coinfo_expand.sql")

    with open(str(script_file), "r") as f:
        conn = sqlite3.connect(DATABASE)
        conn.execute("pragma journal_mode=WAL")
        c = conn.cursor()
        c.executescript(f.read())
        conn.commit()
    # TODO tickers from coinfo not in current table
    try:
        c.execute("""DROP TABLE IF EXISTS new_tickers;""")
        c.execute(
            """CREATE TABLE IF NOT EXISTS new_tickers AS 
			     SELECT DISTINCT
			     cik
			     FROM coinfo
			     WHERE ticker NOT IN
			     (SELECT DISTINCT 
			      cik
			      FROM annual_post);"""
        )
        conn.commit()

    except sqlite3.OperationalError as e:
        print(e)
        return 1

    # TODO select from main where tickers meet above criteria
    c.execute("""DROP TABLE IF EXISTS main_ticker_update""")
    c.execute(
        """CREATE TABLE main_ticker_update AS
		     SELECT * FROM main WHERE cik IN 
		     (SELECT DISTINCT cik FROM new_tickers);"""
    )
    conn.commit()

    # TODO run daily_update script on this main table
    daily_annual_build.main(DATABASE, INPUT_FILE, OUTPUT_FILE, script_files)


if __name__ == "__main__":
    update(DATABASE, INPUT_FILE, OUTPUT_FILE)
