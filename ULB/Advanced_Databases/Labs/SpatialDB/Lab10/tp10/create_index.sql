create index cities_geom_idx on cities USING GIST (geom);
create index regions_geom_idx on regions USING GIST (geom);
vacuum analyze; -- resets query optimizer statistics
