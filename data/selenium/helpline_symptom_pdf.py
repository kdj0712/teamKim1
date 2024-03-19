from selenium import webdriver                                          # 통상과 동일 
from selenium.webdriver.chrome.service import Service as ChromeService  #
from webdriver_manager.chrome import ChromeDriverManager                # 웹드라이버 매니저 패키지의 chrome 브라우저 관련 설치 기능
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def Connect(): # 전체 과정을 통합한 function의 이름으로 Connect라는 이름을 지정한다
    from pymongo import MongoClient  #몽고 DB 콤파스를 Python 과 연동시킴
    mongoClient = MongoClient("mongodb://trainings.iptime.org:48001/") # 몽고 DB 콤파스의 포트에 연결하는 변수 지정
    database = mongoClient["Seleniums"] # 해당 포트에 접속해서 database에 연결
    collection = database['helpline_Academic'] # 데이터베이스에서 11st_comments 이라는 collection에 연결
    return collection # collection이 반환되도록 지정

webdriver_manager_directory = ChromeDriverManager().install()                    # 23.12.16 추가 구간
driver = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
capabilities = driver.capabilities
for page_num in range(6):
    driver.get(f"https://helpline.kdca.go.kr/cdchelp/ph/infNoti/selectAnnFrmList.do?menu=G0600&pageIndex={page_num+1}&schGubun=tit&schNtbdCcd=03&schText=")
    origin_tab = driver.current_window_handle
    html = driver.page_source
    from selenium.webdriver.common.by import By
    main_board = "#frm > div > table"
    main_body = driver.find_elements(by=By.CSS_SELECTOR, value=main_board) 
    into = "#frm > div > table > tbody > tr > td > a"
    element_buttons = driver.find_elements(by=By.CSS_SELECTOR, value=into)
    time.sleep(2)
    for x in element_buttons:
        try:
            number = driver.find_element(by=By.CSS_SELECTOR, value=f"#frm > div > table > tbody > tr:nth-child({x}) > td:nth-child(1)").text
        except:
            number = ""
            pass
        finally:
            pass

        try:
            title  = driver.find_element(by=By.CSS_SELECTOR, value=f"#frm > div > table > tbody > tr:nth-child({x}) > td.subject").text
        except: # 조건에 맞지 않는 것이 나와도 다른 액션을 취하지 않고 그냥 흘러가도록 지정함
            title = ""
        finally:
            pass
            collection = Connect()
            collection.insert_one({"number":number,"title":title})
            time.sleep(1)
            x.click()
            driver.find_element(by=By.CSS_SELECTOR, value="#divFile3 > dd > a").click()
            time.sleep(2)
            driver.back()
            time.sleep(1)
    # 페이지 로딩 대기

