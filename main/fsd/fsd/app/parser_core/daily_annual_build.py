import sqlite3
import sys
from parser_core.pivot import taggrab, tagQueryBuild, tagflip
import pandas

# ----- Shouldn't have to touch this below ------#
def main(DATABASE, INPUT_FILE, OUTPUT_FILE, script_files, output_csv=False):
    for script_file in script_files:
        db_execute(DATABASE, script_file)
    if output_csv:
        pickup(DATABASE, INPUT_FILE, OUTPUT_FILE)


def db_execute(DATABASE, script_file):
    with open(str(script_file), "r") as f:
        conn = sqlite3.connect(DATABASE)
        conn.execute("pragma journal_mode=WAL")
        c = conn.cursor()
        c.executescript(f.read())
        conn.commit()
        conn.close()


def pickup(DATABASE, INPUT_FILE, OUTPUT_FILE):
    conn = sqlite3.connect(DATABASE)
    table = pandas.read_sql("select * from " + INPUT_FILE, conn)
    table.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main(DATABASE, INPUT_FILE, OUTPUT_FILE, script_files)
