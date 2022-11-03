--1
SELECT SUM(storesales) as sales, SUM(storecost) as cost, SUM(unitsales) as unitsales
FROM sales;

--2
SELECT st.storestate, SUM(storesales) as sales, SUM(storecost) as cost, SUM(unitsales) as unitsales
FROM sales sa
JOIN store st ON st.storeid = sa.storeid
WHERE st.storestate = ANY('{CA,WA}'::varchar[])
GROUP BY st.storestate;

--3
SELECT st.storecity, SUM(storesales) as sales, SUM(storecost) as cost, SUM(unitsales) as unitsales
FROM sales sa
JOIN store st ON st.storeid = sa.storeid
WHERE st.storestate = ANY('{CA,WA}'::varchar[])
GROUP BY st.storecity;

--4
SELECT st.storecity, st.storestate, SUM(storesales) as sales, SUM(storecost) as cost, SUM(unitsales) as unitsales
FROM sales sa
JOIN store st ON st.storeid = sa.storeid
WHERE st.storestate = 'CA'
GROUP BY CUBE(st.storecity, st.storestate)
HAVING storestate IS NOT NULL;

--5
SELECT st.storetype, st.storestate, AVG(storesales::numeric::float) as avgsales
FROM sales sa
JOIN store st ON st.storeid = sa.storeid
JOIN date d ON d.dateid = sa.dateid
WHERE d.year = 2017
GROUP BY CUBE(st.storetype, st.storestate);

--6
WITH amplified_sales AS(
	SELECT *, 'S1' as semester
	FROM sales sa
	JOIN date d ON d.dateid = sa.dateid
	WHERE d.year = 2017 AND d.quarter = ANY('{Q1,Q2}'::varchar[])
	
	UNION
	
	SELECT *, 'S2' as semester
	FROM sales sa
	JOIN date d ON d.dateid = sa.dateid
	WHERE d.year = 2017 AND d.quarter = ANY('{Q3,Q4}'::varchar[])
)
SELECT st.storeid, sa.semester as semester, SUM(storesales::numeric::float - storecost::numeric::float) as profit
FROM amplified_sales sa
JOIN store st USING (storeid)
GROUP BY CUBE(st.storeid, sa.semester);

--7
WITH amplified_sales AS(
	SELECT *, 'S1' as semester
	FROM sales sa
	JOIN date d ON d.dateid = sa.dateid
	WHERE d.year = 2017 AND d.quarter = ANY('{Q1,Q2}'::varchar[])
	
	UNION
	
	SELECT *, 'S2' as semester
	FROM sales sa
	JOIN date d ON d.dateid = sa.dateid
	WHERE d.year = 2017 AND d.quarter = ANY('{Q3,Q4}'::varchar[])
)
SELECT st.storeid, sa.semester as semester, SUM(storesales::numeric::float - storecost::numeric::float) as profit
FROM amplified_sales sa
JOIN store st USING (storeid)
GROUP BY CUBE(st.storeid, sa.semester);
