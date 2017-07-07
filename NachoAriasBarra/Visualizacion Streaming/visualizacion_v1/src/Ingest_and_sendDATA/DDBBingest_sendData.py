import sys
import os
import pymongo
import csv
import time
import pandas as pd
path_to_append = os.path.dirname(os.path.abspath(__file__)).replace("/Ingest_and_sendDATA", "")
sys.path.append(path_to_append)
from mongoDBclass.mongoDBclass import mongo as MGDB
from KafkaConnection.kafka_connection import KafkaConnection as KFK
import threading

def init_kafka_docker():
    print('Starting Kafka Broker...')
    curr_path = os.path.dirname(os.path.abspath(__file__)).replace("/src/Ingest_and_sendDATA", "/docker/Spotify_Kafka/")
    run_file = 'run.py'
    os.system('python ' + curr_path + run_file)
    time.sleep(5)

def stop_kafka():
    os.system('docker stop kafka; docker rm kafka')
    time.sleep(2)

def make_query(collection, index):
    print('New query')
    return collection.find_one({'Date': index})

def send_data2kafka(data_2send, producer):
    print('Sending data...')
    # producer.produce(bytes(data_2send))
    data_2send['Data']['Date'] = data_2send['Date']
    producer.produce(str(data_2send['Data']).replace("u'","u''").replace("u'",""))

def remove_data(mongoOBJ, collection):
    print('Removing...')
    mongoOBJ.rm_all_docs_collection(collection)
    mongoOBJ.count_collection_docs(collection)

def insert_data_intoMONGO(mongoOBJ, CSVinput_data, collection, type, sources, coins):
    docs = CSVinput_data.to_dict(orient='records')
    index_docs = list()
    for d in docs:
        date = d['Date']
        data_st = mongoOBJ.create_data_structure(sources, coins, type, date)
        for key_source in sources.keys():
            data_st['Data'][key_source]['Value'] = d[key_source]
        index_docs.append(data_st)

    collection.insert_many(index_docs)
    print('TYPE: ' + type)
    mongoOBJ.count_collection_docs(collection)

def update_index(curr_index, finish_index, finish_queries):

    if curr_index == finish_index:
        finish_queries = True
    else:
        # Stock index
        if curr_index.split('-')[1] == '12':
            month = '01'
            year = str(int(curr_index.split('-')[0]) + 1)
        else:
            month = str(int(curr_index.split('-')[1]) + 1)
            year = curr_index.split('-')[0]
            if len(month) == 1:
                month = '0' + month

        curr_index = str(year) + '-' + str(month)
    print(curr_index)
    return curr_index, finish_queries

def init_visualization():
    print('Starting visualization...')
    vis_path = os.path.dirname(os.path.abspath(__file__)).replace('/Ingest_and_sendDATA','/visualization/')
    os.system('bokeh serve --show ' + vis_path + 'bokeh_visualization.py')


if __name__ == "__main__":

    # Removing previous dockers...
    # Stop all containers
    print('Removing previous containers...')
    os.system('sudo docker stop $(sudo docker ps -a -q)')
    # Remove all stopped containers
    os.system('sudo docker rm $(sudo docker ps -a -q)')

    time.sleep(3)

    # Mongo Docker Set up
    ddbb_data_path = os.path.dirname(os.path.abspath(__file__)).replace('src/Ingest_and_sendDATA', 'docker/MongoDB/data')


    collections_list = ['stockExchange', 'unemployment']
    mongoOBJ = MGDB(collections_list, ddbb_data_path)
    collections = mongoOBJ.get_collections()
    # Stock Exchange Data
    sources = {'IBEX35': 'Spain',
               'DJI': 'EEUU',
               'LSE': 'London',
               'N225': 'Japan'}

    coins = {'IBEX35': 'Euros',
             'DJI': 'Dollars',
             'LSE': 'Pounds',
             'N225': 'Yens'}

    # Kafka config
    kafka_ip = 'localhost'
    kafka_port = 9092

    # Query parameters
    time_to_query = 0

    if len(sys.argv) == 2:
        if sys.argv[1] == 'ingest':
            # Read Mixed CSVS
            sep = ','
            columnames = ['Date', 'DJI', 'LSE', 'IBEX35', 'N225']

            stockExchangePath = os.path.dirname(os.path.abspath(__file__)).replace('src/Ingest_and_sendDATA', 'data/datos_bolsa/processed/csv_stockExchange_mixed')
            unemploymentPath  = os.path.dirname(os.path.abspath(__file__)).replace('src/Ingest_and_sendDATA', 'data/datos_paro/processed/csv_Unem_mixed')

            stockExchangeData = pd.read_csv(stockExchangePath, sep=sep, names=columnames, header = 0)
            unemploymentData = pd.read_csv(unemploymentPath, sep=sep, names=columnames, header = 0)

            # Insert CSV Stock Exchange to mongo
            type = 'stockExchange'
            insert_data_intoMONGO(mongoOBJ, stockExchangeData, collections['stockExchange'], type, sources, coins)

            # Insert CSV Unemployment to mongo
            type = 'unemployment'
            insert_data_intoMONGO(mongoOBJ, unemploymentData, collections['unemployment'], type, sources, coins)

        elif sys.argv[1] == 'remove':
            # Remove data, if needed
            remove_data(mongoOBJ, collections['stockExchange'])
            remove_data(mongoOBJ, collections['unemployment'])
            sys.exit()

    #  Send data


    try:

        # Kafka
        init_kafka_docker()
        kafkaObj_stockExchange = KFK(host = kafka_ip, port = kafka_port, topic = 'stockExchange')
        producer_stock = kafkaObj_stockExchange.init_Kafka_producer()

        kafkaObj_unemployment = KFK(host = kafka_ip, port = kafka_port, topic = 'unemployment')
        producer_unem = kafkaObj_unemployment.init_Kafka_producer()

        init_stock_index = '2000-01'
        init_unem_index = '2000-01'

        finish_stock_index = '2016-11'
        finish_unem_index = '2016-11'

        curr_stock_index = init_stock_index
        curr_unem_index = init_unem_index
        finish_queries = False
        response_stock = None
        response_unem = None

        started_vis = False
        while not finish_queries:
            # Query maker
            response_stock = make_query(collections['stockExchange'], curr_stock_index)
            response_unem = make_query(collections['unemployment'], curr_unem_index)

            curr_stock_index, finish_queries = \
                update_index(curr_stock_index, finish_stock_index, finish_queries)

            curr_unem_index, finish_queries = \
                update_index(curr_unem_index, finish_unem_index, finish_queries)

            print('\nResponse from stock exchange')
            print(response_stock)
            print('\nResponse from unemployment')
            print(response_unem)

            # Send extracted data
            send_data2kafka(response_stock, producer_stock)
            send_data2kafka(response_unem, producer_unem)

            # Time to next query
            time.sleep(time_to_query)

            if not started_vis:
                # Init visualization
                t = threading.Thread(target=init_visualization)
                t.start()

                time.sleep(5)
                started_vis = True

        stop_kafka()
        mongoOBJ.close_mongo_conex()
        mongoOBJ.stop_rm_docker_mongo()
        t.join()
    except KeyboardInterrupt:
        stop_kafka()
        mongoOBJ.close_mongo_conex()
        mongoOBJ.stop_rm_docker_mongo()

