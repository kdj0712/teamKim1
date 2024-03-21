# 몽고디비 연결
from pymongo import MongoClient
import pickle
import os

def dbconnect(Database_name, collection_name) :
    mongoClient = MongoClient("mongodb://192.168.10.236:27017/")
    database = mongoClient[Database_name]
    collection = database[collection_name]
    return collection


def update_news_trend_collection():
    news_weekly_collection = dbconnect("Seleniums", "bosa_news_weekly")
    news_collection = dbconnect("teamkim", "trend_news_test")
    
    # weekly 에 있는 내용 가지고 오기
    cursor = news_weekly_collection.find({})

    
    file_path = os.path.join(os.getcwd(), 'data', 'pkl', 'news_recommend_vectorizer.pkl')
    with open(file_path, "rb") as file:
        vectorizer = pickle.load(file)

    with open(os.path.join('data', 'pkl', 'news_recommend_model.pkl'), "rb") as file:
        model = pickle.load(file)

    for document in cursor :
        news_title = document.get('news_title')
        news_topic = model.predict(vectorizer.transform([news_title]))
        document['news_topic'] = news_topic
        news_collection.insert_one(document)

    # news_trend_collection에 내용 추가하기


if __name__ == "__main__" :
    update_news_trend_collection()