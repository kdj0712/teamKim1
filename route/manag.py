from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, Union
from datetime import datetime
from database.connection import Database
from beanie import PydanticObjectId
from pydantic import BaseModel, Field, EmailStr

from models.academicinfo import academicinfo
from models.info_rarediseases import diseases
from models.institution import Institutions
from models.trend import news_trends
from models.user_member import members
from models.other_QnA import QnA
from models.notice_list import notice
from models.program_list import program
collection_acade = Database(academicinfo)
collection_dise = Database(diseases)
collection_insti = Database(Institutions)
collection_trend = Database(news_trends)
collection_member = Database(members)    
collection_QnA = Database(QnA)
collection_manag_notice = Database(notice)
collection_manag_program = Database(program)

router = APIRouter()

templates = Jinja2Templates(directory="templates/")


#### -------------------------------------------------------------------------------------------------------

# manag main - 대시보드

@router.get("/managmain", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/managmain.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# user_main

@router.get("/manag_user_main/{page_number}")
@router.get("/manag_user_main") # 검색 with pagination

async def list(
    request: Request,
    page_number: Optional[int] = 1, 
    user_ID: Optional[Union[str, int, float, bool]] = None,
    user_name: Optional[Union[str, int, float, bool]] = None,
    user_phone : Optional[Union[str, int, float, bool]] = None,
    user_email: Optional[EmailStr] = None   
    ):

    user_dict = dict(request._query_params)
    conditions = {}
    search_word = request.query_params.get('search_word')

    if search_word:
        conditions.update({
            "$or": [
                {"user_ID": {'$regex': search_word}},
                {"user_name": {'$regex': search_word}},
                {"user_phone": {'$regex': search_word}},
                {"user_email": {'$regex': search_word}}
            ]
        })
    pass

    if user_ID:
        conditions.find({ 'user_ID': { '$regex': search_word }})
    if user_name:
        conditions.find({ 'user_name': { '$regex': search_word }})
    if user_phone:
        conditions.find({ 'user_phone': { '$regex': search_word }})
    if user_email:
        conditions.find({ 'user_email': { '$regex': search_word }})

    # try:
    User_list, pagination = await collection_member.getsbyconditionswithpagination(
    conditions, page_number
    )
    return templates.TemplateResponse(
    name="manag/user/manag_user_main.html",
    context={'request': request, 'user_list': User_list, 'pagination': pagination,'search_word' : search_word},
    )

#### -------------------------------------------------------------------------------------------------------

# community_main

@router.get("/manag_community_main", response_class=HTMLResponse) 
async def community(request:Request):
    return templates.TemplateResponse(name="manag/community/manag_community_main.html", context={'request':request})

@router.post("/manag_community_main", response_class=HTMLResponse) 
async def community(request:Request):
    return templates.TemplateResponse(name="manag/community/manag_community_main.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# program_main

@router.get("/manag_program_main", response_class=HTMLResponse) 
async def program_main_function(
    request:Request,
    page_number: Optional[int] = 1
    ):
    
    conditions = {}
    
    program_list, pagination = await collection_manag_program.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(
        name="manag/program/manag_program_main.html", 
        context={'request':request, 'pagination': pagination, 'programs': program_list})

@router.post("/manag_program_main", response_class=HTMLResponse) 
async def program_main_function(request:Request):
    
    await request.form()
    print(dict(await request.form()))
    
    programs = await collection_manag_program.get_all()
    
    return templates.TemplateResponse(name="manag/program/manag_program_main.html", context={'request':request, 'programs': programs})

@router.get("/manag_program_write", response_class=HTMLResponse) 
async def program_write_function(request:Request):
    
    
    return templates.TemplateResponse(name="manag/program/manag_program_write.html", context={'request':request})

@router.post("/manag_program_write", response_class=HTMLResponse) 
async def program_write_function(request:Request):
    return templates.TemplateResponse(name="manag/program/manag_program_write.html", context={'request':request})

@router.get("/manag_program_reply/{object_id}", response_class=HTMLResponse) 
async def program_read_function(request:Request, object_id:PydanticObjectId):
    
    program = await collection_manag_program.get(object_id)
    
    return templates.TemplateResponse(name="manag/program/manag_program_reply.html", context={'request':request, 'program': program})

@router.post("/manag_program_reply/{object_id}", response_class=HTMLResponse) 
async def program_read_function(request:Request, object_id:PydanticObjectId):
    await request.form()
    program = await collection_manag_program.get(object_id)
        
    return templates.TemplateResponse(name="manag/program/manag_program_reply.html", context={'request':request, 'programs': program})


#### -------------------------------------------------------------------------------------------------------

# manag_QnA

@router.post("/manag_QnA_main", response_class=HTMLResponse) 
async def FAQ(request:Request,     page_number: Optional[int] = 1, 
    ques_title: Optional[str] = None,
    ques_writer: Optional[str] = None,
    ques_content: Optional[str] = None,
    ques_time: Optional[datetime] = None,
    ques_answer: Optional[str] = None):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    current_time = datetime.now()

    # 이 시간을 item 객체의 'ques_time' 속성에 저장한다.
    dict_form_data['ques_time'] = current_time
    if dict_form_data['ques_title'] =='':
        pass
    else:
        QnAs = QnA(**dict_form_data)
        await collection_QnA.save(QnAs)

    user_dict = dict(form_data)
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
                {"dise_url": {'$regex': search_word}}
            ]
        })
    pass

    if ques_title:
        conditions.find({ 'ques_title': { '$regex': search_word }})
    pass
    try:
        QnA_list, pagination = await collection_QnA.getsbyconditionswithpagination(
        conditions, page_number
    )
        return templates.TemplateResponse(
        name="manag/QnA/manag_QnA_main.html",
        context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word' : search_word},
    )

    except:
        pass
        # return templates.TemplateResponse(
        # name="/manag/manag_manager_nonpage.html",
        # context={'request': request})

@router.get("/QnA/manag_QnA_manager_nonpage", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_manager_nonpage.html", context={'request':request})

@router.post("/QnA/manag_QnA_manager_nonpage", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_manager_nonpage.html", context={'request':request})

@router.get("/manag_QnA_main/{page_number}")
@router.get("/manag_QnA_main") # 검색 with pagination
async def list(
    request: Request,
    page_number: Optional[int] = 1, 
    ques_title: Optional[str] = None,
    ques_writer: Optional[str] = None,
    ques_content: Optional[str] = None,
    ques_time: Optional[datetime] = None,
    ques_answer: Optional[str] = None
):
    # db.answers.find({'name':{ '$regex': '김' }})
    # { 'name': { '$regex': user_dict.word } }
    
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
                {"dise_url": {'$regex': search_word}}
            ]
        })

    pass

    if ques_title:
        conditions.find({ 'ques_title': { '$regex': search_word }})
    pass

    try:
        QnA_list, pagination = await collection_QnA.getsbyconditionswithpagination(
        conditions, page_number
    )
        return templates.TemplateResponse(
        name="manag/QnA/manag_QnA_main.html",
        context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word' : search_word},
    )

    except:
        return templates.TemplateResponse(
        name="manag/QnA/manag_QnA_manager_nonpage.html",
        context={'request': request})
        pass

# 글쓰기 창
@router.get("/manag_QnA_write", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_write.html", context={'request':request})

@router.post("/manag_QnA_write", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_write.html", context={'request':request})

# 글 확인

@router.get("/manag_QnA_read/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request, object_id:PydanticObjectId):
    dict(request._query_params)
    QnA = await collection_QnA.get(object_id)
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_read.html", context={'request':request,'QnAs' : QnA})


@router.post("/manag_QnA_read/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request, object_id:PydanticObjectId):
    await request.form()
    QnA = await collection_QnA.get(object_id)
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_read.html", context={'request':request ,'QnAs' : QnA})

# 답글 달기
@router.post("/manag_QnA_reply/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request, object_id:PydanticObjectId,
    page_number: Optional[int] = 1, 
    ques_title: Optional[str] = None,
    ques_writer: Optional[str] = None,
    ques_content: Optional[str] = None,
    ques_time: Optional[datetime] = None,
    ques_answer: Optional[str] = None):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    await collection_QnA.update_one(object_id, dict_form_data)
    conditions = {}

    search_word = request.query_params.get('search_word')
  
    if search_word:
        conditions.update({
            "$or": [
                {"ques_title": {'$regex': search_word}},
                {"ques_writer": {'$regex': search_word}},
                {"ques_content": {'$regex': search_word}},
                {"ques_time": {'$regex': search_word}},
                {"ques_answer": {'$regex': search_word}},
            ]
        })
    pass

    if ques_title:
        conditions.find({ 'ques_title': { '$regex': search_word }})
    pass
    try:
        QnA_list, pagination = await collection_QnA.getsbyconditionswithpagination(
        conditions, page_number
    )
        return templates.TemplateResponse(
        name="manag/QnA/manag_QnA_manager.html",
        context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word':search_word},
    )

    except:
        return templates.TemplateResponse(
        name="manag/QnA/manag_QnA_manager_nonpage.html",
        context={'request': request},
    )
        
# 글 삭제
@router.post("/manag_QnA_delete/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request,object_id:PydanticObjectId,
    page_number: Optional[int] = 1, 
    ques_title: Optional[str] = None,
    ques_writer: Optional[str] = None,
    ques_content: Optional[str] = None,
    ques_time: Optional[datetime] = None,
    ques_answer: Optional[str] = None):
    await collection_QnA.delete_one(object_id)
    
    form_data = await request.form()
    dict_form_data = dict(form_data)
    

    conditions = {}

    search_word = request.query_params.get('search_word')
  
    if search_word:
        conditions.update({
            "$or": [
                {"ques_title": {'$regex': search_word}},
                {"ques_writer": {'$regex': search_word}},
                {"ques_content": {'$regex': search_word}},
                {"ques_time": {'$regex': search_word}},
                {"ques_answer": {'$regex': search_word}},
            ]
        })
    pass

    if ques_title:
        conditions.find({ 'ques_title': { '$regex': search_word }})
    pass
    try:
        QnA_list, pagination = await collection_QnA.getsbyconditionswithpagination(
        conditions, page_number
    )
        return templates.TemplateResponse(
        name="manag/QnA/manag_QnA_main.html",
        context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word':search_word},
    )

    except:
        return templates.TemplateResponse(
        name="manag/QnA/manag_QnA_manager_nonpage.html",
        context={'request': request},
    )

@router.post("/manag_user_detail/{object_id}") # 펑션 호출 방식
async def reads(request:Request,object_id:PydanticObjectId):
    await request.form()
    print(dict(await request.form()))
    return templates.TemplateResponse(name="manag/user/manag_user_detail.html", context={'request':request, 'object_id':object_id})


@router.get("/manag_user_detail/{object_id}") 
async def FAQ(request:Request, object_id:PydanticObjectId):
    dict(request._query_params)
    user_list = await collection_member.get(object_id)
    return templates.TemplateResponse(name="manag/user/manag_user_detail.html", context={'request':request,'User' : user_list})

#### -------------------------------------------------------------------------------------------------------

# notice_main

@router.get("/manag_notice_main", response_class=HTMLResponse) 
async def notice_main_function(
    request:Request, 
    page_number: Optional[int] = 1
    ):
    
    conditions = {}
    
    notice_list, pagination = await collection_manag_notice.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(
    name="manag/notice/manag_notice_main.html",
    context={'request': request, 'pagination': pagination, 'notices': notice_list})

@router.post("/manag_notice_main", response_class=HTMLResponse) 
async def notice_main_function(request:Request):
    await request.form()
    print(dict(await request.form()))
    
    notices = await collection_manag_notice.get_all()
    
    return templates.TemplateResponse(name="manag/notice/manag_notice_main.html", context={'request':request, 'notices':notices})

# notice_write

@router.get("/manag_notice_write", response_class=HTMLResponse) 
async def notice_write_function(request:Request):
    return templates.TemplateResponse(name="manag/notice/manag_notice_write.html", context={'request':request})

@router.post("/manag_notice_write", response_class=HTMLResponse) 
async def notice_write_function(request:Request):
    return templates.TemplateResponse(name="manag/notice/manag_notice_write.html", context={'request':request})

# notice_reply

@router.get("/manag_notice_reply", response_class=HTMLResponse) 
async def notice_reply_function(request:Request):
    return templates.TemplateResponse(name="manag/notice/manag_notice_reply.html", context={'request':request})

@router.post("/manag_notice_reply", response_class=HTMLResponse) 
async def notice_reply_function(request:Request):
    return templates.TemplateResponse(name="manag/notice/manag_notice_reply.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------
    
# data analytics

@router.get("/data_analytics", response_class=HTMLResponse) 
async def data_analytics(request:Request):
    return templates.TemplateResponse(name="manag/data_analytics/manag_data_analytics.html", context={'request':request})

@router.post("/data_analytics", response_class=HTMLResponse) 
async def data_analytics(request:Request):
    return templates.TemplateResponse(name="manag/data_analytics/manag_data_analytics.html", context={'request':request})