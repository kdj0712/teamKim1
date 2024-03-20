
from selenium import webdriver
import time
from selenium import webdriver                                          # 통상과 동일 
from selenium.webdriver.chrome.service import Service as ChromeService  #
from webdriver_manager.chrome import ChromeDriverManager                # 웹드라이버 매니저 패키지의 chrome 브라우저 관련 설치 기능
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


# mongodb 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://192.168.10.236:27017")
database = mongoClient["teamkim"]
collection = database['trend_documents']

webdriver_manager_directory = ChromeDriverManager().install()

# ChromeDriver 실행
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

# Chrome WebDriver의 capabilities 속성 사용
capabilities = browser.capabilities
# chrome browser 열기

# 주소 입력
def getBrowserFromURI(uri):
    browser.get(uri)
    return browser

html = browser.page_source
from selenium.webdriver.common.by import By

collection.delete_many({})
for i in range(13):
    browser_helpline = getBrowserFromURI(f"https://helpline.kdca.go.kr/cdchelp/ph/infNoti/selectFrmDocList.do?menu=G0400&pageIndex={i+1}&schGubun=tit&schNtbdCcd=02&schText=")
    pages_elements = browser_helpline.find_elements(by=By.CSS_SELECTOR, value="#frm > div > table > tbody > tr")
    for element in pages_elements :
        post_click = element.find_element(by=By.CSS_SELECTOR, value="td.subject>a")  
        post_title = post_click.text
        post_click.click()# click 들어가기
        try : 
            time.sleep(1)
            post_file_name_text = ''
            post_file_name = browser_helpline.find_elements(by=By.CSS_SELECTOR, value="#divFile3 > dd > a")
            for x in range(len(post_file_name)) :
                    time.sleep(1)
                    post_file_name[x].click()
                    time.sleep(1)
                    post_file_name_text += post_file_name[x].text+';'
                    time.sleep(1)
        except :
            post_file_name_text=''
        post_contents = browser_helpline.find_element(by=By.CSS_SELECTOR, value="#frm > div > div > dl.tit_con > dd.txt_con.edtTxt").text

        collection.insert_one({'post_title':post_title,'post_file_name': post_file_name_text, 'post_contents': post_contents})
        browser_helpline.back()
    pass
pass