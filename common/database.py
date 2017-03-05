import pymongo

# setup a connection with mangoDB with the network address
#clien = pymongo.MongoClient(['localhost:27017'])
# choose the database is going to use
#DATABASE = clien['test1']
# insert, the content should be json format
# DATABASE['student'].insert({"name":"leo","age":"20"})
# remove
# DATABASE['student'].remove({"name":"leo"})

# create database class to encapsulate connection and aim database
class Database(object):
    URI = ['localhost:27017']
    DATABASE = None

    # using static method to implement functions that may used by other py part
    # those functions encapsulate database management methods
    @staticmethod
    def initialize():
        clien = pymongo.MongoClient(Database.URI)
        Database.DATABASE = clien['crawlerdb']

    @staticmethod
    def insert(collection, data):
        # data format should be JSON format
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        # return query results
        return  Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        # return one query result
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def remove(collection, query):
        return  Database.DATABASE[collection].remove(query)