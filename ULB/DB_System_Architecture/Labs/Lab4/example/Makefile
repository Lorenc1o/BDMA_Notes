EXTENSION   = example
MODULES     = example
DATA        = example--1.0.sql example.control

LDFLAGS=-lrt

PG_CONFIG ?= pg_config
PGXS = $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)


