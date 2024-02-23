from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = APIRouter()

templates = Jinja2Templates(directory="templates/")

@router.get("/info_academicinfo", response_class=HTMLResponse)
async def academicinfo(request:Request):
    return templates.TemplateResponse(name="info/info_academicinfo.html", context={'request':request})

@router.post("/info_academicinfo", response_class=HTMLResponse)
async def academicinfo(request:Request):
    return templates.TemplateResponse(name="info/info_academicinfo.html", context={'request':request})

@router.get("/info_trend", response_class=HTMLResponse)
async def trend(request:Request):
    return templates.TemplateResponse(name="info/info_trend.html", context={'request':request})

@router.post("/info_trend", response_class=HTMLResponse)
async def trend(request:Request):
    return templates.TemplateResponse(name="info/info_trend.html", context={'request':request})