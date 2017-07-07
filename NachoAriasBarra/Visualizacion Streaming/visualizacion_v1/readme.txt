################# El proyecto se ejcutará con python 2.7

################# Serán necesarias las siguientes librería:
	pykafka
	pymongo
	bokeh
	pandas

################# Estructura del proyecto (version con mongo)

	* data
		- datos_bolsa
			1) ^IBEX.csv
				1.1 Nombre: IBEX 35
				1.2 Fuente: https://finance.yahoo.com/quote/%5EIBEX/history?p=%5EIBEX
				1.3 Periodo: 31/12/1999 - 30/11-2016
				1.4 Moneda: Euros

			2) ^DJI.csv
				2.1 Nombre: Dow 30
				2.2 Fuente: https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI
				2.3 Periodo: 01/01/2000 - 01/12-2016
				2.4 Moneda: Dolares

			3) ^LSE.csv
				3.1 Nombre: London Stock Exchange Group plc
				3.2 Fuente: https://finance.yahoo.com/quote/LSE.L/history?period1=978303600&period2=1483138800&interval=1d&filter=history&frequency=1d
				3.3 Periodo: 31/07/2001 - 01/12-2016
				3.4 Moneda: Libras

			4) ^SSE.csv
				4.1 Nombre: SSE Composite Index (Shanghai)
				4.2 Fuente: https://es.finance.yahoo.com/quote/000001.SS/history?period1=946681200&period2=1483138800&interval=1mo&filter=history&frequency=1mo
				4.3 Periodo: 01/01/2000 - 31/12-2016
				4.4 Moneda: Divisa en CNY

			5) ^N255.csv
				5.1 Nombre: Nikkey 225
				5.2 Fuente: https://finance.yahoo.com/quote/%5EN225/history?period1=946681200&period2=1483138800&interval=1mo&filter=history&frequency=1mo
				5.3 Periodo: 31/01/2000 - 30/11-2016
				5.4 Moneda: Divisa en JPY
			6) processed
				6.1 csv_stockExchange_mixed: fichero de datos de bolsa procesados

		- datos_paro
			1) london
				1.1 series-040617.csv: fichero con datos de paro de Londres
				1.2 readme.txt
			2) japon
				2.1 jma_data.csv: fichero con datos de paro de Japón
				2.2 readme.txt
			3) espana
				3.1 4247.csv: fichero con datos de paro de España
				3.2 readme.txt
			4) eeuu
				4.1 SeriesReport-20170604132227_e518f3.csv: fichero con datos de paro de EEUU
				4.2 readme.txt
			5) processed
				5.1 csv_Unem_mixed: fichero de datos de paro procesados			
		- final_data
			1) csv_stockExchange_mixed: fichero con los datos de bolsa procesados
			2) csv_Unem_mixed: fichero con los datos de paro procesados
			3) final_data.csv: fichero con todos los datos procesados
	* docker
		- MongoDB: docker de la base de datos mongoDB
		- Spotify_Kafka: docker kafka
	* src
		- Ingest_and_sendDATA
			1) DDBBingest_sendData.py: script que además de insertar o eliminar ficheros de la base de datos, los envía para el streaming
		- KafkaConnection
			1) kafka_connection.py.py: script de clase para la conexión con kafka
		- mongoDBclass
			1) mongoDBclass.py: script de clase para las operacions con la base de datos
		- process_data
			1) process_data.py: script de clases para el preprocesado de los datos para conseguir un formato común
		- visualization
			1) bokeh_visualization.py: script de visualizacion en bokeh

################# Ejecución DEMO:

- Hay que tener en cuenta, que la ejecución de esta demo para y elimina todo tipo de dockers para realiar una ejecución limpia.
- Si en la primera ejecución de la demo, nos da un error con el broker de kafka, parar ejecución y volver a ejecutar.

1. Nos situamos en la carpeta src/Ingest_and_sendDATA y ejecutamos:
	* python DDBBingest_sendData.py ingest -> Para introducir los datos en la base de datos y empezar el streaming
	* python DDBBingest_sendData.py remove -> Para eliminar los datos de la base de datos
	* python DDBBingest_sendData.py  -> Para ejecutar el estreaming si los datos ya están en la base de datos

En caso de experimentar problemas con los docker, bajarse de nuevo los docker:
	- MongoDB
		sudo docker pull mongo
	- Kafka
		sudo docker pull spotify/kafka
