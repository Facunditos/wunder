# Objetivo 
El objetivo del presente proyecto es la generación de una base de datos con registros hidrometeorológicos de aproximadamente 140 estaciones localizadas en el sur de la provincia de Santa Fe que se actualice diariamente de manera automática.
# Objetivos específicos 
- Diseñar la base de datos relacional
- Descargar datos históricos de las estaciones hidrometeorológicas de interés mediante web scraping y comunicación API-REST
- Insertar los datos históricos en la base de datos
- Automatizar la descarga diaria de los datos y su inserción en la base de datos
- Crear un archivo con los metadatos de cada estación meteorológica (fuente, período con información disponible, variables disponibles, datos del sensor, etc.)
- Vincular la base de datos a un Sistema de Información Geográfica (SIG) para poder ser consultados
# Metodología 
1. Desarrollo de algoritmos de web scraping con Python
2. Análisis de posibilidades técnicas para alojar la base de datos
3. Creación de la base de datos
4. Desarrollo de algoritmos de automatización de ETL (extracción, transformación y carga) de los datos
5. Vincular la base de datos con QGis
6. Elaboración de la documentación e informe final