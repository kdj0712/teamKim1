from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional
from datetime import datetime
from database.connection import Database
from beanie import PydanticObjectId



from models.trend import trends  # mongodb 추가해서 넣어야 함


router = APIRouter()

templates = Jinja2Templates(directory="templates/")


@router.get("/", response_class=HTMLResponse)
async def TREND(request:Request):
    return templates.TemplateResponse(name=" ",context={'request':request})

