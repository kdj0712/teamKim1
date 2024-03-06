# 웹크롤링 동작

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pymongo import MongoClient

# 몽고 디비 연결
def dbconnect(collection) :
    mongoClient = MongoClient("mongodb://192.168.10.236:27017/")
    database = mongoClient["skykim"]
    collection = database[collection]
    return collection

# 뉴스 스크래핑

def bosascrapping(browser_name, keyword) :
    browser = webdriver.Chrome()
    browser.get(browser_name)
    browser.find_element(By.CSS_SELECTOR, "#userSearch > button > i").click() # 찾기
    browser.find_element(By.CSS_SELECTOR, "#search").send_keys(keyword) # keyword에 검색할 것 넣기
    browser.find_element(By.CSS_SELECTOR, "#userSearch > fieldset > form > button.sch-btn").click() # 찾기 검색
    time.sleep(1)
    browser.find_element(By.CSS_SELECTOR, "#sections > section > header > div > div > a:nth-child(1)").click() #제목형
    time.sleep(1)
    # db 연결
    bosa_news_coll = dbconnect("bosa_news_all")
    bosa_news_coll.delete_many({})
    # 위에서부터 스크래핑하기
    # 첫 페이지
    for page_num in range(2,12):
        contents = browser.find_elements(By.CSS_SELECTOR, "#section-list > ul > li")
        browser.find_element(By.CSS_SELECTOR, f"#sections > section > nav > ul > li:nth-child({page_num})").click()
        time.sleep(1)
        for content in contents :
            news_title = content.find_element(By.CSS_SELECTOR, "#section-list > ul > li > h4").text
            news_url = content.find_element(By.CSS_SELECTOR, "#section-list > ul > li> h4 > a").get_attribute("href")
            news_when = content.find_element(By.CSS_SELECTOR, "#section-list > ul > li > em.info.dated").text
            news_topic = content.find_element(By.CSS_SELECTOR, "#section-list > ul > li > em.info.category").text
            content.find_element(By.CSS_SELECTOR, "#section-list > ul > li > a").click() # 안으로 들어가기
            news_contents = ''
            news_contents_p = browser.find_elements(By.CSS_SELECTOR, "#article-view-content-div > p")
            for news_p in news_contents_p :
                news_contents += news_p
            bosa_news_coll.insert_one({"news_title" : news_title
                                       ,"news_when" : news_when
                                       ,"news_topic":news_topic
                                       ,"news_contents":news_contents
                                       ,"news_url":news_url })
            browser.back()
            time.sleep(1)   
    #나머지 페이지
    while True : 
        browser.find_element(By.CSS_SELECTOR, "#sections > section > nav > ul > li.pagination-next > a").click()
        time.sleep(1)
        for page_num in range(4,14):
            contents = browser.find_elements(By.CSS_SELECTOR, "#section-list > ul > li")
            browser.find_element(By.CSS_SELECTOR, f"#sections > section > nav > ul > li:nth-child({page_num})").click()
            time.sleep(1)
            for content in contents :
                news_title = content.find_element(By.CSS_SELECTOR, "#section-list > ul > li > h4").text
                news_url = content.find_element(By.CSS_SELECTOR, "#section-list > ul > li> h4 > a").get_attribute("href")
                news_when = content.find_element(By.CSS_SELECTOR, "#section-list > ul > li > em.info.dated").text
                news_topic = content.find_element(By.CSS_SELECTOR, "#section-list > ul > li > em.info.category").text
                content.find_element(By.CSS_SELECTOR, "#section-list > ul > li > a").click() # 안으로 들어가기
                news_contents = ''
                news_contents_p = browser.find_elements(By.CSS_SELECTOR, "#article-view-content-div > p")
                for news_p in news_contents_p :
                    news_contents += news_p
                bosa_news_coll.insert_one({"news_title" : news_title
                                        ,"news_when" : news_when
                                        ,"news_topic":news_topic
                                        ,"news_contents":news_contents
                                        ,"news_url":news_url })
                    
        

    
if __name__ == "__main__" : 
    bosascrapping("http://www.bosa.co.kr/", "희귀질환")