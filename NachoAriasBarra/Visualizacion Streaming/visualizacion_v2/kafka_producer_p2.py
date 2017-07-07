from pykafka import KafkaClient
import random
from time import sleep
import sys, os
from datetime import datetime as dt

if __name__=="__main__":
    try:
        print("Initialization...")
        # producer = KafkaProducer(bootstrap_servers='172.20.1.21:9092')
        # producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')

        topic_name = sys.argv[1]
        filename = sys.argv[2]
        sleep_time = float(sys.argv[3])
        fecha_ini = sys.argv[4]
        fecha_fin = sys.argv[5]

        print("Sending messages to kafka " + topic_name + " topic...")

        # sleep_time = 0.1
        # fecha_ini = "1999-12"
        # fecha_fin = "2001-05"
        # filename = "final_data.csv"

        fecha_ini_year, fecha_ini_month = fecha_ini.split("-")
        fecha_fin_year, fecha_fin_month = fecha_fin.split("-")

        fecha_ini_dt = dt(int(fecha_ini_year), int(fecha_ini_month), 1)
        fecha_fin_dt = dt(int(fecha_fin_year), int(fecha_fin_month), 1)

        client = KafkaClient(hosts="127.0.0.1:9092")
        topic = client.topics[topic_name]
        producer = topic.get_sync_producer()
    
        f = open(filename, 'rt')
        try:
            for line in f:
                dic_data = {}
                line_list = line.split(",")
                dic_data["Date"] = line_list[0]
                dic_data["EEUU_DJI"] = line_list[1]
                dic_data["UK_LSE"] = line_list[2]
                dic_data["Spain_IBEX35"] = line_list[3]
                dic_data["Japan_N225"] = line_list[4]
                dic_data["EEUU_Unem"] = line_list[5]
                dic_data["UK_Unem"] = line_list[6]
                dic_data["Spain_Unem"] = line_list[7]
                dic_data["Japan_Unem"] = line_list[8][:-1]
                curr_year, curr_month = dic_data["Date"].split("-")
                curr_date = dt(int(curr_year), int(curr_month), 1)

                if curr_date > fecha_ini_dt and curr_date < fecha_fin_dt:
                    print(dic_data)
                    producer.produce(str(dic_data))
                    sleep(sleep_time)
                # sleep(random.uniform(float(low), float(high)))
        finally:
            f.close()
    
        # print("Waiting to complete delivery...")
        # producer.flush()
        # print("End")

    except KeyboardInterrupt:
        print('Interrupted from keyboard, shutdown')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
