from modelos import Reporte,Estacion
from sqlalchemy.engine import * # type: ignore
from sqlalchemy.orm import * # type: ignore
from sqlalchemy import * # type: ignore
import sqlalchemy
from datetime import date,timedelta,datetime
from funciones_grales import imprimir_mensaje,cambiar_api_key,obtener_api_keys
import requests # type: ignore
import time
import csv

def eliminar_reportes(session:sqlalchemy.orm.session.Session):
    with open('./ultima_fecha_carga_BD.txt','r') as csv:
        lines = csv.read()
        ultima_fecha = lines.rstrip('\n')
    stmt = delete(Reporte).where(Reporte.fecha==ultima_fecha)
    session.execute(stmt)
    ultima_fecha_lista = ultima_fecha.split('-')
    año = int(ultima_fecha_lista[0])
    mes = int(ultima_fecha_lista[1])
    dia = int(ultima_fecha_lista[2])
    return date(año,mes,dia)



def cargar_reportes(estacion:Estacion,reportes:list,dia:date,session:sqlalchemy.orm.session.Session)->list:
    """Crea la observación y la agrega a la estación. La observación incluye el campo id_estacion
    para respetar la constraint foreign key. También actualiza la fecha de la última obs en la tabla estación"""
    
    if (len(reportes)==0):
        objeto_obs = Reporte(
                id_estacion = estacion.id_estacion,
                obsTimeLocal=str(dia),
                fecha=str(dia),
                dia_con_obs= 0,
        )
        session.add(objeto_obs)
    else:
        for reporte in reportes:
            objeto_obs = Reporte(
                id_estacion = estacion.id_estacion,
                obsTimeLocal=reporte['obsTimeLocal'],
                fecha=str(dia),
                solarRadiationHigh_watts_m2= reporte['solarRadiationHigh'],
                uvHigh_indice= reporte['uvHigh'],
                winddirAvg_grado = reporte['winddirAvg'],
                humidityAvg_porcentaje = reporte['humidityAvg'],
                tempAvg_grados_C = reporte['metric']['tempAvg'],
                windspeedAvg_km_h = reporte['metric']['windspeedAvg'],
                windgustAvg_km_h = reporte['metric']['windgustAvg'],
                dewptAvg_grados_C = reporte['metric']['dewptAvg'],
                windchillAvg_indefinda = reporte['metric']['windchillAvg'],
                heatindexAvg_indefinda = reporte['metric']['heatindexAvg'],
                pressureMax_hPa = reporte['metric']['pressureMax'],
                pressureMin_hPa = reporte['metric']['pressureMin'],
                pressureTrend_hPa = reporte['metric']['pressureTrend'],
                precipRate_mm_h = reporte['metric']['precipRate'],
                precipTotal_mm = reporte['metric']['precipTotal'],
                dia_con_obs= 1,
            )
            session.add(objeto_obs)
                


def completar_reportes(fecha_hasta:str=datetime.now().date())->None:
    engine = create_engine('postgresql+psycopg2://postgres:facundo@localhost/wunder')
    engine.connect()
    claves_api = obtener_api_keys()
    numero_llamada_global=0
    numero_llamada_api_key=0
    #Seteo de variables
    api_key=claves_api[0]
    numero_error_conexion=0
    recurso=''
    with Session(engine) as session:
        fecha_desde = eliminar_reportes(session=session)    
        fecha_actual = datetime.now().date()
        estaciones = session.query(Estacion).all()
        for estacion_obj in estaciones:
            fecha = fecha_desde
            estacion_id=estacion_obj.stationID
            print('cargando estacion',estacion_id)
            while fecha<=fecha_hasta:
                if (numero_llamada_api_key==1400):
                        imprimir_mensaje(situacion='llamada 1400',vieja_api_key=api_key)
                        api_key=cambiar_api_key(conjunto_api_key=claves_api,api_key_actual=api_key)
                        #Si se agotaron las api keys se rompe el bucle white
                        if (api_key==''):
                            break
                        numero_llamada_api_key=0
                fecha_str = "{:04d}".format(fecha.year) + "{:02d}".format(fecha.month) + "{:02d}".format(fecha.day)
                if (fecha==fecha_actual):
                    recurso=f'https://api.weather.com/v2/pws/observations/all/1day?stationId={estacion_id}&format=json&units=m&apiKey={api_key}&numericPrecision=decimal'
                else:
                    recurso=f'https://api.weather.com/v2/pws/history/all?stationId={estacion_id}&format=json&units=m&apiKey={api_key}&numericPrecision=decimal&date={fecha_str}'
                try:
                    # Mandatoriamente se debe indicar un tiempo límite de espera para evitar que la llamada quede inconclusa por falta de respuesta de la API
                    respuesta = requests.get(recurso,timeout=60,headers={'Cache-Control': 'cache-control: max-age=599'})
                    codigo_respusta=respuesta.status_code
                    numero_llamada_api_key+=1
                    numero_llamada_global+=1
                    # Status Code 200: OK. The request has succeeded.
                    # Status Code 204: No Data Found for specific query. The 204 status code will have an empty response body.
                    if (codigo_respusta==200 or codigo_respusta==204):
                        observaciones_un_dia = respuesta.json()['observations'] if codigo_respusta==200 else []
                        #total_observaciones+=ORM_extraer_campos(IPREZ1,observaciones_un_dia,fecha,estacion_id,var_w)
                        cargar_reportes(estacion=estacion_obj,reportes=observaciones_un_dia,dia=fecha,session=session)
                        fecha+= timedelta(days=1)
                    elif (codigo_respusta==401):
                        # Status Code 401: Unauthorized. The request requires authentication.
                        imprimir_mensaje(situacion='api key desautorizada',status_code=codigo_respusta,vieja_api_key=api_key)
                        api_key=cambiar_api_key(conjunto_api_key=claves_api,api_key_actual=api_key)
                        #Si se agotaron las api keys se rompe el bucle white
                        if (api_key==''):
                            break
                        numero_llamada_api_key=0
                    elif (codigo_respusta==500):
                        imprimir_mensaje(situacion='el servidor no contesta',status_code=codigo_respusta)
                        una_hora=60*60
                        #Se pausa la ejecución para aguardar que normalicen el funcionamiento del servidor
                        time.sleep(una_hora)
                    else:
                        imprimir_mensaje(situacion='respesta del servidor desconocida',status_code=codigo_respusta,url=recurso)
                except requests.exceptions.RequestException as error:
                    numero_error_conexion+=1
                    imprimir_mensaje(situacion='error de conexión',n_error_con=numero_error_conexion,problema=error)
                    un_minuto=60
                    #Se pausa la ejecución para aguardar que normalicen el funcionamiento del servidor
                    time.sleep(un_minuto)
            #Sale del while y corroborra que se pueda pasar a la siguiente estación
            if (api_key==''):
                imprimir_mensaje(situacion='sin api keys',url=recurso)
                break
            else:
                imprimir_mensaje(situacion='cambio estacion',identificador_estacion=estacion_id)
        # Guarda todas las reportes extraídas, aún cuando el script no haya realizado todas las consultas que correspondían
        imprimir_mensaje(situacion='fin ejecución',llamadas_totales=numero_llamada_global)
        if api_key!='': 
            session.commit()     
            with open('./ultima_fecha_carga_BD.txt','w',newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([fecha_hasta])


fecha_limite = date(2024,12,31)
completar_reportes(fecha_hasta=fecha_limite)
