create table users(id integer auto_increment primary key,name text not null,
                   password text not null,admin boolean not null default 0);




create table emp ( id integer AUTOINCREMENT primary key,name text not null,email text,phone integer,address text,
joining_date timestamp default current_timestamp,total_projects integer default 1,
total_test_case integer default 1,total_defects_found integer default 1,total_defects_pending integer default 1);
