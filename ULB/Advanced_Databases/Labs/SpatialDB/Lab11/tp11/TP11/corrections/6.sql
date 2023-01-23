SELECT name, ST_AsText((position).geom), ST_Value(rast, (position).geom)
FROM (SELECT name, rast, ST_DumpPoints(ST_Segmentize(geom, 0.1)) AS position
      FROM belriver JOIN bel_alt on ST_Intersects(geom, rast)) AS dp;

