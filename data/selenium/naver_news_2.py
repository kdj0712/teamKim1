import os
import sys
import urllib.request
import json
import pandas as pd

def getresult(client_id,client_secret,query,display=10,start=1,sort='sim'):
    encText = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/news?query=" + encText + \
    "&display=" + str(display) + "&start=" + str(start) + "&sort=" + sort   

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_json = json.loads(response_body)
    else:
        print("Error Code:" + rescode)

    return pd.DataFrame(response_json['items'])

client_id = "yBMUY635RhbcostPOfky"
client_secret = "aP6FMJ0JBn"
query = '희귀질환'
display=100
start=1
#sort='sim'
sort='date'

result_all=pd.DataFrame()
for i in range(0,3):
    start= 1 + 100*i
    result= getresult(client_id,client_secret,query,display,start,sort)
    
    result_all=pd.concat([result_all,result])


result_all=result_all.reset_index() # index가 100단위로 중복되는것을 초기화
result_all=result_all.drop('index',axis=1) # reset_index후 생기는 이전 index의 column을 삭제
result_all['pubDate']=result_all['pubDate'].astype('datetime64[ns]') # pubDate의 타입을 object에서 datetime으로 변경
result_all['Date'] = result_all['pubDate'].dt.strftime('%Y%m%d')#날짜별 집계를 위해 'YYYYmmdd' 타입의 column을 생성

result_gr=result_all[['Date','title']].groupby(['Date']).count()
result_gr