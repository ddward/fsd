import sys
import sqlite3


def check(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT MAX(submission_date) FROM annual_full_formatted;")
    result = c.fetchone()
    print(result)


if __name__ == "__main__":
    check(sys.argv[1])
