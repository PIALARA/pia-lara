from pialara.db import db


class MongoModel:
    collection_name = None

    def __init__(self):
        self.db = db

    def find(self, params=None):
        return self.db[self.collection_name].find(params)

    def find_one(self, params=None):
        return self.db[self.collection_name].find_one(params)

    def update_one(self, mongo_filter, new_values, upsert=False):
        return self.db[self.collection_name].update_one(mongo_filter, new_values, upsert=upsert)

    def update_many(self, mongo_filter, new_values, upsert=False):
        return self.db[self.collection_name].update_many(mongo_filter, new_values, upsert=upsert)

    def insert_one(self, values):
        return self.db[self.collection_name].insert_one(values)

    def insert_many(self, values):
        return self.db[self.collection_name].insert_many(values)

    def delete_one(self, values):
        return self.db[self.collection_name].delete_one(values)

    def aggregate(self, values):
        return self.db[self.collection_name].aggregate(values)

    def count_documents(self, values):
        return self.db[self.collection_name].count_documents(values)

    def distinct(self, values, query):
        return self.db[self.collection_name].distinct(values, query)