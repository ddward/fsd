import sqlite3
import sys

def main(DATABASE,script_file):
	with open(str(script_file),"r") as f:
		conn = sqlite3.connect(str(DATABASE))
		conn.execute('pragma journal_mode=WAL')
		c = conn.cursor()
		c.executescript(f.read())

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2])
