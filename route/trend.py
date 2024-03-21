from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional
from datetime import datetime
from database.connection import Database
from beanie import PydanticObjectId
from models.trend_documents import trend_documents
from models.trend_guideline import trend_guideline

from models.trend_news import news_trends# mongodb 추가해서 넣어야 함

collection_trend_news= Database(news_trends)
collection_trend_guideline= Database(trend_guideline)
collection_trend_documents= Database(trend_documents)

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
    request:Request,
    ):
    
    await request.form()
    print(dict(await request.form()))
    
    news_list = await collection_trend_news.get_all()
    
    return templates.TemplateResponse(name="trend/trend_news.html", context={'request':request
                                                                             , 'news':news_list})

# news_read

@router.get("/trend_news_read/{object_id}", response_class=HTMLResponse)
async def trend_news_read_function(
    request: Request, 
    object_id:PydanticObjectId
    ):
    
    await request.form()
    print(dict(await request.form()))
    
    news = await collection_trend_news.get(object_id)

    return templates.TemplateResponse(
        name="trend/trend_news_read.html",
        context={"request": request, "news": news})
        
@router.post("/trend_news_read/{object_id}", response_class=HTMLResponse)
async def trend_news_read_function(
    request: Request, 
    ):
    
    await request.form()
    print(dict(await request.form()))
    
    return templates.TemplateResponse(
        name="trend/trend_news.html",
        context={"request": request}
    )
    
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
async def guideline(request:Request, page_number: Optional[int] = 1):
    condition ={}
    guidelines, pagination=await collection_trend_guideline.getsbyconditionswithpagination(condition, page_number)
    return templates.TemplateResponse(name="trend/trend_guideline.html", context={'request':request,
                                                                                  'guidelines':guidelines,
                                                                                  'pagination':pagination})

@router.post("/trend_guideline", response_class=HTMLResponse) 
async def guideline(request:Request):
    return templates.TemplateResponse(name="trend/trend_guideline.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# 민원서식

@router.get("/trend_document", response_class=HTMLResponse) 
async def document(request:Request, page_number: Optional[int] = 1):
    condition ={}
    documents, pagination=await collection_trend_documents.getsbyconditionswithpagination(condition, page_number)
    return templates.TemplateResponse(name="trend/trend_document.html", context={'request':request,
                                                                                  'documents':documents,
                                                                                  'pagination':pagination})


@router.post("/trend_document_read/{object_id}" ) 
async def document(request:Request,  object_id:PydanticObjectId):
    documents = collection_trend_documents.get(object_id)

    return templates.TemplateResponse(name="trend/trend_document.html", context={'request':request,
                                                                                 'documents':documents})

#### -------------------------------------------------------------------------------------------------------

# 관련사이트

@router.get("/trend_site", response_class=HTMLResponse) 
async def trend_site(request:Request):
    return templates.TemplateResponse(name="trend/trend_site.html", context={'request':request})

@router.post("/trend_site", response_class=HTMLResponse) 
async def trend_site(request:Request):
    return templates.TemplateResponse(name="trend/trend_site.html", context={'request':request})