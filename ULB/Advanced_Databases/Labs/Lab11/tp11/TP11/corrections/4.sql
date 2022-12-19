SELECT name, (stats).min, (stats).max
FROM (SELECT name, ST_SummaryStats(ST_Clip(rast, 1, geom, TRUE)) AS stats
      FROM alt JOIN bel_prov ON ST_Intersects(geom,rast)) AS foo;
