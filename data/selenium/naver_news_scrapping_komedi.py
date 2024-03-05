# 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager    
import time
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 몽고디비 연결. 같은 collection 내에 연결하되 저장 시에 신문명을 만들어주기!
def dbconnect(collection) :
    mongoClient = MongoClient("mongodb://192.168.10.236:27017/")
    database = mongoClient["skykim"]
    collection = database[collection]
    return collection

# 뉴스 스크래핑하는 부분
def scrappingnews(browser_name) : 
    webdriver_manager_directory = ChromeDriverManager().install() 
    driver = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
    capabilities = driver.capabilities
    driver.get(browser_name)
    origin_tab = driver.current_window_handle
    html = driver.page_source
    from selenium.webdriver.common.keys import Keys
    previous_scrollHeight = 0
    time.sleep(3)
    while True:
        body = driver.find_element(By.CSS_SELECTOR, "body")
        body.send_keys(Keys.END)
        time.sleep(1)  # 스크롤 동작을 기다립니다.
        current_scrollHeight = driver.execute_script("return document.body.scrollHeight")
        if previous_scrollHeight >= current_scrollHeight:
            break
        else:
            previous_scrollHeight = current_scrollHeight


    element_body = driver.find_elements(by=By.CSS_SELECTOR, value="#main_pack > section > div.api_subject_bx > div.group_news >ul >li")
    # 뉴스명 ====> (개인별 수정 필요!)
    news_comany = '코메디닷컴'
    coll_newsscrap = dbconnect("rare_disease_news_komedi")
    coll_newsscrap.delete_many({})
    for element in element_body:
        try :
            time.sleep(5)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable(element.find_element(By.CSS_SELECTOR, "div > div > div.news_contents > a.news_tit").click()))
            
            all_tabs = driver.window_handles
            new_tab = [tab for tab in all_tabs if tab != origin_tab][0]
            driver.switch_to.window(driver.new_tab)
            # 스크래핑 시작 ----> (개인별 수정 필요!)
            time.sleep(1)
            news_title = driver.find_element(by=By.CSS_SELECTOR, value="# div.post-header-inner > div > h1 > span").text
            news_description_body = driver.find_elements(by=By.CSS_SELECTOR, value="#post-1658943 > p")
            news_description = ''
            try : 
                for description_p in news_description_body : 
                    # news_description = news_description + browser.find_element(by=By.CSS_SELECTOR, value="#articleWrap > div.content01.scroll-article-zone01 > div > div > article > p")
                    news_description = news_description + description_p.text
            except NoSuchElementException :
                pass
            news_time = driver.find_element(by=By.CSS_SELECTOR, value="#span.time.meta_web > time > b").text
        except NoSuchElementException:
            pass

        coll_newsscrap.insert_one({'news_company' : news_comany, 'news_time' : news_time, 'news_title' : news_title, 'news_description' : news_description})
        driver.close()
        driver.switch_to.window(origin_tab)


if __name__ == "__main__" :
    scrappingnews("https://search.naver.com/search.naver?where=news&query=%ED%9D%AC%EA%B7%80%EC%A7%88%ED%99%98&sm=tab_opt&sort=0&photo=0&field=0&pd=5&ds=2023.02.27&de=2024.02.27&docid=&related=0&mynews=1&office_type=2&office_section_code=11&news_office_checked=1296&nso=so%3Ar%2Cp%3A1y&is_sug_officeid=0&office_category=0&service_area=0")
