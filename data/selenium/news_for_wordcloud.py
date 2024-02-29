# 웹크롤링 기본동작
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from pymongo import MongoClient

# 몽고디비연결
def dbconnect(collection):
    mongoClient = MongoClient("mongodb://192.168.10.236:27017/")
    database = mongoClient[""]
    collection = database[collection]
    return collection

# 뉴스 스크래핑