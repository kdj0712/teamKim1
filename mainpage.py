from fastapi import FastAPI
app = FastAPI()

from database.connection import Settings
settings = Settings()
@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

from route.user import router as user_router
from route.trend import router as trend_router
from route.info import router as info_router
from route.empo import router as empo_router
from route.other import router as other_router
from route.manag import router as manag_router

from fastapi import Request
from fastapi.templating import Jinja2Templates
app.include_router(user_router, prefix="/user")
app.include_router(trend_router, prefix="/trend")
app.include_router(info_router, prefix="/info")
app.include_router(empo_router, prefix="/empo")
app.include_router(other_router, prefix="/other")
app.include_router(manag_router, prefix="/manag")


templates = Jinja2Templates(directory="templates/")

from fastapi.middleware.cors import CORSMiddleware
# No 'Access-Control-Allow-Origin'
# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 접근 가능한 도메인만 허용하는 것이 좋습니다.
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
# url 경로, 자원 물리 경로, 프로그래밍 측면
app.mount("/data/img", StaticFiles(directory="data/img/"), name="static_img")


@app.post("/")
@app.get("/")
async def root(request:Request):
    await request.form()
    key_name = request.query_params.get('key_name')
    if key_name == None :
        return templates.TemplateResponse("mainpage.html",{'request':request})
    else :
        search_word = request.query_params.get('search_word')
    
        return templates.TemplateResponse("mainpage.html",
                                      context={'request': request, 'key_name':key_name,'search_word' : search_word})
        


@app.post("/")
async def root(request:Request):
    return templates.TemplateResponse("mainpage.html",{'request':request})


## 뉴스 추천
from database.connection import Database
from models.user_member import members
from models.trend_news import news_trends as news
members_coll = Database(members)
news_coll = Database(news)

from datetime import datetime, timedelta
from pymongo import DESCENDING

@app.get("/")
async def news_recomment(request:Request):
    hope_info = '프로그램 참여' #사용자 ID를 이용해서 유지가능하게 하면 user_id 도입
    recent_day = 20 # 최근 20일 간의 뉴스만 고려
    start_date = datetime.now() - timedelta(days=recent_day)
    if hope_info == '프로그램 참여' :
        news_type_user = '심포지엄/행사'
    elif hope_info == '관련 법 사항' :
        news_type_user = '의료/법안'
    
    query = {
    'news_type': news_type_user,
    'publish_date': {'$gte': start_date}
}

    news_list = await news_coll.find(query).sort('publish_date', DESCENDING).limit(4).to_list(lenth=4)

    recommend_news = []
    for news in news_list:
        recommend_news.append({
            'news_title' : news['news_title']
            , 'news_when' : news['news_when']
            , 'news_contents' : news['news_contents']
            , 'news_url' : news['news_urls']
            , 'news_type' : news['news_type']
        })

    return templates.TemplateResponse("mainpage.html",{'request':request, 'recommend_news': recommend_news})

    
