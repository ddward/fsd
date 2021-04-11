import sqlite3
from manual_append import append
# test cik; google - 0001652044
# test link: google https://www.sec.gov/cgi-bin/viewer?action=view&cik=1288776&accession_number=0001652044-16-000012&xbrl_type=v


#TODO  CRITICAL CHECK FOR CONFLICTING (FULL) RECORDS AND DO NOT ALLOW OVERWRITES!!!!!!!!!@!!!

DATABASE = 'test_4.db'

def main(DATBASE):

	while(True):
		#Connect to Database
		conn = sqlite3.connect(DATABASE)
		conn.execute('pragma journal_mode=WAL')
		conn.row_factory = sqlite3.Row
		c = conn.cursor()

		#Collect Rows
		print("What record would you like to add?")
		data_link = process_link(DATABASE, c)

		date_validated = False
		while(not date_validated):
			instant_date = process_instant(data_link, conn, c)
			start_date = process_start(data_link, conn, c)
			end_date = process_end(data_link, conn, c)
			date_validated = combo_vali_date(instant_date,start_date,end_date)		

		while(True):
			tag = process_tag(DATABASE, c)
			value = process_value()
			
			print("Generating insertion row(s)...")
			extrapolate = c.execute("SELECT DISTINCT ticker, company_name, cik, sic, report_type, report_id, submission_date FROM main WHERE data_link = ?", (data_link,))
			
			rows = []

			row_fragments = extrapolate.fetchall()
			for fragment in row_fragments:
				row = (fragment['ticker'], fragment['company_name'], fragment['cik'], fragment['sic'], fragment['report_type'], fragment['report_id'], data_link, fragment['submission_date'], instant_date, start_date, end_date, tag, value)
				rows.append(row)
			print("You are about to insert the following row(s) into the main table.")
			print("Ticker, Company_Name, CIK, SIC, Report_Type, Report_Id, Data_Link, Submission_Date, Instant_Date, Start_Date, End_Date, Tag, Value")
			for row in rows:
				print(row)
			
			while(True):	
				final_confirm = input("Is this what you want to do? Enter y for yes or n for no.")	
				
				while final_confirm not in ('y','Y','yes','Yes','n','N','no','No'):
					print("Please enter a valid response.")
					final_confirm = input("Manual insert completed. Would you like to insert another record? Enter y for yes or n for no.")

				if(final_confirm in ('y','Y','yes','Yes')):			
					break
				elif(final_confirm in ('n','N','No','no')):
					print('Please try again.')
					return
				else:
					sys.exit('input error')
			print("Inserting rows...")

			insert(DATABASE, rows, c, conn, data_link)
			
			print("Appending rows to main table...")

			append(DATABASE)
			conn.commit()

			repeat_1 = input("Manual insert completed. Would you like to insert another tag and value for these dates? Enter y for yes or n for no.")
			
			while repeat_1 not in ('y','Y','yes','Yes','n','N','no','No'):
				print("Please enter a valid response.")
				repeat_1 = input("Manual insert completed. Would you like to insert another record? Enter y for yes or n for no.")

			if(repeat_1 in ('y','Y','yes','Yes')):			
				tag = ""
				value = ""
				continue
			elif(repeat_1 in ('n','N','No','no')):
				break
			else:
				sys.exit('input error')	

			

		repeat = input("Would you like to insert another full record? Enter y for yes or n for no.")
		
		while repeat not in ('y','Y','yes','Yes','n','N','no','No'):
			print("Please enter a valid response.")
			repeat = input("Manual insert completed. Would you like to insert another record? Enter y for yes or n for no.")

		if(repeat in ('y','Y','yes','Yes')):			
			continue
		elif(repeat in ('n','N','No','no')):
			break
		else:
			sys.exit('input error')	

		conn.commit()
		conn.close()


def cik_check(DATABASE, c):
	while(True):	
		cik = str(int(input("Enter CIK for the record:")))
		print("Consulting database please wait...")
		db_check_1 = c.execute("SELECT DISTINCT company_name FROM main WHERE cik = ?;", (cik,))
		db_check_1a = db_check_1.fetchone()[0]
		cik_confirm = input("You want to add a record for " + db_check_1a + " correct? Enter y for yes or n for no.")
		while cik_confirm not in ('y','Y','yes','Yes','n','N','no','No'):
			print("Please enter a valid response.")
			cik_confirm = input("You want to add a record for " + db_check_1a + " correct? Enter y for yes or n for no.")
				
		if(cik_confirm in ('y','Y','yes','Yes')):
			return cik
		elif(cik_confirm in ('n','N','No','no')):
			continue
		else:
			sys.exit('input error')
		
def process_link(DATABASE, c):
	while(True):
		data_link = input("Enter the data_link (url) for the record:")
		print("Consulting database please wait...")
		db_check_1 = c.execute("SELECT COUNT(rowid) FROM main WHERE data_link = ?", (data_link,))
		db_check_1a = db_check_1.fetchone()[0]
		if (int(db_check_1a) >= 1):
			print("Link is valid.")			
			return data_link
		else: 
			try_again = input("This link does not exist in the database, do you want to try again? Enter y for yes or n for no.")
			while try_again not in ('y','Y','yes','Yes','n','N','no','No'):
				print("Please enter a valid response.")
				cik_confirm = input("This link does not exist in the database, do you want to try again? Enter y for yes or n for no.")

			if(try_again in ('y','Y','yes','Yes')):
				continue
			elif(try_again in ('n','N','No','no')):
				sys.exit('this routine can only add records for reports that already exist in the database.')
			else:
				sys.exit('input error')
	
def process_instant(data_link, conn, c):
	while(True):
		print('\nPulling valid INSTANT DATES from database...')		
		existing_dates = db_date_options('instant_date', data_link, conn, c)
		instant_date = input("Enter the instant date for the record if applicable or press return:")
		if(vali_date(instant_date, existing_dates) == True):
			return instant_date

def process_start(data_link, conn, c):
	while(True):
		print('\nPulling valid START DATES from database...')	
		existing_dates = db_date_options('start_date', data_link, conn, c)
		start_date = input("Enter the start date for the record if applicable or press return:")
		if(vali_date(start_date, existing_dates) == True):
			return start_date

def process_end(data_link, conn, c):
	while(True):
		print('\nPulling valid END DATES from database...')	
		existing_dates = db_date_options('end_date', data_link, conn, c)
		end_date = input("Enter the end date for the record if applicable or press return:")
		if(vali_date(end_date, existing_dates) == True):
			return end_date
		
def vali_date(date_str, existing_date_ary):
	if(date_str == ""):
		return True	
	elif(len(date_str) != 8):
		print("Not a valid date format - must be YYYYMMDD or an empty string.")
		return False
	try: 
		int(date_str)
	except ValueError:
		print("Not a valid date format - must be YYYYMMDD or an empty string.")
		return False
	if(date_str in existing_date_ary):
		return True
	else:
		print("Not a valid date for this record, please try again.")
		return False	
		
def db_date_options(date_type, data_link, conn, c):
	dates_pull = c.execute('SELECT DISTINCT ' + date_type + ' FROM main WHERE data_link = ? ORDER BY ' + date_type + ' ASC;', (data_link,))
	dates = dates_pull.fetchall()
	valid_date_row = []	
	for date in dates:
		valid_date_row.append(date[date_type])
	print('These are the valid ' + date_type + 's for this record:\n', valid_date_row)
	return valid_date_row	
		
def process_value():
	while(True):
		value = input("\nEnter the value for the record:")
		try:
			float(value)
			return value
		except ValueError:
			print("Tag must be an intiger or a floating point variable.")
			continue


def process_tag(DATABASE, c):
	while(True):
		tag = input("\nEnter the tag (eg. earningspersharebasic) for the record:")
		print("Consulting database please wait...")		
		db_check_1 = c.execute("SELECT COUNT(DISTINCT tag) FROM main WHERE tag = ?",(tag,))
		db_check_1a = db_check_1.fetchone()[0]
		if(int(db_check_1a == 0)):
			print("No other tags in the database match this name, please try again. This script doesn't allow for the creation of new tags.")
			continue
		else:
			print("Tag is valid.")			
			return tag

def combo_vali_date(instant_date, start_date, end_date):
	if(instant_date == "" and start_date != "" and end_date != ""):
		return True
	elif(instant_date != "" and start_date == "" and end_date == ""):
		return True
	else:
		print("Please re-enter dates. A record can have either one instant date or one start and one end date.")		
		return False

def insert(DATABASE, rows, c, conn, data_link):
	c.execute("""CREATE TABLE IF NOT EXISTS manual_additions (
		  id INTEGER PRIMARY KEY AUTOINCREMENT,
		  insertion_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
		  Ticker TEXT,
		  Company_Name TEXT,
	   	  CIK TEXT,
		  SIC TEXT,
		  Report_Type TEXT,
		  Report_id TEXT,
		  Data_Link TEXT,
		  Submission_Date INT,
		  Instant_Date TEXT,
		  Start_Date TEXT,
		  End_Date TEXT,
		  Tag TEXT,
		  Value TEXT
			)"""
		  )
	conn.commit()
	
	for row in rows:	
		c.execute("""INSERT INTO manual_additions (
			  ticker,
			  company_name,
			  cik,
			  sic,
			  report_type,
			  report_id,
			  data_link,
			  submission_date,
			  instant_date,
			  start_date,
			  end_date,
			  tag,
			  value )
			  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", row)


	for row in rows:	
		c.execute("""INSERT INTO main (
			  ticker,
			  company_name,
			  cik,
			  sic,
			  report_type,
			  report_id,
			  data_link,
			  submission_date,
			  instant_date,
			  start_date,
			  end_date,
			  tag,
			  value )
			  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", row)
	conn.commit()

	c.execute('DROP TABLE IF EXISTS manual_append_1')
	c.execute('CREATE TABLE manual_append_1 AS SELECT * FROM main WHERE data_link = ?',(data_link,))

	conn.commit()


#TODO insertion process
#generate insertion row
#add insertion record and timestamp to mannual insertion table (insertion row plus timestamp

#values
#CIK: manual
#Data_Link: manual
#Tickers(CIK)
#Company_Name(CIK)
#SIC(CIK)
#Report_type(Data_Link)
#Report_ID(pull from insertion table)
#Submission_Date(data_link)
#Instant_Date: Manual default "" (error checking make sure instant or (start and end) have a value not '--'
#Start_Date: Manual default "" (error checking make sure instant or (start and end) have a value not '--'
#End_DateManual default "" (error checking make sure instant or (start and end) have a value not '--'
#Tag: manual
#Value: manual (include type checking and decimal checking)

#TODO run daily annual append on ONLY NEW insertions (need a master insertion table 
#and a temp insertion table)

#Main Structure:
#Ticker
#Company_Name
#CIK
#SIC
#Report_Type
#Report_id
#Data_Link
#Submission_Date
#Instant_Date
#Start_Date
#End_Date
#Tag
#Value

#connection code
#conn = sqlite3.connect(DATABASE)
#conn.execute('pragma journal_mode=WAL')
#c = conn.cursor()

if __name__== '__main__':
	main(DATABASE)
