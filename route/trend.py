from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional
from datetime import datetime
from database.connection import Database
from beanie import PydanticObjectId

from models.trend_news import news_trends as news  # mongodb 추가해서 넣어야 함
collection_trend_news= Database(news)

router = APIRouter()

templates = Jinja2Templates(directory="templates/")

#### -------------------------------------------------------------------------------------------------------

# 뉴스
@router.get("/trend_news/{page_number}")
@router.get("/trend_news", response_class=HTMLResponse) 
async def trend_news(
    request:Request, 
    page_number: Optional[int] = 1
    ):
    
    await request.form()
    print(dict(await request.form()))
    
    conditions = {}
    
    news_list, pagination = await collection_trend_news.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(
        name="trend/trend_news.html", 
        context={'request': request, 'pagination': pagination, 'news': news_list})

@router.post("/trend_news", response_class=HTMLResponse) 
async def trend_news(
    request:Request):
    
    await request.form()
    print(dict(await request.form()))
    
    news_list = await collection_trend_news.get_all()
    
    return templates.TemplateResponse(name="trend/trend_news.html", context={'request':request
                                                                             , 'news':news_list})

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