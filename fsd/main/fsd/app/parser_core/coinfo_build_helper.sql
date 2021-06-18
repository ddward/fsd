DROP TABLE IF EXISTS helper_1;

CREATE TABLE IF NOT EXISTS omitted_tickers 
(
ticker TEXT,
exchange TEXT,
ticker_pull_date TEXT,
cik_pull_date TEXT,
cik_pull_success TEXT,
cik TEXT,
included_in_coinfo TEXT
);

CREATE TABLE IF NOT EXISTS helper_1 AS
SELECT DISTINCT
ticker,
exchange,
date_confirmed as ticker_pull_date
FROM
ticker_by_exchange
WHERE ticker NOT IN
(SELECT DISTINCT ticker FROM coinfo
 UNION ALL
 SELECT DISTINCT ticker FROM omitted_tickers);

INSERT INTO omitted_tickers (ticker, exchange, ticker_pull_date)
SELECT ticker, exchange, ticker_pull_date
FROM
helper_1;
