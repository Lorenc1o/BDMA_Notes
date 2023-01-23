-- Executing the MapAlgebra function without resampeling will not work as the two raster
-- do not have the same granularity

create table sol1 as 
SELECT ST_MapAlgebra( a.rast, 1, b.rast, 1, '[rast2] - [rast1]') AS rast 
FROM 
    (select b.RID, ST_Resample(b.rast, a.rast) as rast
     from bel_alt b,  alt a) 
as b, alt a;

-- To execute in the terminal, then drag and drop the sol1.tiff in qgis
-- $ gdal_translate -of GTiff PG:"dbname=tp11 schema=public table=sol1" sol1.tiff
