/*USE [master]
GO


CREATE DATABASE [estaciones_wunder]
GO*/


use estaciones_wunder

drop table observaciones
CREATE TABLE [dbo].[observaciones](
	id_observacion,
	id_estacion,
	obsTimeUtc,
	obsTimeLocal,
	epoch,
	solarRadiationHigh,
	uvHigh,
	winddirAvg,
	humidityHigh,
	humidityLow,
	humidityAvg,
	qcStatus,
	tempHigh,
	tempLow,
	tempAvg,
	windspeedHigh,
	windspeedLow,
	windspeedAvg,
	windgustHigh,
	windgustLow,
	windgustAvg,
	dewptHigh,
	dewptLow,
	dewptAvg,
	windchillHigh,
	windchillLow,
	windchillAvg,
	heatindexHigh,
	heatindexLow,
	heatindexAvg,
	pressureMax,
	pressureMin,
	pressureTrend,
	precipRate,
	precipTotal
)

CREATE TABLE [dbo].[estaciones](
	id_estacion
	stationID int IDENTITY(1,1) NOT NULL,
	tz,
	lat,
	lon,
)

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