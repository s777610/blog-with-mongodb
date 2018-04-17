import pymongo

class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod  # not using self
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["fullstack"]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data) #data=json

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query) #query={dict}

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)