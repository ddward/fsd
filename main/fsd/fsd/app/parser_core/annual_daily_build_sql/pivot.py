import sqlite3

#this function puts all tags from a table into a list
def taggrab(database_file,table):
	conn = sqlite3.connect(str(database_file))
	c = conn.cursor()
	tag_table_unformatted = c.execute("SELECT distinct tag from " + table).fetchall()
	tag_table = []
	for tag in tag_table_unformatted:
		#need to keep ' out of the text or it messes up the SQL query. Not needed when using tag instead of label.
		tag_table.append(tag[0].replace("'",""))
	conn.close()
	return tag_table

def tagCustom(tag_table):
	filtered_table = []
	for tag in tag_table:
		if tag in CUSTOM_TABLE:
			filtered_table.append(tag)
	return filtered_table
	
#this function puts all tags in a list into a single string variable with SQL case formatting
def tagQueryBuild(tag_list):	
	case_shell = "SUM(CASE WHEN tag = '{}' THEN amount end) as '{}'"
	case_string = ""
	tags_processed = 0
	number_of_tags = len(tag_list)
	for tag in tag_list:
		if(tags_processed < number_of_tags - 1):
			case_string = case_string + case_shell.format(tag,tag) + ','
		else:
			case_string = case_string + case_shell.format(tag,tag)
		tags_processed = tags_processed + 1
	return case_string

#this function creates a new table that is pivoted
def tagflip(database_file,case_string,new_table_name,from_table_name):
	query_string = ("CREATE TABLE " + new_table_name + " AS select Ticker, Name, CIK, CIK2, Report_Type, Data_Link, Submission_date, Instant_date, end_date, date_diff, " + case_string + " from " + from_table_name + " where date_diff > 300 GROUP BY Ticker, Name, CIK, CIK2, Report_Type, Data_Link, Submission_date, Instant_date, end_date, date_diff order by Ticker asc, CIK2 asc, submission_date desc;")
	print(query_string)
	conn = sqlite3.connect(str(database_file))
	c = conn.cursor()
	c.execute("DROP TABLE IF EXISTS " + new_table_name)
	c.execute(query_string)
	conn.commit()
	conn.close()