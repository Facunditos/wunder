create database wunder;
drop database wunder;

CREATE EXTENSION postgis;

drop table estaciones;
CREATE TABLE estaciones (
  id_estacion serial primary key,
  stationID varchar(20) NOT NULL,
  tz varchar(50),
  ubicacion geometry not null,
  inicio timestamp,
  comentario varchar(50),
  ult_reporte timestamp
) 

alter table estaciones
add constraint estacones_ubicacion_point_chk
    check(st_geometrytype(ubicacion) = 'ST_Point'::text);
    
   