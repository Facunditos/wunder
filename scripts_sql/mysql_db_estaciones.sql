/*USE [master]
GO


CREATE DATABASE estaciones_wunder
GO*/


CREATE DATABASE estaciones_wunder

use estaciones_wunder


-------------------------------------------------      observaciones         --------------------------------------------------

drop table observaciones;
delete from observaciones;
insert into observaciones values
	(1,'2024-07-01 00:04:00',457800.78,0,0);


-- lluvia acumulada por día 
select date(obsTimeLocal) , max(precipTotal_mm) 
from observaciones obs
where id_estacion =7 
group by date(obsTimeLocal)


select *
from observaciones obs
where id_estacion =7 and DATE(obsTimeLocal) = '2023-12-01'
where (precipTotal_mm is null) and (dia_con_obs =1)


select SUM(precipTotal_mm)
from observaciones o 


select *
from observaciones obs 
where (obs.obsTimeLocal  between '2024-10-01 00:00:00' AND '2024-10-15 23:59:59')
order by obsTimeLocal desc

delete from observaciones
where (id_estacion =17) 



select est.stationID,obs.obsTimeLocal , obs.precipTotal ,obs.dia_con_obs 
from observaciones obs
join estaciones est
on obs.id_estacion = est.id_estacion
#where (obs.id_estacion  = 4)
order by obs.obsTimeLocal DESC;

select obsTimeLocal ,count(*) 
from observaciones o 
where dia_con_obs =0
group by obsTimeLocal 


select est.stationID,min(obs.obsTimeLocal),max(obs.obsTimeLocal),est.id_estacion 
from observaciones obs 
join estaciones est
on obs.id_estacion = est.id_estacion
group by est.stationID 

select *
from observaciones obs 
join estaciones est
on obs.id_estacion = est.id_estacion
where est.id_estacion = 3
order by obs.obsTimeLocal desc


select *
from observaciones obs 
join estaciones est
on obs.id_estacion = est.id_estacion
where (stationID like '%35%') and (obs.obsTimeLocal between '2024-03-02' and '2024-03-03')


select distinct o.id_estacion , sum() o.dia_completo 
from observaciones o 

select count(*)
from observaciones obs
join estaciones est
on obs.id_estacion = est.id_estacion
where obs.dia_con_obs =0 ;

insert into observaciones (id_estacion,obsTimeLocal,precipTotal,dia_con_obs,dia_completo)
values (17,'2024-10-12 00:04:49',0.5,1,1);


select datalength(id_observacion) as bytes_id_observacion,datalength(id_estacion) as bytes_id_estacion,datalength(obsTimeLocal) as bytes_obsTimeLocal,datalength(precipTotal) as bytes_precipTotal,datalength(dia_con_obs) as bytes_dia_con_obs,datalength(dia_completo) as bytes_dia_completo
from observaciones;

-------------------------------------------------      estaciones       --------------------------------------------------

drop table estaciones;
delete from estaciones;
insert into estaciones values
	('IPREZ1',-32.997496,-60.768009);

select *
from estaciones e ;

select *
from estaciones
join observaciones 
on estaciones.id_estacion=observaciones.id_estacion;

select datalength(id_estacion) as bytes_estacion,datalength(stationID) as bytes_stationID,datalength(lat) as bytes_lat,datalength(lon) as bytes_lon
from estaciones;

--personas

drop table personas
CREATE TABLE [dbo].[personas](
	altura float(24),
	peso decimal(7,2),
	nacimiento datetime2(0)
)

delete from personas
insert into personas values 
	(2340.5,2340.5,'1989-1-3 20:05:2'),
	(-20.122,-20.120,'1991-04-07');

select * 
from personas;

select datalength(altura) as bytes_altura,datalength(peso) as bytes_altura,datalength(nacimiento) as bytes_altura
from personas;