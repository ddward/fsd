
/* 
main schema:
ticker,
company_name,
cik,
sic,
report_type,
data_link,
submission_date,
instant_date,
start_date,
end_date,
tag,
value

coinfo schema:
ticker,
cik,
name,
sic,
sic_desc
*/

DROP TABLE IF EXISTS date_table_1;
DROP TABLE IF EXISTS alternate_ciks_adj;
DROP TABLE IF EXISTS dup_cik_adj_1;
DROP TABLE IF EXISTS dup_cik_adj_2;
DROP TABLE IF EXISTS date_table_2;
DROP TABLE IF EXISTS main_date_formatted;
DROP TABLE IF EXISTS ticker_appended_main;
DROP TABLE IF EXISTS tag_count;

CREATE TABLE IF NOT EXISTS date_table_1 AS
SELECT
Ticker,
Company_Name,
CIK,
Report_Type,
report_id,
data_link,
Tag,
[Value] as Amount,
(SUBSTR(Instant_Date, 1, 4) || '-' || SUBSTR(Instant_Date, 5, 2) || '-' || SUBSTR(Instant_Date, 7, 2)) AS Instant_Date,
(SUBSTR(Submission_date, 1, 4) || '-' || SUBSTR(Submission_date, 5, 2) || '-' || SUBSTR(Submission_date, 7, 2)) AS submission_date,
(SUBSTR(start_date, 1, 4) || '-' || SUBSTR(start_date, 5, 2) || '-' || SUBSTR(start_date, 7, 2)) AS start_date,
(SUBSTR(end_date, 1, 4) || '-' || SUBSTR(end_date, 5, 2) || '-' || SUBSTR(end_date, 7, 2)) AS end_date
FROM manual_append_1;

CREATE TABLE IF NOT EXISTS alternate_ciks_adj AS
SELECT
*
FROM
alternate_ciks
where cik1 != cik2;


CREATE TABLE IF NOT EXISTS dup_cik_adj_1 AS
SELECT DISTINCT
a.*,
b.cik1,
b.cik2
FROM
date_table_1 a 
LEFT JOIN
alternate_ciks_adj b
on a.cik = b.cik2;

CREATE TABLE IF NOT EXISTS dup_cik_adj_2 AS
SELECT
company_name,
CASE WHEN cik1 IS NULL THEN cik
	 ELSE cik1
END AS cik,
cik1,
cik2,
report_type,
report_id,
data_link,
submission_date,
instant_date,
start_date,
end_date,
tag,
amount,
julianday(end_date) as end_date_julian,
julianday(start_date) as start_date_julian,
julianday(instant_date) as instant_date_julian
FROM dup_cik_adj_1;

CREATE TABLE IF NOT EXISTS date_table_2 AS
SELECT
Company_Name,
CIK,
cik2,
Report_Type,
report_id,
data_link,
Submission_Date,
Instant_Date,
Tag,
Amount,
start_date,
end_date,
instant_date,
max(end_date_julian) as max_end_date_julian,
start_date_julian,
instant_date_julian,
julianday(end_date) - julianday(start_date) AS date_diff,
CASE WHEN cik1 = cik then 'master'
	 ELSE 'new'
END AS Master_CIK_or_new_CIK
FROM dup_cik_adj_2
WHERE (report_type LIKE '10-K%' OR
	   report_type LIKE '40-F%' OR
	   report_type LIKE '20-F%')
GROUP BY
CIK,
cik2,
Report_Type,
report_id,
data_link,
start_date,
instant_date,
tag;

CREATE TABLE IF NOT EXISTS main_date_formatted AS
SELECT
Company_Name,
CIK,
cik2,
Report_Type,
report_id, 
data_link, 
Submission_Date,
Instant_Date,
Tag,
start_date, 
end_date, 
instant_date,
date_diff, 
Amount,
master_CIK_OR_NEW_CIK,
max(start_date_julian) as max_start_date_julian
FROM date_table_2
where (date_diff > 310 OR date_diff IS NULL)
GROUP BY
CIK,
cik2,
Report_Type,
report_id,
data_link,
instant_date,
Submission_Date,
Tag;

CREATE TABLE IF NOT EXISTS Ticker_Appended_Main
AS SELECT
company_name,
a.cik AS cik1,
cik2,
b.Top_Group_Description AS Industry,
b.sic_desc AS Sub_Industry,
report_type,
report_id,
data_link,
submission_date,
instant_date,
start_date,
end_date,
tag,
b.ticker,
b.cik AS CIK,
b.name,
a.Amount,
a.master_CIK_OR_NEW_CIK,
a.date_diff
FROM main_date_formatted a
INNER JOIN coinfo_expanded b
ON a.cik = b.cik
ORDER BY
b.ticker DESC,
submission_date ASC;

DROP TABLE IF EXISTS TAM_with_count_UNSTABLE;
CREATE TABLE IF NOT EXISTS TAM_with_count_UNSTABLE AS
SELECT 
a.*
FROM Ticker_Appended_Main a
where tag in ('earningspersharediluted','earningspersharebasic','earningspersharebasicanddiluted','cashandcashequivalentsatcarryingvalue',
			  'cash','netincomeloss','profitloss','cashandduefrombanks','operatingincomeloss','assetscurrent','assets',
		      'liabilitescurrent','liabilities',
			  'stockholdersequity','stockholdersequityincludingportionattributabletononcontrollinginterest',
			  'liabilitiesandstockholdersequity',
			  'accountspayablecurrent','accountsreceivablenetcurrent',
			  'researchanddevelopmentexpense','inventorynet');

--cleanup
DROP TABLE IF EXISTS date_table_1;
DROP TABLE IF EXISTS date_table_2;
DROP TABLE IF EXISTS main_date_formatted;
DROP TABLE IF EXISTS dup_cik_adj_1;
DROP TABLE IF EXISTS dup_cik_adj_2;
DROP TABLE IF EXISTS ticker_appended_main;
DROP TABLE IF EXISTS tag_count;
