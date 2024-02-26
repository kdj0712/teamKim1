# 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

# 몽고디비 연결. 같은 collection 내에 연결하되 저장 시에 신문명을 만들어주기!
def dbconnect(collection) :
    mongoClient = MongoClient("mongodb://192.168.10.236:27017/")
    database = mongoClient["skykim"]
    collection = database[collection]
    return collection

# 뉴스 스크래핑하는 부분
def scrappingnews(browser_name) : 
    browser = webdriver.Chrome()
    browser.get(browser_name)
    origin_tab = browser.current_window_handle
    from selenium.webdriver.common.keys import Keys
    previous_scrollHeight = 0
    time.sleep(3)
    while True:
        body = browser.find_element(By.CSS_SELECTOR, "body")
        body.send_keys(Keys.END)
        time.sleep(1)  # 스크롤 동작을 기다립니다.
        current_scrollHeight = browser.execute_script("return document.body.scrollHeight")
        if previous_scrollHeight >= current_scrollHeight:
            break
        else:
            previous_scrollHeight = current_scrollHeight


    element_body = browser.find_elements(by=By.CSS_SELECTOR, value="#main_pack > section > div.api_subject_bx > div.group_news >ul >li")
    # 뉴스명 ====> (개인별 수정 필요!)
    news_comany = '연합뉴스'
    coll_newsscrap = dbconnect("rare_disease_news_2")
    coll_newsscrap.delete_many({})
    for element in element_body :
        try :
            element.find_element(by=By.CSS_SELECTOR, value="div.news_contents > a.news_tit").click()
            browser.switch_to.window(browser.window_handles[1])
            # 스크래핑 시작 ----> (개인별 수정 필요!)
            time.sleep(1)
            news_title = browser.find_element(by=By.CSS_SELECTOR, value="#articleWrap > div.content03 > header > h1").text
            news_description_body = browser.find_elements(by=By.CSS_SELECTOR, value="#articleWrap > div.content01.scroll-article-zone01 > div > div > article > p")
            news_description = ''
            try : 
                for description_p in news_description_body : 
                    # news_description = news_description + browser.find_element(by=By.CSS_SELECTOR, value="#articleWrap > div.content01.scroll-article-zone01 > div > div > article > p")
                    news_description = news_description + description_p.text
            except NoSuchElementException :
                pass
            news_time = browser.find_element(by=By.CSS_SELECTOR, value="#newsUpdateTime01").text
        except NoSuchElementException:
            pass

        coll_newsscrap.insert_one({'news_company' : news_comany, 'news_time' : news_time, 'news_title' : news_title, 'news_description' : news_description})
        browser.close()
        browser.switch_to.window(origin_tab)


if __name__ == "__main__" :
    scrappingnews("https://search.naver.com/search.naver?where=news&query=%ED%9D%AC%EA%B7%80%EC%A7%88%ED%99%98&sm=tab_opt&sort=0&photo=0&field=0&pd=5&ds=2023.02.26&de=2024.02.26&docid=&related=0&mynews=1&office_type=2&office_section_code=8&news_office_checked=1001&nso=so%3Ar%2Cp%3A1y&is_sug_officeid=0&office_category=0&service_area=0")