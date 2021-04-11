
DROP TABLE IF EXISTS q_adjustment_adjustment_1;
DROP TABLE IF EXISTS q_adjustment_adjustment_2;
DROP TABLE IF EXISTS q_duplicate_link_adjustment_1;
DROP TABLE IF EXISTS q_duplicate_link_adjustment_2;
DROP TABLE IF EXISTS q_stella_test_1;
DROP TABLE IF EXISTS q_stella_test_2;
DROP TABLE IF EXISTS q_stella_test_3;
DROP TABLE IF EXISTS q_stella_test_4;
DROP TABLE IF EXISTS q_duplicate_link_adjustment_3;
DROP TABLE IF EXISTS q_duplicate_link_adjustment_4;
DROP TABLE IF EXISTS q_duplicate_link_adjustment_5;
DROP TABLE IF EXISTS quarterly_daily_formatted;

CREATE TABLE IF NOT EXISTS q_adjustment_adjustment_1
AS SELECT
distinct
report_id,
max(julianday(submission_date)) as max_submission_julian
from quarterly_Statements_5
group by
ticker,
end_date,
cik,
cik2;

CREATE TABLE IF NOT EXISTS q_adjustment_adjustment_2 AS 
SELECT
DISTINCT
a.*
from quarterly_statements_4 a
inner join q_adjustment_adjustment_1 b
on a.report_id = b.report_id;

CREATE TABLE IF NOT EXISTS q_duplicate_link_adjustment_1 AS
SELECT
DISTINCT
report_id,
COUNT(report_id) AS link_count
FROM q_adjustment_adjustment_2
GROUP BY
report_id;

CREATE TABLE IF NOT EXISTS q_duplicate_link_adjustment_2 AS
SELECT
a.*,
b.link_count
FROM q_adjustment_adjustment_2 a
INNER JOIN
q_duplicate_link_adjustment_1 b
ON a.report_id = b.report_id;

CREATE TABLE IF NOT EXISTS q_stella_test_1 AS
SELECT
DISTINCT
report_id,
count(DISTINCT ticker) as ticker_count
FROM q_duplicate_link_adjustment_2
WHERE link_count > 1
GROUP BY
report_id;

CREATE TABLE IF NOT EXISTS q_stella_test_2 AS
SELECT
DISTINCT
report_id,
cik,
cik2
FROM q_duplicate_link_adjustment_2
WHERE link_count > 1;

CREATE TABLE IF NOT EXISTS q_stella_test_3 AS
SELECT
DISTINCT
report_id,
count(report_id) as cik_count
FROM q_stella_test_2
GROUP BY
report_id;

CREATE TABLE IF NOT EXISTS q_duplicate_link_adjustment_5 AS
SELECT
DISTINCT
a.*,
b.ticker_count,
c.cik_count
FROM  
q_duplicate_link_adjustment_2 a LEFT JOIN
q_stella_test_1 b ON a.report_id = b.report_id LEFT JOIN
q_stella_test_3 c on a.report_id = c.report_id;

CREATE TABLE IF NOT EXISTS quarterly_daily_formatted AS
SELECT
distinct
*
FROM q_duplicate_link_adjustment_5
WHERE
link_count = 1 OR 
(link_count != 1 AND ticker_count > 1 AND cik_count > 1 AND cik2 IS NULL) OR
(link_count != 1 AND ticker_count = 1 AND cik_count > 1 AND cik2 IS NULL) OR
(link_count !=1 AND ticker_count > 1 AND cik_count = 1);
