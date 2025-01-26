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
   

select "stationID" ,"geom",max("obsTimeLocal") as hora ,max("precipTotal_mm") as lluvia_acum
from estaciones as e
join reportes as r
on e.id_estacion = r.id_estacion
where "obsTimeLocal" between '2024-11-28' and '2024-11-29'
group by "stationID" ,"geom"
having ;   


select id_estacion ,max(fecha),max("obsTimeLocal")
from reportes r 
group by id_estacion 
where 

select fecha,dia_con_obs 
from reportes r
where id_estacion =2 and fecha >= '2024-09-01'
group by fecha,dia_con_obs 
order by max("obsTimeLocal")  desc

select *
from reportes r
where id_estacion =1 and fecha >= '2024-09-01'
order by fecha 


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
where id_estacion =3 and fecha >= '2024-09-09' 


update reportes 
set "precipRate_mm_h"  = null 
where "precipRate_mm_h"  = 'NaN';
update reportes 
set "pressureMin_hPa"  = null 
where "pressureMin_hPa"  = 'NaN';
update reportes 
set "pressureTrend_hPa"  = null 
where "pressureTrend_hPa"  = 'NaN';

select *
from estaciones e 
alter table estaciones 
drop column ultimo_reporte;

alter table reportes 
rename column "precipRate_mm" to "precipRate_mm_h";