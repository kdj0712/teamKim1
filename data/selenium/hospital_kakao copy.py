from selenium import webdriver                                          # 통상과 동일 
from selenium.webdriver.chrome.service import Service as ChromeService  #
from webdriver_manager.chrome import ChromeDriverManager                # 웹드라이버 매니저 패키지의 chrome 브라우저 관련 설치 기능
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def dbconnect(): # 전체 과정을 통합한 function의 이름으로 Connect라는 이름을 지정한다
    from pymongo import MongoClient  #몽고 DB 콤파스를 Python 과 연동시킴
    mongoClient = MongoClient("mongodb://trainings.iptime.org:48001/") # 몽고 DB 콤파스의 포트에 연결하는 변수 지정
    database = mongoClient["Seleniums"] # 해당 포트에 접속해서 database에 연결
    collection = database['kakao_hospital_reviews'] # 데이터베이스에서 11st_comments 이라는 collection에 연결
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



def search(browser):
    time.sleep(2)
    search = browser.find_element(by=By.CSS_SELECTOR, value="#search\.keyword\.query")
    search.send_keys("병원")
    button = browser.find_element(by=By.CSS_SELECTOR, value="#search\.keyword\.submit")
    button.click()

def pagination(browser) :
    time.sleep(1)
    try :         
        more_button = browser.find_element(by=By.CSS_SELECTOR, value="#info\.search\.place\.more")
        more_button.click()
    except :
        pass
    time.sleep(1)
    pagination = browser.find_elements(by=By.CSS_SELECTOR, value="#info\.search\.page > div > a")
    return pagination

def click_next_page(browser) :
    next_page = browser.find_element(by=By.CSS_SELECTOR, value="#info\.search\.page\.next")
    next_page.click

def pagination_loop(browser, i) :        
    time.sleep(1)
    pagination_elements[i].click()
    # 병원 리스트 : 
    elements = browser.find_elements(by=By.CSS_SELECTOR, value="#info\.search\.place\.list > li > div.head_item.clickArea > strong > a.link_name")
    origin_tab = browser.current_window_handle
    pass
    return elements, origin_tab
    
def scrapping(browser, origin_tab, x) :    
        # 병원 개수 만큼 반복
        time.sleep(1)
        hospital = browser.find_elements(by=By.CSS_SELECTOR, value="#info\.search\.place\.list > li")[x]
        hospital_name = hospital.find_element(by=By.CSS_SELECTOR, value="div.head_item.clickArea > strong > a.link_name").text
        hospital_reviews = hospital.find_element(by=By.CSS_SELECTOR, value="div.rating.clickArea > span.score > a")
            # 병원 리뷰 페이지로 이동
        #info\.search\.place\.list > li:nth-child(14) > div.rating.clickArea > span.txt_blind
        if hospital_reviews.text == '0건'or hospital_reviews.text=='' :
            pass
        else :
            hospital_reviews.click()
            time.sleep(2)
            browser.switch_to.window(browser.window_handles[1])
            more_review(browser)
            contents = browser.find_elements(by=By.CSS_SELECTOR, value="#mArticle > div.cont_evaluation > div.evaluation_review > ul > li > div.comment_info > p > span")
            for content in contents :
                try : 
                    text = content.text
                except :
                    text = ''
                pass
                collection.insert_one({'hospital_name':hospital_name, 'text':text})
            browser.close()
            browser.switch_to.window(origin_tab)
            

def more_review(browser):
    while True :
        time.sleep(1)
        try :
            if browser.find_element(by=By.CSS_SELECTOR, value="#mArticle > div.cont_evaluation > div.evaluation_review > a").text != '후기 더보기' : 
                break
            else :
                more_element = browser.find_element(by=By.CSS_SELECTOR, value="#mArticle > div.cont_evaluation > div.evaluation_review > a")
                more_element.click()
        except :
            break
                    

def quitBrowser(browser):
    # 브라우저 종료
    browser.quit()
    return 0

if __name__ == "__main__" :
    collection = dbconnect()
    browser = getBrowserFromURI(uri="https://map.kakao.com/?referrer=daumtop")
    search(browser=browser)
    while True :
        pagination_elements = pagination(browser=browser)
        for i in range(len(pagination_elements)) :
            elements, origin_tab = pagination_loop(browser, i)
            for x in range(len(elements)) :
                scrapping(browser, origin_tab, x)
        click_next_page(browser)
        pass
            


