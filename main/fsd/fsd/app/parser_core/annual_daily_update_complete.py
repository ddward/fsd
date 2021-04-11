import time
from datetime import datetime
from pytz import timezone

from parser_core import parser10_daily, daily_annual_build, new_ticker_update
import pathlib

from parser_core.engine10 import daily_check
from parser_core.helpers import day_diff

import os

dirname = os.path.dirname(__file__)
pathlib_dirname = pathlib.Path(__file__).absolute()

# ----- Variables for all functions -----#
DATABASE = pathlib_dirname.parent.parent / "fsd.db"
START_TIME = datetime.strptime("10:00PM", "%I:%M%p")
END_TIME = datetime.strptime("12:00AM", "%I:%M%p")
TZ = timezone("EST")

# ----- Variables for parser10_daily -----#
SUBSET_TABLE = "daily_update"
PRIMARY_TABLE = "main"

# ----- Variables for daily_annual_build -----#
INPUT_FILE = "annual_formatted"
OUTPUT_FILE = "/var/www/flaskr/flaskr/annual.csv"

script_files = []
script_files.append(
    os.path.join(dirname, "annual_daily_build_sql/schema_annual_build_daily.sql")
)
script_files.append(os.path.join(dirname, "annual_daily_build_sql/pivot_script.sql"))
script_files.append(
    os.path.join(
        dirname, "annual_daily_build_sql/schema_annual_build_post_pivot_daily.sql"
    )
)
script_files.append(
    os.path.join(dirname, "annual_daily_build_sql/schema_annual_daily_append.sql")
)


# ----- Functions -----#
def main():
    start = START_TIME.replace(tzinfo=timezone("EST"))
    end = END_TIME.replace(tzinfo=timezone("EST"))
    update_needed = False
    last_day = daily_check(DATABASE)

    while True:
        updated = False
        now = datetime.now(TZ)

        if isNowInTimePeriod(start.hour + 2, end.hour + 2, now.hour):
            new_ticker_update.update(DATABASE, INPUT_FILE, OUTPUT_FILE)

        if isNowInTimePeriod(start.hour, end.hour, now.hour):

            now_formatted = now.strftime("%Y%m%d")

            if day_diff(last_day, now_formatted) == []:
                print("made it here")
                update_needed = False
            else:
                update_needed = True

            if update_needed:
                parser10_daily.main(DATABASE, SUBSET_TABLE, PRIMARY_TABLE)
                daily_annual_build.main(DATABASE, INPUT_FILE, OUTPUT_FILE, script_files)
                updated = True
                last_day = daily_check(DATABASE)

        if updated:
            print(
                "Annual dataset update loop completed at "
                + str(now)
                + " EST, data WAS updated, sleeping for 60 seconds..."
            )
        else:
            print(
                "Annual dataset update loop completed at "
                + str(now)
                + " EST, data WAS NOT updated, sleeping for 60 seconds..."
            )

        time.sleep(60)


def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime < endTime
    else:
        return nowTime >= startTime or nowTime < endTime


def simpleUpdate(db):
    SUBSET_TABLE = "daily_update"
    PRIMARY_TABLE = "main"

    # ----- Variables for daily_annual_build -----#
    INPUT_FILE = "annual_formatted"
    OUTPUT_FILE = "/var/www/flaskr/flaskr/annual.csv"

    script_files = []
    script_files.append(
        os.path.join(dirname, "annual_daily_build_sql/schema_annual_build_daily.sql")
    )
    script_files.append(
        os.path.join(dirname, "annual_daily_build_sql/pivot_script.sql")
    )
    script_files.append(
        os.path.join(
            dirname, "annual_daily_build_sql/schema_annual_build_post_pivot_daily.sql"
        )
    )
    script_files.append(
        os.path.join(dirname, "annual_daily_build_sql/schema_annual_daily_append.sql")
    )
    print("Collecting new reports...")
    parser10_daily.main(db, SUBSET_TABLE, PRIMARY_TABLE)
    print("Formatting...")
    daily_annual_build.main(db, INPUT_FILE, OUTPUT_FILE, script_files)


if __name__ == "__main__":
    # main()
    simpleUpdate(DATABASE)
