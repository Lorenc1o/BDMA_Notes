CREATE TABLE "regions" (
        "id" serial primary key,
        "name" varchar(17));
CREATE TABLE "cities" (
        "id" serial primary key,
        "name" varchar(20));

ALTER TABLE regions ADD COLUMN geom geometry(MULTIPOLYGON,4326);
ALTER TABLE cities ADD COLUMN geom geometry(POINT,4326);
