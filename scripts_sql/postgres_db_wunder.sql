--create database wunder;
--create EXTENSION postgis;

---------- peso de la base de datos y de sus tablas ----------------------------

select pg_size_pretty(
	pg_database_size('wunder')
) as peso_total;

select
  table_name,
  pg_size_pretty(pg_total_relation_size(quote_ident(table_name))),
  pg_total_relation_size(quote_ident(table_name))
from information_schema.tables
where table_schema = 'public'
order by 3 desc;


---------- Tabla estaciones ----------------------------

select count(*) as cantidad_estaciones
from estaciones e;

select *
from estaciones e
order by e.inicio;

select e.inicio,count(*) as cantidad_estaciones
from estaciones e 
where e.inicio >'2024-12-31'
group by e.inicio
order by e.inicio;

---------- Tabla reportes ----------------------------

select count(*) as cantidad_reportes
from reportes e;

select *
from reportes r;

select count(*)
from reportes 
where dia_con_obs is false

select *
from reportes 
where dia_con_obs is false
limit 20

---------- Reportes contemplando todas las estaciones ----------------------------

-- según rango días y región 

select e."stationID",e.geom,r."obsTimeLocal",r."precipTotal_mm" 
from estaciones e 
join reportes r 
on e.id_estacion = r.id_estacion 
where 
	r.fecha between '2025-02-04' and '2025-02-06'
	and 
	ST_Contains( 	
		-- se define una región para encontrar las estaciones localizadas en Firmat	
		ST_Polygon('LINESTRING(-61.37 -33.54, -61.58 -33.54, -61.58 -33.39, -61.37 -33.39, -61.37 -33.54)'::geometry, 4326),
		e.geom
	);

-- histórico región 

select e."stationID",e.geom,r."obsTimeLocal",r."precipTotal_mm" 
from estaciones e 
join reportes r 
on e.id_estacion = r.id_estacion 
where 
	ST_Contains(
	-- se define una región para encontrar las estaciones localizadas en Firmat	
	ST_Polygon('LINESTRING(-61.37 -33.54, -61.58 -33.54, -61.58 -33.39, -61.37 -33.39, -61.37 -33.54)'::geometry, 4326),
	e.geom
	);

-- según rango días

select e."stationID",e.geom,r."obsTimeLocal",r."precipTotal_mm" 
from estaciones e 
join reportes r 
on e.id_estacion = r.id_estacion 
where "fecha" between '2025-02-04' and '2025-02-05';

-- según día y horario

select e."stationID",e.geom,r."obsTimeLocal",r."precipTotal_mm" 
from estaciones e 
join reportes r 
on e.id_estacion = r.id_estacion 
where "obsTimeLocal" between '2025-02-05 10:00' and '2025-02-05 15:00';

---------- Reportes contemplando una única estación ----------------------------

-- según rango días

select e."stationID",e.geom,r."obsTimeLocal",r."precipTotal_mm" 
from estaciones e 
join reportes r 
on e.id_estacion = r.id_estacion 
where 
	e."stationID"  like 'IROSAR100'
	and
	r.fecha between '2025-02-04' and '2025-02-06';

-- histórico
select e."stationID",e.geom,r."obsTimeLocal",r."precipTotal_mm" 
from estaciones e 
join reportes r 
on e.id_estacion = r.id_estacion 
where 
	e."stationID"  like 'IROSAR100';

-- según día

select e."stationID",e.geom  ,r."obsTimeLocal",r."precipTotal_mm" 
from estaciones e 
join reportes r 
on e.id_estacion = r.id_estacion 
where e."stationID"  like 'IROSAR100' and r.fecha ='2025-02-05';

-- según día y horario

select e."stationID",e.geom  ,r."obsTimeLocal",r."precipTotal_mm" 
from estaciones e 
join reportes r 
on e.id_estacion = r.id_estacion 
where (e."stationID"  like 'IROSAR100') and 
	"obsTimeLocal" between '2025-02-05 10:00' and '2025-02-05 15:00';

---------- Mediana de la lluvia acumulada según día ----------------------------

SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY lluvia_acum_por_estacion)  
from (select max("precipTotal_mm") as lluvia_acum_por_estacion
from reportes r 
where fecha ='2025-02-05'
group by id_estacion); 


select max("precipTotal_mm") as lluvia_acum_por_estacion
from reportes r 
where fecha ='2025-02-05'
group by id_estacion
having max("precipTotal_mm") is not null
order by 1;

---------- Reinicio de la precipitación acumulada ----------------------------


select r.fecha ,max(r."precipTotal_mm") 
from estaciones e 
join reportes r 
on e.id_estacion = r.id_estacion 
where 
	e."stationID"  like 'ISANTAFE105'
	and
	r.fecha between '2024-11-01' and '2024-11-30'
	and 
	r."precipTotal_mm" >0
group by fecha;

select e."stationID",e.geom,r."obsTimeLocal",r."precipTotal_mm" 
from estaciones e 
join reportes r 
on e.id_estacion = r.id_estacion 
where 
	e."stationID"  like 'ISANTAFE105'
	and
	r.fecha between '2024-11-06' and '2024-11-07';

--drop table estaciones;
CREATE TABLE estaciones (
  id_estacion int primary key,
  stationID varchar(20) NOT NULL,
  tz varchar(50),
  ubicacion geometry,
  inicio timestamp,
  comentario varchar(50),
  ult_reporte timestamp
) 

--drop table reportes;

alter table estaciones
add constraint estacones_ubicacion_point_chk
    check(st_geometrytype(ubicacion) = 'ST_Point'::text);

select max(fecha)
from reportes r;

select count(*) 
from reportes r
where fecha < '2025-02-13';

select extract (year from (select max(fecha) from reportes r));

select count(*)
from estaciones e ;

select id_estacion,count(*) as n_reportes_dato_lluvia_nulo
from reportes r 
where "precipTotal_mm" is null and dia_con_obs is true 
group by id_estacion ;

select count(*) as n_reportes_dato_lluvia_nulo
from reportes r 
where "precipTotal_mm" is null and dia_con_obs is true;

select count(*) as n_reportes_dato_lluvia_nulo
from reportes r 
where "precipTotal_mm" is null and dia_con_obs is false;

select count(*) as n_reportes_dato_lluvia_nulo
from reportes r 
where "precipTotal_mm" is null;


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



/*
update estaciones set inicio ='2025-01-01'
where inicio = '2025-01-26';
*/

alter table reportes 
rename column "precipRate_mm" to "precipRate_mm_h";