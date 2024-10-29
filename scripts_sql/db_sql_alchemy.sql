
use sql_alchemy;
select *
from user_account
where name in ('sandy','spongebob');


select a.id,a.email_address
from user_account u
join address a
on u.id = a.user_id
where u.name='sandy' and a.email_address like '%sandy@sql%';

select *
from address;

select 'Hello World';

select *
from some_table


insert into some_table values 
	(3,9),
	(4,16),
	(5,25);

select * from some_table;

delete from address where user_id=2;
select * from address
select * from user_account

drop table equipo;
create table equipo(
	id_equipo int,
	nombre varchar(20),
	primary key (id_equipo),
)
drop table dt;
create table dt(
	id_dt int,
	nombre varchar(20),
	equipo int,
	primary key (id_dt),
	--foreign key fk_dt_equipo (id_equipo) ;
);

alter table dt 
add constraint fk_equipo_dt
foreign key (id_equipo) references equipo(id_equipo);




insert into user_account values 
	('ramiro','ramiro@gamil.com');


SELECT u_a.id, u_a.name, u_a.fullname 
FROM user_account u_a
ORDER BY u_a.name 

drop table student_account;
create table student_account(
	id int primary key identity,
	name varchar(30),
	age tinyint
)


insert into student_account 
	values 
		('maite',20);

(select *
from user_account)
union all
(select * 
from student_account);

select *
from user_account

select *
from user_account u_a
full join address a
on u_a.id = a.user_id

insert into address
	values
		(120,'alckemy@org.com.ar');

alter table address
alter column  user_id
INT NULL;