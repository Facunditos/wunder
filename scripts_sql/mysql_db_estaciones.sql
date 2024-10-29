/*USE [master]
GO

GO*/
CREATE DATABASE estaciones_wunder



use estaciones_wunder


--observaciones

drop table observaciones;
delete from observaciones;
insert into observaciones values
	(1,'2024-07-01 00:04:00',457800.78,0,0);

select *
from observaciones

select *
from observaciones obs
join estaciones est
on obs.id_estacion = est.id_estacion
where obs.precipTotal>0 and est.stationID like 'IROSAR18';


select datalength(id_observacion) as bytes_id_observacion,datalength(id_estacion) as bytes_id_estacion,datalength(obsTimeLocal) as bytes_obsTimeLocal,datalength(precipTotal) as bytes_precipTotal,datalength(dia_con_obs) as bytes_dia_con_obs,datalength(dia_completo) as bytes_dia_completo
from observaciones;

--estaciones

drop table estaciones;
delete from estaciones;
insert into estaciones values
	('IPREZ1',-32.997496,-60.768009);

select *
from estaciones;

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