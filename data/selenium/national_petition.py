from selenium import webdriver
import time

# mongodb 연결
from pymongo import MongoClient
mongoClient = MongoClient("")
database = mongoClient[""]
collection = database['']

# chrome browser 열기
browser = webdriver.Chrome()
browser.get("")

html = browser.page_source
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys