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
# from google.oauth2 import service_account
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

#### -------------------------------------------------------------------------------------------------------

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
# 희귀질환정보검색
@router.post("/info_raredisease", response_class=HTMLResponse) 
async def raredisease(request:Request):
    return templates.TemplateResponse(name="search/search_raredisease.html", context={'request':request})

@router.get("/info_raredisease/{page_number}")
@router.get("/info_raredisease") # 검색 with pagination
async def list(
    request: Request, 
    page_number: Optional[int] = 1, 
    dise_name_kr: Optional[str] = None,
):
    
    user_dict = dict(request._query_params)
    conditions = {}

    search_word = request.query_params.get('search_word')

    if search_word:
        conditions.update({
            "$or": [
                {"dise_KCD_code": {'$regex': search_word}},
                {"dise_group": {'$regex': search_word}},
                {"dise_name_kr": {'$regex': search_word}},
                {"dise_name_en": {'$regex': search_word}},
                {"dise_support": {'$regex': search_word}},
                {"dise_url": {'$regex': search_word}},
                {"dise_symptoms": {'$regex': search_word}}
            ]
        })

    pass

    if dise_name_kr:
        conditions.find({ 'dise_name_kr': { '$regex': search_word }})
    pass

    try :
        dise_list, pagination = await collection_disease.getsbyconditionswithpagination(
            conditions, page_number
        )

        return templates.TemplateResponse(
            name="/info/info_raredisease.html",
            context={'request': request, 'dises': dise_list, 'pagination': pagination,'search_word' : search_word},
        )
    except:
        return templates.TemplateResponse(
            name="/info/info_raredisease_nondata.html",
            context={'request': request},
        )

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
