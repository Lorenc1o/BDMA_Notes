-- complain if script is sourced in psql, rather than via CREATE EXTENSION
\echo Use "CREATE EXTENSION base36" to load this file. \quit

CREATE OR REPLACE FUNCTION base36_encode(integer) 
RETURNS cstring 
AS '$libdir/base36'
LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION base36_in(cstring)
RETURNS base36
AS '$libdir/base36'
LANGUAGE C IMMUTABLE STRICT;

--base36_out(base36)
CREATE OR REPLACE FUNCTION base36_out(base36)
RETURNS cstring
AS '$libdir/base36'
LANGUAGE C IMMUTABLE STRICT;

--base36_recv
CREATE OR REPLACE FUNCTION base36_recv(internal) RETURNS base36
AS '$libdir/base36'
LANGUAGE C IMMUTABLE STRICT;

--base36_send
CREATE OR REPLACE FUNCTION base36_send(base36) RETURNS bytea
AS '$libdir/base36'
LANGUAGE C IMMUTABLE STRICT;

CREATE TYPE base36 (
	INPUT          = base36_in,
	OUTPUT         = base36_out,
	RECEIVE        = base36_recv,
	SEND           = base36_send,
	LIKE           = bigint,
	CATEGORY       = 'N'
);
COMMENT ON TYPE base36 IS 'bigint written in base36: [0-9A-Z]+';


