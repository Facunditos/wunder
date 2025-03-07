from datetime import date,datetime
import pandas as pd
import random
import csv

def imprimir_mensaje(situacion:str,vieja_api_key:str=None,url:str=None,llamadas_totales:int=None,
    identificador_estacion:str=None,dia:date=None,status_code:int=None,n_error_con:int=None,problema=None)->None:
    """
    Imprime un mensaje según la situación 
    """
    
    #Se agotó el cupo de llamadas por api key
    if (situacion=='llamada 1400'):
        print(f'cambio de api key por llamada 1400. Vieja api key\n{vieja_api_key}')
    #La api key no tiene autorización
    elif (situacion=='api key desautorizada'):
        print(f'cambio de api key por problmeas de autorización.\nRespuesta:{status_code}.\nVieja api key\n{vieja_api_key}')
    #El servidor no responde
    elif (situacion=='el servidor no contesta'):
        print(f'Problemas con el servidor web.\nRespuesta:{status_code}.\nSe pausa durante una hora la ejecución.\nHora de pausa:{datetime.now()}')
    elif (situacion=='respesta del servidor desconocida'):
        print(f'Se obtuvo una respuesta desconocida.\nRespuesta:{status_code}.\nLlamado:{url}')
    elif (situacion=='error de conexión'):
        print(f'Hubo un problema con la conexión al servidor.\nError número:{n_error_con}.\nError:{problema}\nSe aguarda 1 minuto')
    #Se agotaron todas las api keys
    elif(situacion=='sin api keys'):
        print(f'se consumieron todas las api keys disponibles.\nÚltimo llamado:{url}.')
    #La estación registró 30 días consecutivos sin reportes
    elif(situacion=='cambio estacion'):
        print(f'se cargaron todas las observacines de {identificador_estacion}')
    elif(situacion=='fin ejecución'):
        print(f'Finalizó la ejecucución del programa.\nTotal de llamadas:{llamadas_totales}')

def cambiar_api_key(conjunto_api_key:list[str],api_key_actual:str)->str:
    """
    Recibe el lote de api keys y la api key que se está utilizando en las llamadas a la API. 
    Retorna la api key que le sigue a menos que se hayan consumidos todas api keys disponibles (retorna un str vacío)
    """
    indice_api_key_actual=conjunto_api_key.index(api_key_actual)
    if indice_api_key_actual==len(conjunto_api_key)-1:
        return ''
    else:
        siguiente_api_key=conjunto_api_key[indice_api_key_actual+1]
        return siguiente_api_key      

def obtener_api_keys()->list:
    """
    Retorna una lista de api keys para realizar llamadas a la API de Wunder
    """
    # Se crea un dataframe en base a la info de un excel que guarda las cuentas de wunder con las respectivas api keys
    df_cuentas_wunder=pd.read_excel('./info_wunder.xlsx','apiKeys',skiprows=2)
    api_keys=df_cuentas_wunder['apiKey']
    # Se crea una lista con las api keys
    api_keys=list(api_keys)
    api_keys_des = api_keys.copy()
    # Se desordenan las api keys para no empezar siempre por la misma. 
    random.shuffle(api_keys_des)
    return api_keys_des  

def escribirCSV(ruta:str,datos:list,header:list|tuple=None)->None:
    #Se elige el modo escritura(w) por lo que se sobreescribe el archivo
    with open(ruta,'w',newline='') as csv_file:
            writer = csv.writer(csv_file)
            if header : writer.writerow(header)
            writer.writerows(datos)
