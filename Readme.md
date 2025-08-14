# Aplicacion de geolocalizacion

**objetivos**: tener un listado de personas en un documento con su nombre y direccion donde vive. Cada personas reside en un barrio pero no tenemos una base de datos actualizada de cada persona donde vive. Para eso tenemos que tener delimitado los barrios en un área de coordenadas para poder usar un algoritmo de geolocalizacion y definir a través de el si la persona XXX vive en el barrio YY si el la dirección de su casa [un punto en un mapa] esta dentro del barrio[si el punto esta dentro del area "barrio YYY"]

### Herramientas

**nombre**: https://developer.mapquest.com
**que hace**: La podemos utilizar como google maps para medir distancia o viaje entre dos puntos
**para que la utilizaríamos?**: esto podríamos hacerlo para medir la distancia y el tiempo entre la direccion de una persona y el punto de destino para XX tarea que tenga que hacer la persona

**nombre**: https://geojson.io
**que hace**: Obtener coordinadas de un poligono sobre un mapa que determina el área que compone un barrio X
**para que la utilizaríamos?**: con esto nos podemos armar una base de datos de todos los barrios del conurbano
**ejemplo**: barrio san jose -> https://geojson.io/#map=14.21/-34.6766/-58.62475


### Scrtipt

**nombre**: generate_pers_barrio.py
**descripcion**: a partir de un json de personas y de barrios genero otro como resultado combinando la direccion de cada persona con el barrio de donde es a partir de la comparación de algoritmo de geolocalizacion usando principalmente las bibliotecas Poligon y Point

