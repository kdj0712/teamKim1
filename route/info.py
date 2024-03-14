from fastapi import APIRouter, FastAPI, Form, Depends, Query, HTTPException
from typing import Optional
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aiohttp import ClientSession
from fastapi import Request
from pydantic import BaseModel
from typing import Optional
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

from database.connection import Database
from models.info_rarediseases import diseases
collection_disease = Database(diseases)

from models.institution import Institutions
collection_institution = Database(Institutions)

from models.trend import news_trends
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
tfidf_vectorizer_file_name = 'search_symptoms.pkl'
vectorizer = load_pickle_from_gcs(bucket_name, tfidf_vectorizer_file_name)

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
@router.post("/info_raredisease", response_class=HTMLResponse) 
async def raredisease(request:Request):
    return templates.TemplateResponse(name="search/search_raredisease.html", context={'request':request})

# @router.get("/info_raredisease/{page_number}")
# @router.get("/info_raredisease")
# async def list(
#     request: Request, 
#     page_number: Optional[int] = 1, 
#     dise_name_kr: Optional[str] = None,
#     dise_symptoms: Optional[str] = None,
# ):
    
#     user_dict = dict(request._query_params)
#     conditions = {}

#     search_word = request.query_params.get('search_word')

#     if search_word:
#         conditions.update({
#             "$or": [
#                 {"dise_KCD_code": {'$regex': search_word}},
#                 {"dise_group": {'$regex': search_word}},
#                 {"dise_name_kr": {'$regex': search_word}},
#                 {"dise_name_en": {'$regex': search_word}},
#                 {"dise_support": {'$regex': search_word}},
#                 {"dise_url": {'$regex': search_word}},
#                 {"dise_symptoms": {'$regex': search_word}}
#             ]
#         })

#     pass
#     if dise_name_kr:
#         conditions.find({ 'dise_name_kr': { '$regex': search_word }})
#     pass
#     try :
#         dise_list, pagination = await collection_disease.getsbyconditionswithpagination(
#             conditions, page_number
#         )

#         return templates.TemplateResponse(
#             name="/info/info_raredisease.html",
#             context={'request': request, 'dises': dise_list, 'pagination': pagination,'search_word' : search_word}
#         )
#     except:
#         return templates.TemplateResponse(
#             name="/info/info_raredisease_nondata.html",
#             context={'request': request}
#         )
@router.get("/info_raredisease/{page_number}")
@router.get("/info_raredisease")
async def disease_list(request: Request, page_number: int = 1, key_name: Optional[str] = Query(None), search_word: Optional[str] = Query(None)):
    # await request.form()
    # dise_list = await collection_disease.get_all()
    conditions = {}
    search_word = request.query_params.get('search_word')
    if key_name and search_word:
        # 검색 조건을 기반으로 질환을 필터링하는 로직
        if key_name == 'dise_name_kr':
            # 희귀질환명으로 검색하는 로직
            conditions["dise_name_kr"] = search_word
        elif key_name == 'dise_KCD_code':
            # KCD코드로 검색하는 로직
            conditions["dise_KCD_code"] = search_word
        elif key_name == 'dise_spc_code':
            # 산정특례 특정기호로 검색하는 로직
            conditions["dise_spc_code"] = search_word
        elif key_name == 'dise_symptoms':
            # 증상명으로 검색하는 로직
            conditions["dise_symptoms"] = search_word
        dise_list, pagination = await collection_disease.getsbyconditionswithpagination(conditions, page_number)
    else:
        # key_name이 없을 경우 모든 질환의 리스트를 출력
        dise_list = await collection_disease.get_all()
        dise_list, pagination = await collection_disease.getsbyconditionswithpagination(conditions, page_number)

        return templates.TemplateResponse(
            name="/info/info_raredisease.html",
            context={'request': request, 'dise_list': dise_list, 'pagination': pagination}
        )



    # disease_list,pagination = await collection_disease.getsbyconditionswithpagination()
    # return templates.TemplateResponse(name="notice/notice_main.html", context={'request':request, 'disease_list' : disease_list,'pagination': pagination})


@router.get("/info_raredisease_nondata", response_class=HTMLResponse) 
async def institution(request:Request):
    return templates.TemplateResponse(name="info/info_raredisease_nondata.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# 의료기관검색

@router.get("/info_institution", response_class=HTMLResponse) 
async def institution(request:Request, keyword: str = Query(None, alias="keyword")):
    if keyword:
        url = "https://maps.googleapis.com/maps/api/place/searchByText/json"
        params = {
            "input": keyword,
            "inputtype": "textquery",
            "fields": "photos,formatted_address,name,rating,geometry,place_id",
            "key": api_key
        }
        async with ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                results = data.get('results', [])  # 'results' 키의 값을 추출하고, 없을 경우 빈 배열을 사용합니다.
        return templates.TemplateResponse("info/info_institution.html", {"request": request, "results": results})
    elif keyword is None:
        return templates.TemplateResponse("info/info_institution.html", {"request": request, 'API_KEY': api_key})

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
