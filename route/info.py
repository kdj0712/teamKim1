from fastapi import APIRouter, FastAPI, Form, Depends, Query, HTTPException, Request
from typing import Optional
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aiohttp import ClientSession
from pydantic import BaseModel
from dotenv import load_dotenv
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google.cloud import storage
import pandas as pd
import pickle
load_dotenv()
import os
api_key = os.getenv("API_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/teamKim/macro-atom-415806-fd4035d471e1.json"
router = APIRouter()

from fastapi.staticfiles import StaticFiles
router.mount("/data/csv", StaticFiles(directory="data/csv/"), name="static_csv")

from database.connection import Database
from models.info_rarediseases import diseases
collection_disease = Database(diseases)

from models.institution import Institutions
collection_institution = Database(Institutions)

from models.trend_news import news_trends
collection_trend = Database(news_trends)

from models.academicinfo import academicinfo
collection_academicinfo = Database(academicinfo)

templates = Jinja2Templates(directory="templates/")
### 검색 모델 적용 조건---------------------------------------------------------------------------------------
def load_pickle_from_gcs(bucket_name, file_name):
    """Google Cloud Storage에서 피클 파일을 로드합니다."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    pickle_data = blob.download_as_bytes()
    return pickle.loads(pickle_data)
bucket_name = 'savehomes'
file_name = 'search_symptoms.pkl'
# vectorizer = load_pickle_from_gcs(bucket_name, file_name)

with open('data/pkl/vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

with open('data/pkl/tfidf_matrix_symptoms.pkl', 'rb') as file:
    tfidf_matrix_symptoms = pickle.load(file)
df1 = pd.read_csv('data/csv/df1.csv')

def predict_disease(search_word):
    """주어진 검색어에 대해 유사도가 높은 상위 질병을 반환합니다."""
    # 검색어 텍스트를 TF-IDF 벡터로 변환합니다.
    tfidf_vector = vectorizer.transform([search_word])
    # 각 질병에 대한 증상 벡터와의 코사인 유사도를 계산합니다.
    cosine_similarities = cosine_similarity(tfidf_vector, tfidf_matrix_symptoms)
    # 유사도와 질병 인덱스를 함께 저장합니다.
    disease_similarities = list(zip(cosine_similarities[0], range(len(df1))))
    # 유사도가 70% 이상인 질병을 찾습니다.
    similar_diseases = [index for similarity, index in disease_similarities if similarity > 0.7]
    # 유사도가 높은 순서대로 정렬합니다.
    similar_diseases.sort(key=lambda x: -disease_similarities[x][0])
    # 유사도가 높은 상위 질병의 이름을 반환합니다.
    disease_names = [df1['disease_korean_title'].iloc[i] for i in similar_diseases]
    # 중복된 질병 이름을 제거합니다.
    unique_disease_names = list(set(disease_names))
    # 유사도가 높은 상위 질병을 반환합니다.
    return unique_disease_names[:min(100, len(unique_disease_names))]


#### -------------------------------------------------------------------------------------------------------


# 희귀질환정보검색
# @router.post("/info_raredisease", response_class=HTMLResponse) 
# async def raredisease(request:Request):
#     return templates.TemplateResponse(name="search/search_raredisease.html", context={'request':request})
@router.post("/info_raredisease", response_class=HTMLResponse) 
@router.get("/info_raredisease/{page_number}")
@router.get("/info_raredisease")
async def disease_list(request: Request, page_number: int = 1, key_name: Optional[str] = Query(None), search_word: Optional[str] = Query(None)):
    await request.form()
    conditions = {}
    key_name = request.query_params.get('key_name')
    search_word = request.query_params.get('search_word')
    if key_name and search_word:
        # 검색 조건을 기반으로 질환을 필터링하는 로직
        if key_name == 'dise_name_kr': # 희귀질환명으로 검색하는 로직
            conditions.update({ 'dise_name_kr': { '$regex': search_word }})
        elif key_name == 'dise_KCD_code':  # KCD코드를 검색하는 로직
            conditions.update({ 'dise_KCD_code': { '$regex': search_word }})
        elif key_name == 'dise_spc_code': #spc코드를 검색하는 로직
            conditions.update({ 'dise_spc_code': { '$regex': search_word }})
        elif key_name == 'dise_symptoms': #증상명으로 검색하는 로직
            similar_diseases_names = predict_disease(search_word)  # 유사 질병 이름을 얻습니다.
            conditions.update({'dise_name_kr': {'$in': similar_diseases_names}})
        try:
            dise_list, pagination = await collection_disease.getsbyconditionswithpagination(conditions, page_number)
            return templates.TemplateResponse(
                name="/info/info_raredisease.html",
                context={'request': request, 'dise_list': dise_list, 'pagination': pagination,'key_name':key_name,'search_word' : search_word})
        except:
            return templates.TemplateResponse(
                    name="/info/info_raredisease_nondata.html",
                    context={'request': request})
    else: # key_name이 없을 경우 모든 질환의 리스트를 출력
        dise_list = await collection_disease.get_all()
        dise_list, pagination = await collection_disease.getsbyconditionswithpagination(conditions, page_number)

        return templates.TemplateResponse(
            name="/info/info_raredisease.html",
            context={'request': request, 'dise_list': dise_list, 'pagination': pagination})

@router.get("/info_raredisease_nondata", response_class=HTMLResponse) 
async def institution(request:Request):
    return templates.TemplateResponse(name="info/info_raredisease_nondata.html", context={'request':request})

from flask import Flask, send_file
@router.post('/download')
def download_file():
    path_to_file = "data/csv/[헬프라인]희귀질환목록_2024_03_20_10_34_05.xlsx"
    return send_file(path_to_file, as_attachment=True)




#### -------------------------------------------------------------------------------------------------------

# 의료기관검색
@router.post("/info_institution", response_class=HTMLResponse) 
@router.get("/info_institution") 
async def institution(request:Request):
    await request.form()
    keyword = request.query_params.get('keyword')
    if keyword:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": keyword,
            "fields": "formatted_address,name,rating,geometry,place_id,formatted_phone_number",
            "key": api_key
        }
        async with ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                results = data.get('results', [])  # 'results' 키의 값을 추출하고, 없을 경우 빈 배열을 사용합니다.
        return templates.TemplateResponse("info/info_institution.html", {"request": request, "results": results,'keyword':keyword,'API_KEY': api_key})
    elif keyword is None:
        results = {}
        return templates.TemplateResponse("info/info_institution.html", {"request": request, "results": results,'API_KEY': api_key})

@router.post("/info_institution", response_class=HTMLResponse) 
async def institution(request:Request):
    return templates.TemplateResponse(name="info/info_institution.html", context={'request':request, 'API_KEY':api_key})
# @router.get("/info_raredisease", response_class=HTMLResponse) 
# async def raredisease(request:Request):
#     return templates.TemplateResponse(name="info/info_raredisease.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# 학술정보

@router.get("/info_academicinfo", response_class=HTMLResponse)
async def academicinfo(request:Request):
    return templates.TemplateResponse(name="info/info_academicinfo.html", context={'request':request})

@router.post("/info_academicinfo", response_class=HTMLResponse)
async def academicinfo(request:Request):
    return templates.TemplateResponse(name="info/info_academicinfo.html", context={'request':request})
