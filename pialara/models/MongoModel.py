from pialara.db import db

class MongoModel:

    collection_name = None

    def __init__(self):
        self.db = db

    def find(self, params=None):
        return self.db[self.collection_name].find(params)
