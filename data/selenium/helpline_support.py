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
    database = mongoClient["project"] # 해당 포트에 접속해서 database에 연결
    collection = database['helpline_Support'] # 데이터베이스에서 11st_comments 이라는 collection에 연결
    return collection # collection이 반환되도록 지정

webdriver_manager_directory = ChromeDriverManager().install()                    # 23.12.16 추가 구간
driver = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
capabilities = driver.capabilities
for page_num in range(1,129):
    driver.get(f"https://helpline.kdca.go.kr/cdchelp/ph/supbiz/selectMdepSupList.do?menu=B0102&pageIndex={page_num}&schGubun=tit&schSuplDcd=&schText=")
    # origin_tab = driver.current_window_handle
    # html = driver.page_source
    from selenium.webdriver.common.by import By
    time.sleep(1)
  
    table = driver.find_elements(by=By.CSS_SELECTOR, value= "#frm > div > table > tbody > tr")
    for i in table:
        try:
            disease_number = i.find_element(by=By.CSS_SELECTOR, value="th").text
        except:
            disease_number = ""
            pass
        finally:
            pass

        try:
            dise_name  = i.find_element(by=By.CSS_SELECTOR, value="td > dl > dt").text
        except: # 조건에 맞지 않는 것이 나와도 다른 액션을 취하지 않고 그냥 흘러가도록 지정함
            dise_name = ""
        finally:
            pass

        try:
            KCD_code = i.find_element(by=By.CSS_SELECTOR, value="td > dl > dd > ul > li:nth-child(1)").text
            # 가져온 items의 내용물을 비교하여 value에 지정한 값과 같은 것을 찾는다면, 그것을 element_point라는 변수로 선언한다.
        except:
            KCD_code = ""
            pass
        finally:
            pass

        try:
            sanjung_code = i.find_element(by=By.CSS_SELECTOR, value="td > dl > dd > ul > li:nth-child(2)").text
            # 가져온 items의 내용물을 비교하여 value에 지정한 값과 같은 것을 찾는다면, 그것을 element_point라는 변수로 선언한다.
        except:
            sanjung_code = ""
            pass
        finally:
            pass

        try:
            support_content = i.find_element(by=By.CSS_SELECTOR, value="td > dl > dd > ul > li:nth-child(3)").text
            # 가져온 items의 내용물을 비교하여 value에 지정한 값과 같은 것을 찾는다면, 그것을 element_point라는 변수로 선언한다.
        except:
            support_content = ""
            pass
        finally:
            pass

        collection = Connect()
        collection.insert_one({"disease_number":disease_number,"dise_name":dise_name,"KCD_code":KCD_code, "sanjung_code":sanjung_code, "support_content":support_content})
        time.sleep(2)
    # 페이지 로딩 대기

