DROP TABLE IF EXISTS coinfo_1;
DROP TABLE IF EXISTS coinfo_expanded;

CREATE TABLE IF NOT EXISTS coinfo_1 AS
SELECT
a.*,
SUBSTR(sic,0, 3) as top_sic
FROM coinfo a;

CREATE TABLE IF NOT EXISTS coinfo_expanded AS
SELECT
a.*,
b.sic_description as Top_Group_Description
FROM coinfo_1 a
INNER JOIN
top_lvl_sics b
ON
a.top_sic = b.sic;
