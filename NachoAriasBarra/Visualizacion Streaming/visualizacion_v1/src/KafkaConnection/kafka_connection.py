# -*- coding: utf-8 -*-
from pykafka import KafkaClient
from pykafka.common import OffsetType

class KafkaConnection():
    
    def __init__(self, host = 'localhost', port = 9092, topic = 'parserOutput', offsetType = 'True'):
        self.host = host
        self.port = str(port)
        self.topic = topic
        self.offsetType = offsetType
        self.client = KafkaClient(hosts=self.host + ':' + self.port)
        self.topic = self.client.topics[self.topic]
        
    def init_Kafka_consumer(self):
        # client = KafkaClient(hosts=self.host + ':' + self.port)
        # topic = client.topics[self.topic]
        # consumer = self.topic.get_simple_consumer(auto_offset_reset=OffsetType.LATEST, reset_offset_on_start=self.offsetType, use_rdkafka=True)
        # consumer = self.topic.get_simple_consumer(auto_offset_reset=OffsetType.LATEST, reset_offset_on_start=self.offsetType)
        consumer = self.topic.get_simple_consumer()
        return consumer

    def init_Kafka_producer(self):
        # client = KafkaClient(hosts=self.host + ':' + self.port)
        # topic = client.topics[self.topic]
        producer = self.topic.get_sync_producer()
	    #producer = self.topic.get_producer(use_rdkafka=True)
        return producer

    def get_topic(self):
        return self.topic

