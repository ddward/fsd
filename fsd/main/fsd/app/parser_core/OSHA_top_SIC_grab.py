from bs4 import BeautifulSoup
import requests
import sys
import sqlite3
from helpers import RepresentsNum

DATABASE = 'test_4.db'
TABLE_NAME = 'top_lvl_sics'
OSHA_LINK = 'https://www.osha.gov/pls/imis/sic_manual.html'

conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS ' + TABLE_NAME + ' (SIC TEXT, SIC_description TEXT)')
conn.commit()

with (requests.get(OSHA_LINK)) as doc_resp:
	doc_str = doc_resp.text
	
soup = BeautifulSoup(doc_str, 'lxml')
a = soup.find(id='maincontain')
b = a.find_all('a')

for c in b:
	group_string = c.text
	group_num = group_string[12:14]
	if(not(RepresentsNum(group_num))):
		continue
	group_title = group_string[16:]
	row = [group_num,group_title]
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('INSERT INTO ' + TABLE_NAME + ' VALUES (?,?)', row)
	conn.commit()
	
conn.close()