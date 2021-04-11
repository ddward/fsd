import sqlite3
import os

def append(DATABASE):
	
	dirname = os.path.dirname(__file__)
	
	script_files = []
	script_files.append(os.path.join(dirname,'annual_manual_update_sql/schema_annual_build_manual.sql'))
	script_files.append(os.path.join(dirname,'annual_manual_update_sql/pivot_script.sql'))
	script_files.append(os.path.join(dirname,'annual_manual_update_sql/schema_annual_build_post_pivot_manual.sql'))
	script_files.append(os.path.join(dirname,'annual_manual_update_sql/schema_annual_manual_append.sql'))

	for script_file in script_files:
		with open(str(script_file),"r") as f:
			conn = sqlite3.connect(DATABASE)
			conn.execute('pragma journal_mode=WAL')
			c = conn.cursor()
			c.executescript(f.read())
			conn.commit()
			conn.close()
