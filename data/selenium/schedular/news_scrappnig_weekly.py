
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
import os
from konlpy.tag import Okt


okt = Okt()
stopwords = ['서울대', '희귀질환', '희귀', '대다',  '케다', '소아', '생명', '한국', '한미','사노피', '하다', '급여', '국내', '샤이어',  '스케', '세포'
            , '병원',  '질환',  '한독', '화이자제약',  '전달', '질병', '인하대병원',  '관리', '다국적', '환자', '지정', '치료'
            , '오다', '헌터', '작년', '브리', '위해', '베다', '받다', '심평원', '코로나', '건보', '화순', '전남대', '실시', '자임','녹십자'
            ] #추가 생성 필요
f=open('/app/teamKim/data/selenium/schedular/korean_stopwords_basic.txt') #기본적으로 제공되는 한국어 불용어 리스트 파일
lines = f.readlines()
for line in lines:
    line = line.strip()
    stopwords.append(line)
f.close()
def tokenizer(raw, pos=['Noun', 'Verb'],stopword=stopwords):
    return [
        word for word, tag in okt.pos(raw, norm=True, stem=True)
        if len(word) >1 and tag in pos and word not in stopword
    ]
# with open('data/pkl/news_title_tokenizer.pkl', "rb") as file:
#     news_title_tokenizer = pickle.load(file)
with open('data/pkl/news_recommend_model.pkl', "rb") as file:
    model_test = pickle.load(file)


# 몽고 디비 연결
def dbconnect(collection) :
    mongoClient = MongoClient("mongodb://192.168.10.236:27017/")
    database = mongoClient["Seleniums"]
    collection = database[collection]
    return collection

# 날짜 바꾸기
def convert_to_datetime(orgin_str):
    current_datetime = datetime.now()
    news_datetime = datetime.strptime(orgin_str, "%m.%d %H:%M")
    current_year = current_datetime.year
    news_datetime = news_datetime.replace(year=current_year)
    return news_datetime

# 뉴스 스크래핑

def bosascrapping(browser_name, keyword) :

    bosa_news_coll = dbconnect('bosa_news_weekly')
    bosa_news_coll.delete_many({})

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
    browser = webdriver.Chrome(options=chrome_options)
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
            
            # 날짜 형식 맞춰주기
            news_datetime = convert_to_datetime(news_when_orgin)
            news_when = news_datetime.strftime("%Y-%m-%d")
            
            bosa_news_coll.insert_one({"news_title" : news_title
                                    ,"news_when" : news_when
                                    , "news_datetime" : news_datetime
                                    ,"news_contents":news_contents
                                    ,"news_url":news_url
                                     ,'news_paper' : "의학신문" })
            browser.back()
            time.sleep(1)
        except StaleElementReferenceException :
            print("StaleElementReferenceException 발생. 다음 요소로 넘어갑니다")
            continue


bosascrapping("http://www.bosa.co.kr/", "희귀질환")
