from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional
from datetime import datetime
from database.connection import Database
from beanie import PydanticObjectId



from models.trend import news_trends  # mongodb 추가해서 넣어야 함


router = APIRouter()

templates = Jinja2Templates(directory="templates/")

#### -------------------------------------------------------------------------------------------------------

# 뉴스

@router.get("/trend_news", response_class=HTMLResponse) 
async def trend_news(request:Request):
    return templates.TemplateResponse(name="trend/trend_news.html", context={'request':request})

@router.post("/trend_news", response_class=HTMLResponse) 
async def trend_news(request:Request):
    news_data = news_trends.objects().all()

    news_title = []
    news_when = []
    news_contents = []
    news_urls = []
    news_paper = '의학신문'

    for data in news_data :
        news_title.append(data.news_title)
        news_when.append(data.news_when)
        news_contents.append(data.news_contents)
        news_urls.append(data.news_url)

    return templates.TemplateResponse(name="trend/trend_news.html", context={'request':request
                                                                             , 'news_title' : news_title
                                                                             , 'news_when' : news_when
                                                                             , 'news_contents' : news_contents
                                                                             , 'news_urls' : news_urls
                                                                            , 'news_paper' : news_paper})

#### -------------------------------------------------------------------------------------------------------

# 법, 시행령, 시행규칙

@router.get("/trend_law", response_class=HTMLResponse) 
async def trend_law(request:Request):
    return templates.TemplateResponse(name="trend/trend_law.html", context={'request':request})

@router.post("/trend_law", response_class=HTMLResponse) 
async def trend_law(request:Request):
    return templates.TemplateResponse(name="trend/trend_law.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# 고시, 지침

@router.get("/trend_guideline", response_class=HTMLResponse) 
async def guideline(request:Request):
    return templates.TemplateResponse(name="trend/trend_guideline.html", context={'request':request})

@router.post("/trend_guideline", response_class=HTMLResponse) 
async def guideline(request:Request):
    return templates.TemplateResponse(name="trend/trend_guideline.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# 민원서식

@router.get("/trend_document", response_class=HTMLResponse) 
async def document(request:Request):
    return templates.TemplateResponse(name="trend/trend_document.html", context={'request':request})

@router.post("/trend_document", response_class=HTMLResponse) 
async def document(request:Request):
    return templates.TemplateResponse(name="trend/trend_document.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# 관련사이트

@router.get("/trend_site", response_class=HTMLResponse) 
async def trend_site(request:Request):
    return templates.TemplateResponse(name="trend/trend_site.html", context={'request':request})

@router.post("/trend_site", response_class=HTMLResponse) 
async def trend_site(request:Request):
    return templates.TemplateResponse(name="trend/trend_site.html", context={'request':request})