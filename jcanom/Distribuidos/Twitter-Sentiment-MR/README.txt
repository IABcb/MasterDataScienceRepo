README

1. Preparar servidor geolocalización.
1.1. Lanzar en EC2 el servidor "Geo photon".
1.2. Lanzar el servidor "java -jar geo_photon.jar" (necesaria clave jcano.pem).
1.3. Copiar la dirección IP del servidor a la variable 'url' del script "streaming_mapper.py".
2. Subir los ficheros "streaming_mapper.py" y "streaming_reducer.py" a un bucket S3.
3. Subir los el fichero de datos "tweets_es.json" a un bucket S3.
4. Lanzar clúster EMR.
4.1. Create cluster
4.2. Seleccionar "Step execution" y seleccionar "Streaming program" en Step type.
4.3. Configure.
	Name: Twitter analisys
	Mapper: Ruta del bucket S3 donde se guardó "streaming_mapper.py" en el paso 2.
	Reducer: Ruta del bucket S3 donde se guardó "streaming_reducer.py" en el paso 2.
	Input S3 location: Ruta del bucket S3 donde se guardó "tweets_es.json" en el paso 3.
	Output S3 location: Ruta del bucket S3 donde se quiere guardar la salida. NO DEBE EXISTIR!
4.4. Create cluster.

