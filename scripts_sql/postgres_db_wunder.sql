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


select *
from reportes r 
where r.fecha =  '2024-01-09' and id_estacion =120;