# from : https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15094089
import requests
import xml.etree.ElementTree as ET
from pymongo import MongoClient
import urllib.parse

# API 호출
def get_hosp_info():
    url = 'http://apis.data.go.kr/B551182/exclInstHospAsmInfoService/getExclInstHospAsmInfo?'
    raw_service_key = 'y5zk2Il3wqLeADyw4OnaRsn0CBXC7/FzuIGDg+V0pxfV8/4zQeYhESnXSRJ56xFG1HiQqU2MlxHIKpN1K7hDzA=='
    encoded_service_key = urllib.parse.quote(raw_service_key)
    params = {
        'numOfRows' : 20000,
        'page_num' : 1,
        'serviceKey': raw_service_key}
    response = requests.get(url, params=params)
    print(response.content)
    root = ET.fromstring(response.content)
    for item in root.findall('./body/items/'):
        # 예시: 'name' 태그와 'price' 태그의 텍스트를 가져옵니다.
        asmGrd = item.find('asmGrd').text
        asmGrdNm = item.find('asmGrdNm').text
        asmNm = item.find('asmNm').text
        yadmNm = item.find('yadmNm').text
        ykiho = item.find('ykiho').text
        collection.insert_one({'asmGrd': asmGrd
                               ,'asmGrdNm' : asmGrdNm
                               , 'asmNm' : asmNm
                                ,  'yadmNm': yadmNm
                                ,  'ykiho': ykiho})

from pymongo import MongoClient
def dbconnect(collection_name) :
    # MongoDB 클라이언트 설정 mongodb://localhost:27017
    mongoClient = MongoClient("mongodb://192.168.10.236:27017")
    database = mongoClient["teamkim"]
    collection = database[collection_name]
    return collection




collection = dbconnect('info_institution_good_hospital_info')

get_hosp_info()

# type(contents)
# # <class 'dict'>
# contents['header']
# # {'resultCode': '00', 'resultMsg': '정상'}
# type(contents['body']['items'])
# # <class 'list'>



