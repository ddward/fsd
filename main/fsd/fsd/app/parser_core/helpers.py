## List of small helper functions for use in parser.py

from datetime import datetime, timedelta

def RepresentsNum(s):
	if len(s) < 50:
		mod1 = s.replace('.','',1)
		return mod1.replace('-','',1).isdigit()
	else:
		return False
		
#converts a date string in the yyyy-mm-dd format to a date int in the format yyyymmdd
def dateFormat(date_string):
	return int(date_string.replace('-',''))
	
#accepts a day in yyyymmdd format and returns a dictionary for that day broken out into year, month, and day
def day_format(yyyymmdd):
	yyyy = yyyymmdd[:4]
	mm = yyyymmdd[4:6]
	dd = yyyymmdd[-2:]
	
	day = {'year' : yyyy,
	       'month': mm,
		   'day'  : dd}
	
	return day
	
	
# takes two dates in yyyymmdd format and returns a list of dates in range (oldest_date, newest date] in yyyymmdd format excluding saturdays and sundays
def day_diff(ymd_old, ymd_new):
	if(ymd_old == ymd_new):
		return []

	date_ary = []
		
	datetime_obj_old = datetime.strptime(ymd_old, '%Y%m%d')
	datetime_obj_new = datetime.strptime(ymd_new, '%Y%m%d')
	
	diff = (datetime_obj_new - datetime_obj_old).days
	
	for i in range(1, diff + 1):
		day = datetime_obj_old + timedelta(i)
		if(day.weekday() not in [5,6]):
			date_ary.append(day.strftime('%Y%m%d'))
	
	return(date_ary)
	
def quarterCheck(month):
	mm = int(month)
	if(0 < mm <= 3):
		return '1'
	elif(3 < mm <=6):
		return '2'
	elif(6 < mm <=9):
		return '3'
	elif(9 < mm <=12):
		return '4'
	else:
		print("Month out of range error") 
		return -1