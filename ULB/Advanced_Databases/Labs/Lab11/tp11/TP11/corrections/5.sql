CREATE TABLE alt_16_belgium AS
SELECT rid, ST_Clip(rast, 1, geom, TRUE) AS rast
FROM (SELECT ST_UNION(ARRAY(SELECT geom FROM bel_regn)) AS geom) AS belgium
JOIN alt ON ST_Intersects(geom, rast);
