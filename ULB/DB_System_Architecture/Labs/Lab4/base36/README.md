# PostgreSQL base36 data type

This datatype is internally a *bigint*, but only accepts positive values. It
inputs and outputs data as a number in radix 36, using `[0-9A-Za-z]` (case
insensitive) as its symbols in input and `[0-9A-Z]` in its output.

This data type is a quick hack and only has *demo* quality, its shy of a
brick load of being *production ready*. If you need it for serious work,
please consider opening an issue against this project, potentially with a
patch attached (they call that a *pull request* around here).

## Demo

    base36# create extension base36;
    CREATE EXTENSION
    
    base36# create table demo(i bigint, x base36);
    CREATE TABLE
    
    base36# insert into demo(i, x)
                 select n, n::bigint
    			   from generate_series(1, 10) t(n);
    INSERT 0 10
    
    base36# insert into demo(i, x)
                  select n, n::bigint
    			    from generate_series(10000, 10010) t(n);
    INSERT 0 11
    
    base36# insert into demo(i, x)
                 select n, n::bigint
    			   from generate_series(100000000, 100000010) t(n);
    INSERT 0 11
    
    base36# select * from demo;
    select * from demo;
         i     |   x    
    -----------+--------
             1 | 1
             2 | 2
             3 | 3
             4 | 4
             5 | 5
             6 | 6
             7 | 7
             8 | 8
             9 | 9
            10 | A
         10000 | 7PS
         10001 | 7PT
         10002 | 7PU
         10003 | 7PV
         10004 | 7PW
         10005 | 7PX
         10006 | 7PY
         10007 | 7PZ
         10008 | 7Q0
         10009 | 7Q1
         10010 | 7Q2
     100000000 | 1NJCHS
     100000001 | 1NJCHT
     100000002 | 1NJCHU
     100000003 | 1NJCHV
     100000004 | 1NJCHW
     100000005 | 1NJCHX
     100000006 | 1NJCHY
     100000007 | 1NJCHZ
     100000008 | 1NJCI0
     100000009 | 1NJCI1
     100000010 | 1NJCI2
    (32 rows)
    
    base36# create index on demo(x);
    CREATE INDEX

## Accepted range

The base36 accepted range is the same as the bigint one, albeit only for
positive numbers:

    base36# select pg_typeof(9223372036854775807);
     pg_typeof 
    -----------
     bigint
    (1 row)
    
    base36# select pg_typeof(9223372036854775808);
     pg_typeof 
    -----------
     numeric
    (1 row)
    
    base36# select 9223372036854775807::base36;
        base36     
    ---------------
     1Y2P0IJ32E8E7
    (1 row)
    
    base36# select 9223372036854775808::base36;
    ERROR:  cannot cast type numeric to base36 at character 27
    STATEMENT:  select 9223372036854775808::base36;
    ERROR:  42846: cannot cast type numeric to base36
    LINE 1: select 9223372036854775808::base36;
                                      ^
    LOCATION:  transformTypeCast, parse_expr.c:2247

And look at that, as I told you, not *production ready*.

    base36# select '-1'::base36;
    ERROR:  value '-' is not a valid digit for type base36. at character 8
    STATEMENT:  select '-1'::base36;
    ERROR:  XX000: value '-' is not a valid digit for type base36.
    LINE 1: select '-1'::base36;
                   ^
    LOCATION:  base36_from_str, base36.c:93
    
    base36# select -1::bigint::base36;
     ?column? 
    ----------
           -1
    (1 row)

