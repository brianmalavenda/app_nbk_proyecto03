# Aplicacion de geolocalizacion

**objetivos**: tener un listado de personas en un documento con su nombre y direccion donde vive. Cada personas reside en un barrio pero no tenemos una base de datos actualizada de cada persona donde vive. Para eso tenemos que tener delimitado los barrios en un área de coordenadas para poder usar un algoritmo de geolocalizacion y definir a través de el si la persona XXX vive en el barrio YY si el la dirección de su casa [un punto en un mapa] esta dentro del barrio[si el punto esta dentro del area "barrio YYY"]
Entidades principales del modelo: [Personas], [Barrios], [Escuelas]

### Herramientas

**repositorio base**: https://github.com/datosgobar/georef-ar-api
**descripcion**: https://datosgobar.github.io/georef-ar-api/georef-api-development/

**curso python**: https://www.youtube.com/watch?v=TkN2i-_4N4g

**nombre**: https://developer.mapquest.com
**que hace**: La podemos utilizar como google maps para medir distancia o viaje entre dos puntos
**para que la utilizaríamos?**: esto podríamos hacerlo para medir la distancia y el tiempo entre la direccion de una persona y el punto de destino para XX tarea que tenga que hacer la persona

**nombre**: https://geojson.io
**que hace**: Obtener coordinadas de un poligono sobre un mapa que determina el área que compone un barrio X
**para que la utilizaríamos?**: con esto nos podemos armar una base de datos de todos los barrios del conurbano
**ejemplo**: barrio san jose -> https://geojson.io/#map=14.21/-34.6766/-58.62475

**nombre**: https://mapaescolar.abc.gob.ar/mapaescolar
**que hace**: se puede obtener a partir de distintos filtros, las instituciones educativas por nivel educativo, predios, distincion entre privados y publicos y todo eso exportable en formato geojson
**para que la utilizaríamos?**: con esto tenemos la ubicacion de cada escuela publica que son los lugares donde se vota en las elecciones
**ejemplo**: predios educativos -> https://mapaescolar.abc.gob.ar/mapaescolar/#map=14.5/-58.633918486371144/-34.676976093036934/0/0,5/0a131c2a-ac99-4300-8925-9a40fdac9b16

**nombre**: https://epsg.io
**que hace**: api de transformacion de coordenadas geograficas
**ejemplo**: de lon-lat a coordenadas UTM: https://epsg.io/transform#s_srs=4326&t_srs=3857&x=-58.0000000&y=-34.0000000

#### Repositorios ejemplo

**nombre**: OpenDataCordoba
**url**: https://github.com/OpenDataCordoba/barrios/blob/main/caba_comunas.geojson
**que hace**: tiene barrios definidos de cordoba


## Bibliotecas o Librerías

**nombre**: https://www.elastic.co/docs
**descripcion**: para trabajar con consultas a archivos largos y obtimizar una busqueda

**nombre**: https://www.digitalocean.com/community/
**descripcion**: para trabajar con docker


### Scrtipt

**nombre**: generate_pers_barrio.py
**descripcion**: a partir de un json de personas y de barrios genero otro como resultado combinando la direccion de cada persona con el barrio de donde es a partir de la comparación de algoritmo de geolocalizacion usando principalmente las bibliotecas Poligon y Point

**nombre**: app.py
**descripcion**: a partir de un json de personas que cargo en un elemento select en un template de html obtengo a partir de cada persona seleccionada de que barrio es. Cuando selecciono una persona se activa el script que hace un request a una ruta de mi server con el parametro del id de la persona seleccionada y obtengo su barrio.


## Continuidad de proyecto
**objetivo**: generar una base de datos de geolocalizaciones de todas las instituciones educativas en el conurbano. Generar otro script que escale el anterior para además de agregar el barrio a cada persona, agregue el barrio a cada institucion. Combinar las tres entidades principales del proyecto en una sola base de conocimiento donde partir de las tres fuente separadas [Personas], [Barrios], [Escuelas] => [Personas(nombre,direccion,barrio,escuela)], -la escuela hace referencia donde vota-
