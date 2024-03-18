from database.connection import Database
from fastapi import APIRouter, Request, FastAPI
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from beanie import PydanticObjectId
from typing import Optional
from datetime import datetime
from models.program_list import program
collection_manag_program = Database(program)

app = FastAPI()
router = APIRouter()

# from models.### import .###
# collection_.### = Database(.###)

templates = Jinja2Templates(directory="templates/")

#### -------------------------------------------------------------------------------------------------------

# program
@router.get("/empo_program", response_class=HTMLResponse) 
async def empo_program_function(request:Request):
    return templates.TemplateResponse(name="empo/empo_program.html", context={'request':request})

@router.post("/empo_program", response_class=HTMLResponse) 
async def empo_program_function(request:Request):
    return templates.TemplateResponse(name="empo/empo_program.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# community
@router.get("/empo_community", response_class=HTMLResponse) 
async def empo_community_function(request:Request):
    return templates.TemplateResponse(name="empo/empo_community.html", context={'request':request})

@router.post("/empo_community", response_class=HTMLResponse) 
async def empo_community_function(request:Request):
    return templates.TemplateResponse(name="empo/empo_community.html", context={'request':request})
