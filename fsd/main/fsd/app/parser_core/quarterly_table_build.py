import os
import pathlib
import daily_annual_build

dirname = os.path.dirname(__file__)
pathlib_dirname = pathlib.Path(__file__).absolute()

DATABASE = pathlib_dirname.parent.parent / "fsd.db"
INPUT_FILE = "quarterly_formatted"
OUTPUT_FILE = "/var/www/flaskr/flaskr/annual.csv"

script_files = []

script_files.append(
    os.path.join(
        dirname, "quarterly_daily_build_sql/schema_quarterly_build_offshoot.sql"
    )
)
script_files.append(
    os.path.join(dirname, "quarterly_daily_build_sql/quarterly_pivot_script.sql")
)
script_files.append(
    os.path.join(
        dirname, "quarterly_daily_build_sql/schema_quarterly_build_post_pivot_daily.sql"
    )
)
script_files.append(
    os.path.join(dirname, "quarterly_daily_build_sql/schema_quarterly_daily_append.sql")
)

if __name__ == "__main__":
    daily_annual_build.main(DATABASE, INPUT_FILE, OUTPUT_FILE, script_files)