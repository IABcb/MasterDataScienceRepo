from pymongo import MongoClient
import os
import sys
class mongo():
    def __init__(self, collections_list, ddbb_data_path, ddbb = 'visualization'):
        self.ddbb_data_path = ddbb_data_path
        os.system('sudo docker run --rm --name my-mongo -v ' +  self.ddbb_data_path + ':/data/db -it -d -p 27017:27017 mongo:latest')
        self.client = MongoClient()
        self.collections_list = collections_list
        self.db = self.client.ddbb
        self.collections = dict()

        if len(collections_list) > 0:
            for col in self.collections_list:
                self.collections[col] = self.db[col]

    def get_collections(self):
        return self.collections

    def insert_doc(self, collection, doc):
        print('Inserting doc')
        collection.insert(doc)

    def check_collection_docs(self, collection):
        for i in collection.find():
            print('The doc is: ')
            print(i)

    def count_collection_docs(self, collection):
        print('Items of collection')
        print(collection.count())

    def stop_rm_docker_mongo(self):
        os.system('sudo docker stop my-mongo; sudo docker rm my-mongo')

    def close_mongo_conex(self):
        self.client.close()

    def rm_doc_from_collection(self, collection, doc):
        collection.delete_one(doc)

    def rm_all_docs_collection(self, collection):
        collection.delete_many({})

    def rm_collection(self, collection):
        collection.drop()

    def create_data_structure(self, sources, coins, type, date):
        message_structure = dict()
        data_structure = dict()

        message_structure['Type'] = type
        message_structure['Date'] = date

        for stockExchange in coins.keys():
            data_structure[stockExchange] = dict()
            data_structure[stockExchange]['Coin'] = coins[stockExchange]
            data_structure[stockExchange]['Source'] = sources[stockExchange]
            data_structure[stockExchange]['Value'] = 'NA'

        message_structure['Data'] = data_structure

        return message_structure

