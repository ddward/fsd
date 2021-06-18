DROP TABLE IF EXISTS q_combine_1;
DROP TABLE IF EXISTS quarterly_pre;

CREATE TABLE IF NOT EXISTS quarterly_pre AS
SELECT * 
FROM quarterly_full_formatted;

DROP TABLE IF EXISTS quarterly_post;

CREATE TABLE IF NOT EXISTS quarterly_post AS
SELECT
*
FROM quarterly_pre
UNION ALL
SELECT
* 
FROM quarterly_daily_formatted;

DROP TABLE IF EXISTS quarterly_pre;
CREATE TABLE quarterly_pre AS
SELECT
*
FROM quarterly_post;

DROP TABLE IF EXISTS quarterly_full_formatted;
CREATE TABLE IF NOT EXISTS quarterly_full_formatted AS
SELECT *
FROM quarterly_post;

CREATE TABLE IF NOT EXISTS q_combine_1 AS
SELECT
ticker,
name,
CIK,
cik2,
Industry,
Sub_Industry,
Report_Type,
Report_ID,
Data_Link,
Submission_Date,
Instant_Date,
End_date,
CASE WHEN (earningspersharediluted = NULL) THEN earningspersharebasicanddiluted
     ELSE earningspersharediluted
     END AS earningspersharediluted,
CASE WHEN (earningspersharebasic = NULL) THEN earningspersharebasicanddiluted
     ELSE earningspersharebasic
     END AS earningspersharebasic,
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
liabilitiesandstockholdersequity,
accountspayablecurrent,
accountsreceivablenetcurrent,
inventorynet,
researchanddevelopmentexpense
FROM
quarterly_post;

DROP TABLE IF EXISTS quarterly_formatted;
CREATE TABLE IF NOT EXISTS quarterly_formatted AS
SELECT DISTINCT
ticker as "Stock Ticker",
name as "Company Name",
CIK as "Company SEC ID",
cik2 as "Previous SEC ID",
Industry,
Sub_industry as "Sub-Industry",
Report_type as "Report Type",
Data_link as "SEC Data Link",
submission_date as "Date Reported",
instant_date as "Period Ending Date",
earningspersharediluted,
earningspersharebasic,
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
liabilitiesandstockholdersequity,
accountspayablecurrent,
accountsreceivablenetcurrent,
inventorynet,
researchanddevelopmentexpense
FROM
q_combine_1
ORDER BY
ticker ASC,
"Pre-Merger/Restructure SEC ID",
"Date Reported" DESC;
