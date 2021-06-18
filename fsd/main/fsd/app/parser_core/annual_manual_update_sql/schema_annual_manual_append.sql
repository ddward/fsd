DROP TABLE IF EXISTS combine_1;

CREATE TABLE IF NOT EXISTS annual_pre AS
SELECT * 
FROM annual_full_formatted;

DELETE FROM annual_pre WHERE
data_link in (SELECT DISTINCT data_link FROM annual_manual_formatted);

DROP TABLE IF EXISTS annual_post;

CREATE TABLE IF NOT EXISTS annual_post AS
SELECT
*
FROM annual_pre
UNION ALL
SELECT
* 
FROM annual_manual_formatted;

DROP TABLE IF EXISTS annual_pre;
CREATE TABLE annual_pre AS
SELECT
*
FROM annual_post;

DROP TABLE IF EXISTS annual_full_formatted;
CREATE TABLE IF NOT EXISTS annual_full_formatted AS
SELECT *
FROM annual_post;

CREATE TABLE IF NOT EXISTS combine_1 AS
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
annual_post;

DROP TABLE IF EXISTS annual_formatted;
CREATE TABLE IF NOT EXISTS annual_formatted AS
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
combine_1
ORDER BY
ticker ASC,
"Pre-Merger/Restructure SEC ID",
"Date Reported" DESC;
