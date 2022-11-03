EXTENSION   = base36
MODULES     = base36
DATA        = base36--1.0.sql base36.control

LDFLAGS=-lrt

PG_CONFIG ?= pg_config
PGXS = $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)
