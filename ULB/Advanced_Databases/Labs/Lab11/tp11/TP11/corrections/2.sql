SELECT (stats).max
FROM (SELECT ST_SummaryStats(rast, 1) AS stats
      FROM bel_alt WHERE rid=1) AS foo;
