# 네이버 뉴스 인사이트
# from : 

import requests

# request api 요청
url = "https://openapi.naver.com/v1/search/news"
params = {'query' : '희귀질환'}
headers = {'X-Naver-Client-Id':'taH_0plC1S0PwAZzX4iJ','X-Naver-Client-Secret':'yLKRlYcavp'}
bodys = {
    "startDate" : "2014-01-01"
    ,"endDate" : "2024-02-23"
}
response = requests.get(url, params=params, headers=headers)

import json
contents = json.loads(response.content)

from pymongo import MongoClient
mongoclient = MongoClient("mongodb://192.168.10.236:27017")
database = mongoclient['skykim']
collection = database['rarediseasenews']

for i in range
result = collection.insert_many(contents['response']['body']['items'])


import os
import sys
import urllib.request #urllib.request 모듈 : URL을 열고 데이터를 읽는데 사용
client_id = "yBMUY635RhbcostPOfky"
client_secret = "aP6FMJ0JBn"
query = '희귀질환'

