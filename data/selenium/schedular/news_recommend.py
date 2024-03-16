# 몽고디비 연결
from pymongo import MongoClient

def dbconnect(collection) :
    mongoClient = MongoClient("mongodb://192.168.10.236:27017/")
    database = mongoClient["Seleniums"]
    collection = database[collection]
    return collection


