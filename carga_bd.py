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


def eliminar_reportes(session:sqlalchemy.orm.session.Session)->date:
    """
    Recibe el objeto session. Consulta a la base de datos la última fecha cargada 
    para luego eliminar los reportes que tengan esta fecha. 
    Retorna dicha fecha.
    """
    resultado = session.execute(text('SELECT MAX(fecha) FROM reportes'))
    ultima_fecha_cargada = resultado.mappings().all()[0]['max']
    stmt = delete(Reporte).where(Reporte.fecha==ultima_fecha_cargada)
    session.execute(stmt)
    return ultima_fecha_cargada



def cargar_reportes(estacion:Estacion,reportes:list,dia:date,session:sqlalchemy.orm.session.Session)->list:
    """
    Recibe una estación, los reportes asociados a la estación, la fecha de consulta y el objeto session.
    Carga en el objeto session los reportes de la estación de la fecha consultada. 
    """
    # Si la lista de reportes está vacía significa que la estación no reportó en la fecha consultada. 
    if (len(reportes)==0):
        # Se agrega una única fila en la base de datos para la fecha consultada y se setea en false la columna dia_con_obs
        objeto_obs = Reporte(
                id_estacion = estacion.id_estacion,
                obsTimeLocal=str(dia),
                fecha=str(dia),
                dia_con_obs= 0,
        )
        session.add(objeto_obs)
    else:
        # Se agrega a la base de datos una fila por cada reporte emitido por la estación en la fecha consultada.
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
                


def completar_reportes()->None:
    """
    Actualiza los reportes cargados en la base de datos
    """
    # Crea el motor de base de datos para conectarse a la base de datos wunder.
    # Credenciales del cliente. Usuario: postgres | Contraseña: facundo. 
    engine = create_engine('postgresql+psycopg2://postgres:facundo@localhost/wunder')
    engine.connect()
    # Seteo de variables
    claves_api = obtener_api_keys()
    api_key=claves_api[0]
    numero_llamada_global=0
    numero_llamada_api_key=0
    numero_error_conexion=0
    numero_api_keys_inhabilitadas = 0
    recurso=''
    # Crea el objeto session 
    with Session(engine) as session:
        # fecha desde es igual a la última fecha cargada en la base de datos. Se elimina para evitar duplicados al actualizar
        fecha_desde = eliminar_reportes(session=session)    
        fecha_actual = date.today()
        dif_dias = (fecha_actual - fecha_desde).days
        if dif_dias <= 14:
            # Actualiza hasta la fecha corriente
            fecha_hasta = fecha_actual 
        else:
            # Carga los 14 días siguientes a la última fecha cargada
            fecha_hasta = fecha_desde + timedelta(days=14)

        estaciones = session.query(Estacion).all()
        inicio = time.time()
        # Se itera sobre cada estación 
        for estacion_obj in estaciones:
            fecha = fecha_desde
            estacion_id=estacion_obj.stationID
            print('cargando estacion',estacion_id)
            # El bucle se ejecuta hasta que la  fecha a actulizar supere a la fecha límite
            while fecha<=fecha_hasta:
                # Si limita el número de llamadas por api key para no sobrecargarlas (wunder permite 1500 llamadas por día por api key)
                if (numero_llamada_api_key==1400):
                        imprimir_mensaje(situacion='llamada 1400',vieja_api_key=api_key)
                        api_key=cambiar_api_key(conjunto_api_key=claves_api,api_key_actual=api_key)
                        #Si se agotaron las api keys se corta la ejecución de la función 
                        if (api_key==''):
                            imprimir_mensaje(situacion='sin api keys',url=recurso)
                            return 
                        numero_llamada_api_key=0
                fecha_str = "{:04d}".format(fecha.year) + "{:02d}".format(fecha.month) + "{:02d}".format(fecha.day)
                # Si la fecha a actulizar es igual a la fecha corriente debe cambiarse el endpoint de consulta porque el endpoint history/all no sirve para actualizar los reportes del día en curso (cachea la primer respuesta)
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
                        # Se convierte el json que contiene la respuesta de la api de wunder en un diccionario de python y se consulta la clave que contiene los reportes. Si la estación no reportó se crea una lista vacía. 
                        observaciones_un_dia = respuesta.json()['observations'] if codigo_respusta==200 else []
                        cargar_reportes(estacion=estacion_obj,reportes=observaciones_un_dia,dia=fecha,session=session)
                        fecha+= timedelta(days=1)
                    # Status Code 401: Unauthorized. The request requires authentication.
                    elif (codigo_respusta==401):
                        imprimir_mensaje(situacion='api key desautorizada',status_code=codigo_respusta,vieja_api_key=api_key)
                        numero_api_keys_inhabilitadas += 1
                        api_key=cambiar_api_key(conjunto_api_key=claves_api,api_key_actual=api_key)
                        #Si se agotaron las api keys se corta la ejecución de la función 
                        if (api_key==''):
                            imprimir_mensaje(situacion='sin api keys',url=recurso)
                            return 
                        numero_llamada_api_key=0
                    # Status Code 500: Internal server error. The server encountered an unexpected condition which prevented it from fulfilling the request.
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
                    # Se pausa la ejecución para luego restablecer la comunicación 
                    time.sleep(un_minuto)
            
            imprimir_mensaje(situacion='cambio estacion',identificador_estacion=estacion_id)

        # Salida del bucle for: ya se cargaron todos los reportes
        fin = time.time()
        tiempo_s = fin - inicio
        tiempo_m = int(tiempo_s // 60)
        tiempo_h = int(tiempo_m // 60)
        minutos_restantes = tiempo_m % 60
        tiempo_llamada_API_s = round(numero_llamada_global / tiempo_s,2)
        imprimir_mensaje(situacion='fin ejecución',llamadas_totales=numero_llamada_global)
        print(f'Cada llamada a la API consumió, en promedio, {tiempo_llamada_API_s} segundos')
        print(f'El tiempo consumido en la descarga de los reportes fue de {tiempo_h} hs y {minutos_restantes} minutos')
        print(f'Última fecha cargada en la base de datos: {fecha_hasta}')
        # Si se constata que al menos 20 api keys quedaron inhabilitadas se advierte sobre la necesidad de renovar el lote completo de api keys
        if numero_api_keys_inhabilitadas >= 20: print('Hay al menos 20 api keys que están inhabilitadas. Se aconseja renovar el lote completo de api keys')
        # Se ejecutan todas las sentencias ligadas a la base de datos: eliminación e inserción de reportes
        session.commit()     

completar_reportes()
