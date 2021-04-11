DROP TABLE IF EXISTS Annual_Statements_i;
DROP TABLE IF EXISTS Annual_statements_p;
DROP TABLE IF EXISTS Annual_Statements_2;
DROP TABLE IF EXISTS Annual_Statements_3;
DROP TABLE IF EXISTS Annual_Statements_3v2;
DROP TABLE IF EXISTS Annual_Statements_4;
DROP TABLE IF EXISTS incosistent_date_adjustment;
DROP TABLE IF EXISTS incosistent_date_adjustment_2;
DROP TABLE IF EXISTS inconsistent_date_adjustment_3;
DROP TABLE IF EXISTS inconsistent_date_adjustment_4;
DROP TABLE IF EXISTS inconsistent_date_adjustment_5;
DROP TABLE IF EXISTS annual_statements_5;

CREATE TABLE Annual_Statements_i AS 
SELECT 
Ticker, 
Name, 
CIK, 
CIK2, 
Industry,
Sub_Industry,
Report_Type, 
report_id,
Data_Link, 
Submission_date, 
Instant_date,
end_date,
sum(CASE WHEN tag = 'cashandcashequivalentsatcarryingvalue' THEN amount end) as 'cashandcashequivalentsatcarryingvalue',
sum(CASE WHEN tag = 'cash' THEN amount end) as 'cash',
sum(CASE WHEN tag = 'cashandduefrombanks' then amount end) as 'cashandduefrombanks',
sum(CASE WHEN tag = 'assetscurrent' THEN amount end) as 'assetscurrent',
sum(CASE WHEN tag = 'assets' THEN amount end) as 'assets',
sum(CASE WHEN tag = 'liabilities' THEN amount end) as 'liabilities',
sum(CASE WHEN tag = 'stockholdersequity' THEN amount end) as 'stockholdersequity',
sum(CASE WHEN tag = 'stockholdersequityincludingportionattributabletononcontrollinginterest' THEN amount end) as 'stockholdersequityincludingportionattributabletononcontrollinginterest',
sum(CASE WHEN tag = 'liabilitiesandstockholdersequity' THEN amount end) as 'liabilitiesandstockholdersequity',
sum(CASE WHEN tag = 'accountspayablecurrent' THEN amount end) as 'accountspayablecurrent',
sum(CASE WHEN tag = 'accountsreceivablenetcurrent' THEN amount end) as 'accountsreceivablenetcurrent',
sum(CASE WHEN tag = 'inventorynet' THEN amount end) as 'inventorynet' 
from tam_with_count_unstable
group by
Ticker, 
Name, 
CIK, 
CIK2, 
Industry,
Sub_Industry,
Report_Type,
report_id, 
Data_Link, 
Submission_date,
end_date,
instant_date
order by 
Ticker asc, 
CIK2 asc, 
submission_date desc;

CREATE TABLE Annual_Statements_p AS 
SELECT 
Ticker, 
Name, 
CIK, 
CIK2, 
Industry,
Sub_Industry,
Report_Type, 
report_id,
Data_Link, 
Submission_date, 
Instant_date,
end_date,
sum(CASE WHEN tag = 'earningspersharediluted' THEN amount end) as 'earningspersharediluted',
sum(CASE WHEN tag = 'earningspersharebasic' THEN amount end) as 'earningspersharebasic',
sum(CASE WHEN tag = 'earningspersharebasicanddiluted' THEN amount end) as 'earningspersharebasicanddiluted',
sum(CASE WHEN tag = 'netincomeloss' THEN amount end) as 'netincomeloss',
sum(CASE WHEN tag = 'profitloss' THEN amount end) as 'profitloss',
sum(CASE WHEN tag = 'operatingincomeloss' THEN amount end) as 'operatingincomeloss',
sum(CASE WHEN tag = 'researchanddevelopmentexpense' THEN amount end) as 'researchanddevelopmentexpense'
from tam_with_count_unstable
where date_diff > 300 or date_diff IS NULL
group by
Ticker, 
Name, 
CIK, 
CIK2, 
Industry,
Sub_Industry,
Report_Type, 
report_id,
Data_Link, 
Submission_date,
end_date,
instant_date
order by 
Ticker asc, 
CIK2 asc, 
submission_date desc;

DROP TABLE IF EXISTS Annual_Statements_2;
CREATE TABLE Annual_Statements_2 AS 
select
Ticker, 
Name, 
CIK, 
CIK2, 
Industry,
Sub_Industry,
Report_Type,
report_id, 
Data_Link, 
Submission_date, 
Instant_date,
max(end_date) as end_date,
earningspersharediluted,
earningspersharebasic,
earningspersharebasicanddiluted,
netincomeloss,
profitloss,
operatingincomeloss,
researchanddevelopmentexpense
from
annual_statements_p
where instant_date = '--'
group by
Ticker, 
Name, 
CIK, 
CIK2, 
Industry,
Sub_Industry,
Report_Type, 
report_id,
Data_Link, 
Submission_date, 
Instant_date;

DROP TABLE IF EXISTS Annual_Statements_3;
CREATE TABLE Annual_Statements_3 AS 
select
Ticker, 
Name, 
CIK, 
CIK2, 
Industry,
Sub_Industry,
Report_Type, 
report_id,
Data_Link, 
Submission_date, 
Max(instant_date) as instant_date,
end_date,
cashandcashequivalentsatcarryingvalue,
cash,
cashandduefrombanks,
assetscurrent,
assets,
liabilities,
stockholdersequity,
stockholdersequityincludingportionattributabletononcontrollinginterest,
liabilitiesandstockholdersequity,
accountspayablecurrent,
accountsreceivablenetcurrent,
inventorynet 
from
annual_statements_i
where end_date = '--'
group by
Ticker, 
Name, 
CIK, 
CIK2, 
Industry,
Sub_Industry,
Report_Type,
report_id, 
Data_Link, 
Submission_date, 
end_date;


CREATE TABLE annual_statements_4 AS
SELECT
a.Ticker, 
a.Name, 
a.CIK, 
a.CIK2, 
a.Industry,
a.Sub_Industry,
a.Report_Type, 
a.report_id,
a.Data_Link, 
a.Submission_date, 
b.Instant_date,
a.end_date,
a.earningspersharediluted,
a.earningspersharebasic,
a.earningspersharebasicanddiluted,
b.cashandcashequivalentsatcarryingvalue,
b.cash,
b.cashandduefrombanks,
a.netincomeloss,
a.profitloss,
a.operatingincomeloss,
b.assetscurrent,
b.assets,
b.liabilities,
b.stockholdersequity,
b.stockholdersequityincludingportionattributabletononcontrollinginterest,
b.liabilitiesandstockholdersequity,
b.accountspayablecurrent,
b.accountsreceivablenetcurrent,
b.inventorynet,
a.researchanddevelopmentexpense
FROM
annual_statements_3 b
INNER JOIN
annual_statements_2 a
ON a.report_id = b.report_id
AND a.end_date = b.instant_date
ORDER BY
a.ticker asc,
a.cik2,
a.submission_date desc;

CREATE TABLE IF NOT EXISTS inconsistent_date_adjustment AS
SELECT 
a.report_id,
a.end_date,
b.instant_date
FROM
annual_statements_2 a 
INNER JOIN
annual_statements_3 b 
USING(report_id);

CREATE TABLE IF NOT EXISTS inconsistent_date_adjustment_2 AS
SELECT
*,
CASE WHEN (instant_date > end_date) THEN 'priority_i'
     WHEN (instant_date < end_date) THEN 'priority_p'
	 WHEN (instant_date = end_date) THEN 'identical'
	 ELSE 'ERROR'
END AS date_comp
FROM inconsistent_date_adjustment;

CREATE TABLE IF NOT EXISTS inconsistent_date_adjustment_3 AS
SELECT 
Ticker, 
Name, 
CIK, 
CIK2, 
Industry,
Sub_Industry,
Report_Type, 
report_id,
Data_Link, 
Submission_date, 
Instant_date,
end_date,
earningspersharediluted,
earningspersharebasic,
earningspersharebasicanddiluted,
NULL AS cashandcashequivalentsatcarryingvalue,
NULL AS cash,
NULL AS cashandduefrombanks,
netincomeloss,
profitloss,
operatingincomeloss,
NULL AS assetscurrent,
NULL AS assets,
NULL AS liabilities,
NULL AS stockholdersequity,
NULL AS stockholdersequityincludingportionattributabletononcontrollinginterest,
NULL AS liabilitiesandstockholdersequity,
NULL AS accountspayablecurrent,
NULL AS accountsreceivablenetcurrent,
NULL AS inventorynet,
researchanddevelopmentexpense
FROM annual_statements_2
UNION ALL
SELECT 
Ticker, 
Name, 
CIK, 
CIK2, 
Industry,
Sub_Industry,
Report_Type,
report_id, 
Data_Link, 
Submission_date, 
instant_date,
end_date,
NULL AS earningspersharediluted,
NULL AS earningspersharebasic,
NULL AS earningspersharebasicanddiluted,
cashandcashequivalentsatcarryingvalue,
cash,
cashandduefrombanks,
NULL AS netincomeloss,
NULL AS profitloss,
NULL AS operatingincomeloss,
assetscurrent,
assets,
liabilities,
stockholdersequity,
stockholdersequityincludingportionattributabletononcontrollinginterest,
liabilitiesandstockholdersequity,
accountspayablecurrent,
accountsreceivablenetcurrent,
inventorynet,
NULL AS researchanddevelopmentexpense 
FROM annual_statements_3 b;

CREATE TABLE IF NOT EXISTS inconsistent_date_adjustment_4 AS
SELECT
*
FROM inconsistent_date_adjustment_3
WHERE
report_id IN
	(SELECT 
	 report_id
	 FROM inconsistent_date_adjustment_2
	 WHERE date_comp IN ('priority_i','priority_p'));
	 
CREATE TABLE IF NOT EXISTS inconsistent_date_adjustment_5 AS
SELECT
Ticker, 
Name, 
CIK, 
CIK2,
Industry,
Sub_Industry,
Report_Type, 
report_id,
Data_Link, 
Submission_date, 
Instant_date,
end_date,
earningspersharediluted,
earningspersharebasic,
earningspersharebasicanddiluted,
cashandcashequivalentsatcarryingvalue,
cash,
cashandduefrombanks,
netincomeloss,
profitloss,
operatingincomeloss,
assetscurrent,
assets,
liabilities,
stockholdersequity,
stockholdersequityincludingportionattributabletononcontrollinginterest,
liabilitiesandstockholdersequity,
accountspayablecurrent,
accountsreceivablenetcurrent,
inventorynet,
researchanddevelopmentexpense
FROM  inconsistent_date_adjustment_4;

CREATE TABLE IF NOT EXISTS annual_statements_5 AS
SELECT
a.*
FROM annual_statements_4 a
UNION ALL
SELECT 
b.*
FROM inconsistent_date_adjustment_5 b
ORDER BY
a.ticker asc,
a.cik2,
a.submission_date desc;