
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


from pymongo import MongoClient

import pickle
import os

# 몽고 디비 연결
def dbconnect(collection) :
    mongoClient = MongoClient("mongodb://192.168.10.236:27017/")
    database = mongoClient["Seleniums"]
    collection = database[collection]
    return collection

# 뉴스 스크래핑

def bosascrapping(browser_name, keyword) :
    bosa_news_coll = dbconnect('bosa_news_weekly')

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 현재 날짜 설정
    from datetime import datetime, timedelta
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    one_week_date = current_date - timedelta(days=10)
    current_date = current_date.strftime('%Y-%m-%d')
    one_week_date = one_week_date.strftime('%Y-%m-%d')

    ## 상세검색
    browser = webdriver.Chrome()
    browser.get(browser_name)
    browser.find_element(By.CSS_SELECTOR, "div.user-etc > div.search-list > span > a").click() # 상세 검색
    time.sleep(1)
    new_tab = browser.window_handles[-1]
    browser.switch_to.window(new_tab)

    browser.find_element(By.CSS_SELECTOR, "#sc_sdate").clear()
    browser.find_element(By.CSS_SELECTOR, "#sc_sdate").send_keys(one_week_date)
    browser.find_element(By.CSS_SELECTOR, "#sc_edate").clear()
    browser.find_element(By.CSS_SELECTOR, "#sc_edate").send_keys(current_date)
    browser.find_element(By.CSS_SELECTOR, "#sc_word").send_keys(keyword)
    browser.find_element(By.CSS_SELECTOR, "#search-tabs1 > form > footer > div > button").click()
    time.sleep(2)
    ## 스크래핑
    contents = browser.find_elements(By.CSS_SELECTOR, "#section-list > ul > li")
    for index in range(len(contents)) :
        contents = browser.find_elements(By.CSS_SELECTOR, "#section-list > ul > li")
        try : 
            news_title = contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li > h4 > a").text
            news_url = contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li> h4 > a").get_attribute("href")
            news_when_orgin = contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li > em.info.dated").text
            contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li> h4 > a").click() # 안으로 들어가기
            news_contents = ''
            news_contents_p = browser.find_elements(By.CSS_SELECTOR, "#article-view-content-div > p")
            for news_p in news_contents_p :
                news_contents += news_p.text

            # 가지고 온 내용 수정

            # with open('data\pkl\\news_recommend.pkl', "rb") as file:
            #     model = pickle.load(file)
            with open('data\pkl\\news_recommend_model.pkl', "rb") as file:
                model_test = pickle.load(file)

            
            with open('data/pkl/news_recommend_vectorizer.pkl', "rb") as file : 
                vector_test = pickle.load(file)
            


            vector_test_title = vector_test.transform(news_title)
            answer_test = model_test.predict(vector_test_title)

            # news_topic = model([news_title])
            news_paper = '의학신문'
            
            # 날짜 형식 맞춰주기
            desired_format = "%Y-%m-%d"
            news_when = datetime.strftime(news_when_orgin, desired_format)
            
            bosa_news_coll.insert_one({"news_title" : news_title
                                    ,"news_when" : news_when
                                    ,"news_contents":news_contents
                                    ,"news_url":news_url
                                    ,"news_topic" : news_topic
                                    , "news_paper" : news_paper })
            browser.back()
            time.sleep(1)
        except StaleElementReferenceException :
            print("StaleElementReferenceException 발생. 다음 요소로 넘어갑니다")
            continue
        
if __name__ == "__main__" : 
    bosascrapping("http://www.bosa.co.kr/", "희귀질환")