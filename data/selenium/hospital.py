# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

def dbconnect(): # 전체 과정을 통합한 function의 이름으로 Connect라는 이름을 지정한다
    from pymongo import MongoClient  #몽고 DB 콤파스를 Python 과 연동시킴
    mongoClient = MongoClient("mongodb://trainings.iptime.org:48001/") # 몽고 DB 콤파스의 포트에 연결하는 변수 지정
    database = mongoClient["hospital"] # 해당 포트에 접속해서 database에 연결
    collection = database['reviews'] # 데이터베이스에서 11st_comments 이라는 collection에 연결
    return collection # collection이 반환되도록 지정

#  기능 functioin : 한 업무에 종속성이 없는 것
#  uri에 의한 Browser 가져오기
def getBrowserFromURI(uri):
    webdriver_manager_directory = ChromeDriverManager().install()

    # ChromeDriver 실행
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

    # Chrome WebDriver의 capabilities 속성 사용
    capabilities = browser.capabilities

    # - 주소 입력
    browser.get(uri)
    return browser



def selectCourts(browser, collection):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    time.sleep(2)
    while True : 
        browser.switch_to.default_content()
        iframe_element = browser.find_element(By.ID, "searchIframe")
        browser.switch_to.frame(iframe_element)
        
        # 게시물 리스트 : #idJiwonNm > option////
        elements = browser.find_elements(by=By.CSS_SELECTOR, value="#_pcmap_list_scroll_container > ul > li > div.IPtqD > a:nth-child(1)")
        pass
        for element in elements :
            
            hospital_name = element.find_element(by=By.CSS_SELECTOR, value="div.LYTmB > div > span").text
            element.click()
            time.sleep(2)
            browser.switch_to.default_content()
            iframe_element = browser.find_element(By.ID, "entryIframe")
            browser.switch_to.frame(iframe_element)
            browser.find_element(by=By.CSS_SELECTOR, value="#app-root > div > div > div > div.place_fixed_maintab > div > div > div > div > a:nth-child(2)").click()
            
            while True :
                time.sleep(2)
                try  :
                    more_element = browser.find_element(by=By.CSS_SELECTOR, value="#app-root > div > div > div > div> div > div.place_section.k5tcc > div.NSTUp > div > a")
                    more_element.click()
                except : 
                    break
                pass
            pass 
            
            contents = browser.find_elements(by=By.CSS_SELECTOR, value="#app-root > div > div > div > div:nth-child(6) > div:nth-child(2) > div.place_section.k5tcc > div > ul > li > div.ZZ4OK > a")
            for content in contents :
                try : 
                    content.click()
                    text = content.text
                except :
                    text = ''
                pass
                collection.insert_one({'hospital_name':hospital_name, 'text':text})
            pass


            browser.switch_to.default_content()
            iframe_element = browser.find_element(By.ID, "searchIframe")
            browser.switch_to.frame(iframe_element)
        
        pass
        
        # dc_title = Select(element.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > header > div > h3 > span.title_subject")) 
        # dc_title_text = dc_title.text
        # dc_name = Select(element.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > header > div > div > div.fl > span.nickname")) 
        # dc_name_text = dc_name.text
        # dc_date = Select(element.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > header > div > div > div.fl > span.gall_date")) 
        # dc_date_text = dc_date.text
        # dc_contents = Select(element.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > div > div.inner.clear > div.writing_view_box > div.write_div")) 
        # dc_contents_text = dc_contents.text
        # print(f"title: {dc_title_text}, name: {dc_name_text}, date: {dc_date_text}, contents: {dc_contents_text}")
        # browser.back()
        pass
    pass
    return 

def quitBrowser(browser):
    # 브라우저 종료
    browser.quit()
    return 0

if __name__ == "__main__" :
    collection = dbconnect()
    selectCourts(getBrowserFromURI(uri="https://map.naver.com/p/search/%EB%B3%91%EC%9B%90/"), collection)