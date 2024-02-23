from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional
from datetime import datetime
from database.connection import Database
from beanie import PydanticObjectId


from models.member import members
collection_member = Database(members)
from models.QnA import QnA
collection_QnA = Database(QnA)

router = APIRouter()

templates = Jinja2Templates(directory="templates/")

@router.post("/manag_manager", response_class=HTMLResponse) 
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
        name="/manag/manag_manager.html",
        context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word' : search_word},
    )

    except:
        return templates.TemplateResponse(
        name="/manag/manag_manager_nonpage.html",
        context={'request': request},
    )

@router.get("/manag_manager_nonpage", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/manag_manager_nonpage.html", context={'request':request})

@router.post("/manag_manager_nonpage", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/manag_manager_nonpage.html", context={'request':request})


@router.get("/manag_manager/{page_number}")
@router.get("/manag_manager") # 검색 with pagination
# http://127.0.0.1:8000/users/list_jinja_pagination?key_name=name&word=김
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=김
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
        name="/manag/manag_manager.html",
        context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word' : search_word},
    )

    except:
        return templates.TemplateResponse(
        name="/manag/manag_manager_nonpage.html",
        context={'request': request},
    )








# 글쓰기 창
@router.get("/manag_write", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/manag_write.html", context={'request':request})

@router.post("/manag_write", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/manag_write.html", context={'request':request})

# 글 확인

@router.get("/manag_read/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request, object_id:PydanticObjectId):
    dict(request._query_params)
    QnA = await collection_QnA.get(object_id)
    return templates.TemplateResponse(name="manag/manag_read.html", context={'request':request,'QnAs' : QnA})


@router.post("/manag_read/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request, object_id:PydanticObjectId):
    await request.form()
    QnA = await collection_QnA.get(object_id)
    return templates.TemplateResponse(name="manag/manag_read.html", context={'request':request ,'QnAs' : QnA})


# 답글 달기
@router.post("/manag_reply/{object_id}", response_class=HTMLResponse) 
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
        name="/manag/manag_manager.html",
        context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word':search_word},
    )

    except:
        return templates.TemplateResponse(
        name="/manag/manag_manager_nonpage.html",
        context={'request': request},
    )
# 글 삭제
@router.post("/manag_delete/{object_id}", response_class=HTMLResponse) 
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
        name="/manag/manag_manager.html",
        context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word':search_word},
    )

    except:
        return templates.TemplateResponse(
        name="/manag/manag_manager_nonpage.html",
        context={'request': request},
    )