create extension base36;

create table demo(i bigint, x base36);


insert into demo(i, x)
              select n, n::bigint
    		   from generate_series(1, 10) t(n);

insert into demo(i, x)
            select n, n::bigint
		    from generate_series(10000, 10010) t(n);


binsert into demo(i, x)
              select n, n::bigint
 			   from generate_series(100000000, 100000010) t(n);


select * from demo;

create index on demo(x);