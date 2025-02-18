create database wunder;
drop database wunder;

CREATE EXTENSION postgis;

drop table estaciones;
CREATE TABLE estaciones (
  id_estacion int primary key,
  stationID varchar(20) NOT NULL,
  tz varchar(50),
  ubicacion geometry,
  inicio timestamp,
  comentario varchar(50),
  ult_reporte timestamp
) 

drop table reportes;

alter table estaciones
add constraint estacones_ubicacion_point_chk
    check(st_geometrytype(ubicacion) = 'ST_Point'::text);
   

select id_estacion  ,max("obsTimeLocal") as hora ,max("precipTotal_mm") as lluvia_acum
from reportes r 
where fecha ='2025-01-19'
group by id_estacion 
having max("obsTimeLocal") ;   




select count(*)
from estaciones e ;

select id_estacion,count(*) as n_reportes_dato_lluvia_nulo
from reportes r 
where "precipTotal_mm" is null and dia_con_obs is true 
group by id_estacion ;

select *
from reportes r 
where r."precipTotal_mm" ;

group by id_estacion,fecha ,dia_con_obs 
intersect 
select id_estacion 
from reportes r 
where fecha = '2025-01-01'and id_estacion>139 and dia_con_obs=false 
group by id_estacion,fecha ,dia_con_obs 

/*
delete 
from reportes 
where id_estacion >139 and fecha = '2024-12-31'
*/

select *
from estaciones e 
order by id_estacion 
select *
from reportes r 
where id_estacion =140
order by fecha desc 
-- id_estacion > 139

select fecha,dia_con_obs 
from reportes r
where id_estacion =2 and fecha >= '2024-09-01'
group by fecha,dia_con_obs 
order by max("obsTimeLocal")  desc

-- verificación la actividad de las estaciones en el último tiempo
select id_estacion ,count(*) as q_dias_sin_reportes
from reportes r
where id_estacion > 140 and dia_con_obs=false
group by id_estacion 
order by q_dias_sin_reportes desc


DECLARE myvar integer;

select q_dias_sin_reporte := count(*)
from reportes r
where id_estacion = 274 and dia_con_obs=false

-----------------------------------------

select max(fecha)
from reportes r
where id_estacion = 274

select *
from reportes r 
where r.fecha =  '2024-01-09' and id_estacion =120;

select fecha,max("precipTotal_mm"),dia_con_obs 
from reportes r 
where id_estacion=42
group by fecha,dia_con_obs 
order by fecha ;


select fecha,max("precipTotal_mm")
from reportes r 
where fecha >= '2024-01-01' and  ("precipTotal_mm" <> 'NaN')
group by "fecha" 

select id_estacion ,fecha,max("precipTotal_mm")
from reportes r 
where fecha >= '2024-09-12'
group by id_estacion ,fecha 

select *
from reportes r 
where id_estacion =121 and fecha >= '2025-02-13' 


update reportes 
set "precipRate_mm_h"  = null 
where "precipRate_mm_h"  = 'NaN';
update reportes 
set "pressureMin_hPa"  = null 
where "pressureMin_hPa"  = 'NaN';
update reportes 
set "pressureTrend_hPa"  = null 
where "pressureTrend_hPa"  = 'NaN';

select inicio,count(*)
from estaciones e
where inicio > '2024-12-30'
group by inicio 
order by inicio
union
select 'antes 2024-12-30' as inicio,count(*)
from estaciones e
where inicio < '2024-12-30' ;

select "stationID" 
from estaciones e
where inicio = '2025-02-14'

alter table estaciones 
drop column ultimo_reporte;

/*
update estaciones set inicio ='2025-01-01'
where inicio = '2025-01-26';
*/

alter table reportes 
rename column "precipRate_mm" to "precipRate_mm_h";