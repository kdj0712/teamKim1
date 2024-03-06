from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from beanie import PydanticObjectId
from typing import Optional
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()
router = APIRouter()

from database.connection import Database

# from models.### import .###
# collection_.### = Database(.###)

templates = Jinja2Templates(directory="templates/")

@router.get("/empo_program", response_class=HTMLResponse) 
async def empo_program(request:Request):
    return templates.TemplateResponse(name="empo/empo_program.html", context={'request':request})

@router.get("/empo_community", response_class=HTMLResponse) 
async def empo_community(request:Request):
    return templates.TemplateResponse(name="empo/empo_community.html", context={'request':request})
