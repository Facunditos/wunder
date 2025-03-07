from modelos import Reporte,Estacion
from sqlalchemy.engine import * # type: ignore
from sqlalchemy.orm import * # type: ignore
from sqlalchemy import * # type: ignore
import sqlalchemy
from datetime import date,timedelta,datetime
from funciones_grales import imprimir_mensaje,cambiar_api_key,obtener_api_keys,escribirCSV
import requests # type: ignore
import time
import csv
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

engine = create_engine('postgresql+psycopg2://postgres:facundo@localhost/wunder')
engine.connect()

def buscar_estaciones_rectangulo()->list[tuple]:
    """
    Busca estaciones cercanas a los coordenadas contenidas en un rectángulo que contiene al polígono irregular de interés
    """
    #Seteo de variables
    numero_llamada_global=0
    numero_llamada_api_key=0
    coordenadas_sin_consultar = []
    claves_api = obtener_api_keys()
    api_key=claves_api[0]
    numero_error_conexion=0
    recurso=''
    stationsID = []
    estaciones = []
    # Lee el archivo que almacena las coordenadas ubicas dentro del rectángulo
    coordenadas_df = pd.read_csv('./busqueda_estaciones/puntos_rectangulo.txt')
    for idx,coor in coordenadas_df.iterrows():
        if (numero_llamada_api_key==1400):
            imprimir_mensaje(situacion='llamada 1400',vieja_api_key=api_key)
            api_key=cambiar_api_key(conjunto_api_key=claves_api,api_key_actual=api_key)
            #Si se agotaron las api keys se rompe el bucle white
            if (api_key==''):
                print(f'indice coordenada consultada: {idx}')
                imprimir_mensaje(situacion='sin api keys',url=recurso)
                return []
            numero_llamada_api_key=0
        lat = coor.loc['lat']
        lon = coor.loc['lon']
        # El endpoint devuelve las estaciones más cercanas a la coordenada pasada como query, por lo general es 10 el número de estaciones devueltas.
        recurso=f'https://api.weather.com/v3/location/near?geocode={lat},{lon}&product=pws&format=json&apiKey={api_key}'
        # Se crea este bucle while para garantizar que se va a realizar la llamada sobre la coordenada que se está iterando
        while True:
            try:
                # Mandatoriamente se debe indicar un tiempo límite de espera para evitar que la llamada quede inconclusa por falta de respuesta de la API
                respuesta = requests.get(recurso,timeout=60,headers={'Cache-Control': 'cache-control: max-age=599'})
                codigo_respusta=respuesta.status_code
                numero_llamada_api_key+=1
                numero_llamada_global+=1
                # Status Code 200: OK. The request has succeeded.
                # Status Code 204: No Data Found for specific query. The 204 status code will have an empty response body.
                if (codigo_respusta==200):
                    estaciones_cercanas = respuesta.json()['location']
                    for i,est_carcana_stationID in enumerate(estaciones_cercanas['stationId']):
                            # Se corroborra que la estación cercana no se haya recuperado en una consulta anterior
                            if (est_carcana_stationID not in stationsID):
                                stationsID.append(est_carcana_stationID)
                                est_cercana_latitud = estaciones_cercanas['latitude'][i]
                                est_cercana_longitud = estaciones_cercanas['longitude'][i]
                                # Se crea una tupla con el id de la estación, su latitud y su longitud
                                est_datos = est_carcana_stationID,est_cercana_latitud,est_cercana_longitud
                                estaciones.append(est_datos)
                            else:
                                continue
                    # Luego que se analizaron todas las estaciones próximas a la coordenada sobre la que se está iterando, se sale del bucle while para avanzar con la siguiente coordenada.
                    break        
                elif (codigo_respusta==401):
                    # Status Code 401: Unauthorized. The request requires authentication.
                    imprimir_mensaje(situacion='api key desautorizada',status_code=codigo_respusta,vieja_api_key=api_key)
                    api_key=cambiar_api_key(conjunto_api_key=claves_api,api_key_actual=api_key)
                    #Si se agotaron las api keys se retorna una lista vacía
                    if (api_key==''):
                        print(f'indice coordenada consultada: {idx}')
                        imprimir_mensaje(situacion='sin api keys',url=recurso)
                        return []
                    numero_llamada_api_key=0
                elif (codigo_respusta==500):
                    imprimir_mensaje(situacion='el servidor no contesta',status_code=codigo_respusta)
                    una_hora=60*60
                    #Se pausa la ejecución para aguardar que normalicen el funcionamiento del servidor
                    time.sleep(una_hora)
                else:
                    # A veces error 404 "The resource requested could not be located. Please verify the URL and try again later."
                    imprimir_mensaje(situacion='respesta del servidor desconocida',status_code=codigo_respusta,url=recurso)
                    coordenadas_sin_consultar.append(coor) # Se guarda la coordenada que no pudo ser consultada
                    break # Se continua con la siguiente coordenada
            except requests.exceptions.RequestException as error:
                numero_error_conexion+=1
                imprimir_mensaje(situacion='error de conexión',n_error_con=numero_error_conexion,problema=error)
                un_minuto=60
                #Se pausa la ejecución para aguardar que normalicen el funcionamiento del servidor
                time.sleep(un_minuto)
        
    imprimir_mensaje(situacion='fin ejecución',llamadas_totales=numero_llamada_global)
    print(coordenadas_sin_consultar)
    print(f'se encontraron {len(estaciones)} estaciones en el rectángulo')
    return estaciones
 

def buscar_estaciones_poligono_irregular(estaciones:list[tuple])->list[tuple]:
    #Leer el archivo KMZ
    kmz_path = "./busqueda_estaciones/poligono_cuencas.kmz"
    poligono = gpd.read_file(f"/vsizip/{kmz_path}")

    # Asegurarse de que está en WGS84
    poligono = poligono.to_crs("EPSG:4326")
    poligono_unico = poligono.unary_union

    # A partir de la lista de estaciones se crea un GeoDataFrame
    stationsId = []
    latitudes = []
    longitudes = []
    for stationId,lat,lon in estaciones:
        stationsId.append(stationId)
        latitudes.append(lat)
        longitudes.append(lon)
    df = pd.DataFrame({
        'stationId':stationsId,
        'lat':latitudes,
        'lon':longitudes,
    })

    # Crear una columna de geometría a partir de latitud y longitud
    gdf = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df['lon'], df['lat'])], crs="EPSG:4326")
    
    # Filtrar los puntos dentro del polígono
    puntos_dentro = gdf[gdf.geometry.within(poligono_unico)]

    estaciones_filtradas = [estacion for estacion in estaciones if estacion[0] in puntos_dentro['stationId'].to_list()]
    print(f'se encontraron {len(estaciones_filtradas)} estaciones en el polígono irregular')
    return estaciones_filtradas

def buscar_estaciones_nuevas(estaciones:list[tuple])->list[tuple]:
    with Session(engine) as session:
        estaciones_BD = session.query(Estacion).all()
    estaciones_BD_stationID = [estacion.stationID for estacion in estaciones_BD]
    estaciones_filtradas = [estacion for estacion in estaciones if estacion[0] not in estaciones_BD_stationID]
    print(f'se encontraron {len(estaciones_filtradas)} que no estaban en la base de datos')
    return estaciones_filtradas
    

def buscar_estaciones_activas(estaciones:list[tuple])->list:
    numero_error_conexion=0
    claves_api = obtener_api_keys()
    api_key=claves_api[0]
    estaciones_filtradas = []
    for estacion in estaciones:  
        stationId = estacion[0]
        recurso=f'https://api.weather.com/v2/pws/dailysummary/7day?stationId={stationId}&format=json&units=m&apiKey={api_key}&numericPrecision=decimal'
        try: 
            # Mandatoriamente se debe indicar un tiempo límite de espera para evitar que la llamada quede inconclusa por falta de respuesta de la API
            respuesta = requests.get(recurso,timeout=60,headers={'Cache-Control': 'cache-control: max-age=599'})
            codigo_respusta=respuesta.status_code
            # Status Code 200: OK. The request has succeeded.
            # Status Code 204: No Data Found for specific query. The 204 status code will have an empty response body.
            if (codigo_respusta==200 or codigo_respusta==204):
                resumen_ultima_semana = respuesta.json()["summaries"] if codigo_respusta==200 else []
                if resumen_ultima_semana != []: estaciones_filtradas.append(estacion)
            elif (codigo_respusta==401):
                # Status Code 401: Unauthorized. The request requires authentication.
                imprimir_mensaje(situacion='api key desautorizada',status_code=codigo_respusta,vieja_api_key=api_key)
                api_key=cambiar_api_key(conjunto_api_key=claves_api,api_key_actual=api_key)
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
    print(f'se encontraron {len(estaciones_filtradas)} estaciones activas (enviaron al menos un reporte en la última semana)')
    return estaciones_filtradas

def insertar_estaciones_activas(estaciones):
    with Session(engine) as session:
        # La fech de inicio de las nuevas estaciones se corresponde con la última fecha cargada en la base de datos
        resultado = session.execute(text('SELECT MAX(fecha) FROM reportes'))
        ultima_fecha = resultado.mappings().all()[0]['max'] 
        for stationId,latitud,longitud in estaciones:
            #Creo el objetos_nu de la clase estación.
            # Tengo que imputar None a los faltantes para no tener problemas luego en la inserción de las estaciones.
            # Tipos de faltantes. np.nan | np.float(nan) | pandas._libs.tslibs.nattype.NaTType -> dan errores en la inserción
            lon = str(longitud)
            lat = str(latitud)
            geom = f'SRID=4326;POINT({lon} {lat})'
            inicio = ultima_fecha
            obj_estacion = Estacion(
                stationID= stationId,
                geom= geom,
                inicio= inicio,
                comentario= 'el inicio indica la fecha desde la cual comenzó a buscarse los reportes de esta estación',
            )
            session.add(obj_estacion)
        session.commit()
        print('se agregagaros todas las estaciones activas a la base de datos')

def clasificar_estaciones():
    estaciones_clasificacion = []
    [estaciones_clasificacion.append(estacion+('activa',)) for estacion in estaciones_activas]
    [estaciones_clasificacion.append(estacion+('inactiva',)) for estacion in estaciones_nuevas if estacion not in estaciones_activas]
    [estaciones_clasificacion.append(estacion+('bd',)) for estacion in estaciones_poligono_irregular if estacion not in estaciones_nuevas]
    [estaciones_clasificacion.append(estacion+('afuera',)) for estacion in estaciones_rectangulo if estacion not in estaciones_poligono_irregular]
    fecha = str(date.today()).replace('-','_')
    encabezado = ('stationId','lat','lon','categoria')
    escribirCSV(ruta=f'./busqueda_estaciones/estaciones_encontradas_clasificacion_{fecha}.csv',datos=estaciones_clasificacion,header=encabezado)

estaciones_rectangulo = buscar_estaciones_rectangulo()
estaciones_poligono_irregular = buscar_estaciones_poligono_irregular(estaciones_rectangulo)
estaciones_nuevas = buscar_estaciones_nuevas(estaciones_poligono_irregular)
estaciones_activas = buscar_estaciones_activas(estaciones_nuevas)
insertar_estaciones_activas(estaciones_activas)
clasificar_estaciones()

