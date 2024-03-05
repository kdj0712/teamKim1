# 네이버 뉴스 인사이트
# from : 

import requests

# request api 요청
url = "https://openapi.naver.com/v1/search/news"
params = {'query' : '희귀질환'
          ,'start' : 1
          ,'display' : 10
          ,"startDate" : "2023-01-01"
          ,"endDate" : "2024-02-23"}
headers = {'X-Naver-Client-Id':'ndxIQL5_LTtVAqPe562i','X-Naver-Client-Secret':'V5zNZYCxgr'}
bodys = {

}

import json

from pymongo import MongoClient
mongoclient = MongoClient("mongodb://192.168.10.236:27017")
database = mongoclient['skykim']
collection = database['rare_disease_news']
collection.delete_many({})

for page in range(1,17817):
    params['start'] = page
    response = requests.get(url, params=params, headers=headers)
    contents = json.loads(response.content) 
    collection.insert_many(contents['items'])
