from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId

from models.academicinfo import academicinfo
from models.info_rarediseases import diseases
from models.institution import Institutions
from models.user_member import members
from models.trend import news_trends
from models.other_QnA import QnA
from models.manag_program import program
from models.manag_notice import notice
import os

from motor.motor_asyncio import AsyncIOMotorClient

from pydantic_settings import BaseSettings

from utils.paginations import Paginations

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    container_prefix: Optional[str] = None
    API_KEY : Optional[str] = None
    async def initialize_database(self):
        if self.DATABASE_URL is not None:
            client = AsyncIOMotorClient(self.DATABASE_URL)
            await init_beanie(database=client.get_default_database(),
                              document_models=[academicinfo, diseases, Institutions, members, news_trends, QnA, program, notice])

    class Config:
        env_file = ".env"

class Database:
    # model 즉 collection
    def __init__(self, model) -> None:
        self.model = model
        pass       

    # 전체 리스트
    async def get_all(self) :
        documents = await self.model.find_all().to_list()   # find({})
        pass
        return documents
    
    # 상세 보기
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)  # find_one()
        if doc:
            return doc
        return False    
    
    # 저장
    async def save(self, document) -> None:
        await document.create()
        return None   
    
    # 업데이트
    async def update_one(self, id: PydanticObjectId, dic) -> Any:
        doc = await self.model.get(id)
        if doc:
            for key, value in dic.items():
                setattr(doc, key, value)
            await doc.save()
            return True
        return False
    
        # 삭제
    # async def delete(self, id: PydanticObjectId) -> Any:
    #     from pymongo import MongoClient
    #     from dotenv import load_dotenv
    #     import os

    #     load_dotenv()
    #     DB_URI = os.getenv('DB_URI')
    #     # MongoDB 연결 설정
    #     client = MongoClient(DB_URI)
    #     db = client['teamplays']
    #     collection = db['QnA']
    #     deleted_doc = await collection.delete_one({"_id": id})
    #     if deleted_doc:
    #         return True
    #     return False
     
    async def delete_one(self, id: PydanticObjectId) -> bool:
        doc = await self.model.get(id)
        if doc:
            await doc.delete()
            return True
        return False

    # column 값으로 여러 Documents 가져오기
    async def getsbyconditions(self, conditions:dict) -> Any:
        documents = await self.model.find(conditions).to_list()  # find({})
        if documents:
            return documents
        return False    
    
    async def getsbyconditionswithpagination(self
                                             , conditions:dict, page_number) -> Any:
        # find({})
        total = await self.model.find(conditions).count()
        pagination = Paginations(total_records=total, current_page=page_number)
        documents = await self.model.find(conditions).skip(pagination.start_record_number-1).limit(pagination.records_per_page).to_list()
        if documents:
            return documents, pagination
        return False  
    



if __name__ == '__main__':
    settings = Settings()
    async def init_db():
        await settings.initialize_database()

    collection_user = Database(members)
    conditions = "{ name: { $regex: '이' } }"
    list = collection_user.getsbyconditions(conditions)
    pass