import sqlite3
import sys

DATABASE = 'test_4.db'

scripts = []
scripts.append('schema_annual_build_daily.sql')
scripts.append('pivot_script.sql')
scripts.append('schema_annual_build_post_pivot_daily.sql')
scripts.append('schema_annual_daily_append.sql')

conn = sqlite3.connect(str(DATABASE))
conn.execute('pragma journal_mode=WAL')
c = conn.cursor()

for script in scripts:
    with open(str(script),"r") as file:
	print('Processing script ' + script)        
	c.executescript(file.read())
        conn.commit()

conn.close()
