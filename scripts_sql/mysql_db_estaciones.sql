/*USE [master]
GO


CREATE DATABASE estaciones_wunder
GO*/


CREATE DATABASE estaciones_wunder

use estaciones_wunder


CREATE TABLE `ptos` (
  `punto` geometry NOT NULL,
  SPATIAL KEY `punto` (`punto`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO ptos  VALUES (POINT (1,2) );
INSERT INTO ptos VALUES (ST_PointFromText(`POINT(-6.64227 40.96303)`, 4326));
INSERT INTO ptos VALUES (ST_PointFromText(`POINT(-6.66115 40.95858)`, 4326));
INSERT INTO ptos VALUES (ST_PointFromText(`POINT(-6.68685 40.93992)`, 4326));

-------------------------------------------------      observaciones         --------------------------------------------------

drop table observaciones;
delete from observaciones;
insert into observaciones values
	(1,'2024-07-01 00:04:00',457800.78,0,0);


-- lluvia acumulada por día 
select date(obsTimeLocal) , max(precipTotal_mm) 
from observaciones obs
group by date(obsTimeLocal)


select obs.id_estacion,lat,lon,max(precipTotal_mm )
from observaciones obs
join estaciones e 
on obs.id_estacion = e.id_estacion 
where DATE(obsTimeLocal) = '2024-11-27'
group by obs.id_estacion,lat,lon


select SUM(precipTotal_mm)
from observaciones o 


select *
from observaciones obs 
where (obs.obsTimeLocal  between '2024-10-01 00:00:00' AND '2024-10-15 23:59:59')
order by obsTimeLocal desc

delete from observaciones
where (id_estacion =17) 



select est.stationID,min(obs.tempAvg_grados_C)
from observaciones obs
join estaciones est
on obs.id_estacion = est.id_estacion
where est.comentario like '%2%'
group by est.stationID ;

select obsTimeLocal ,count(*) 
from observaciones o 
where dia_con_obs =0
group by obsTimeLocal 


select est.stationID,min(obs.obsTimeLocal),max(obs.obsTimeLocal),est.id_estacion 
from observaciones obs 
join estaciones est
on obs.id_estacion = est.id_estacion
group by est.stationID 

select year(obs.obsTimeLocal),month(obs.obsTimeLocal),day(obs.obsTimeLocal),min(obs.tempAvg_grados_C)
from observaciones obs 
group by year(obs.obsTimeLocal),month(obs.obsTimeLocal),day(obs.obsTimeLocal)


select id_estacion,max(obsTimeLocal) , min(obs.tempAvg_grados_C)
from observaciones obs 
where year(obs.obsTimeLocal) = 2024 and month(obs.obsTimeLocal) =11
group by obs.id_estacion 

select *
from observaciones obs 
where id_estacion =1 and  year(obs.obsTimeLocal) = 2024 






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
from estaciones e 
order by stationID 

-- DELETE FROM estaciones  WHERE statio;

update estaciones 
set comentario = 'lote 1 - sin observaciones'
where id_estacion in (17,54,92,107)

delete 
from estaciones where id_estacion >= 144;

alter table estaciones 
add ult_reporte datetime default null;



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