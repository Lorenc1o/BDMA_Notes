SELECT name, ST_Value(rast, geom) FROM bel_alt JOIN bel_city ON ST_Intersects(geom, rast);
