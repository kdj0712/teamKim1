from selenium import webdriver                                          # 통상과 동일 
from selenium.webdriver.chrome.service import Service as ChromeService  #
from webdriver_manager.chrome import ChromeDriverManager           # 웹드라이버 매니저 패키지의 chrome 브라우저 관련 설치 기능
import time
webdriver_manager_directory = ChromeDriverManager().install()                    # 23.12.16 추가 구간
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
capabilities = browser.capabilities
browser.get("https://play.google.com/store/apps/details?id=com.humanscape.rarenote&hl=ko-KR")
time.sleep(3)
html = browser.page_source
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
def Connect(): # 전체 과정을 통합한 function의 이름으로 Connect라는 이름을 지정한다
    from pymongo import MongoClient  #몽고 DB 콤파스를 Python 과 연동시킴
    mongoClient = MongoClient("mongodb://trainings.iptime.org:48001/") # 몽고 DB 콤파스의 포트에 연결하는 변수 지정
    database = mongoClient["project"] # 해당 포트에 접속해서 database에 연결
    collection = database['reviews'] # 데이터베이스에서 11st_comments 이라는 collection에 연결
    return collection # collection이 반환되도록 지정


button = "#yDmH0d > c-wiz.SSPGKf.Czez9d > div > div > div:nth-child(1) > div.tU8Y5c > div.wkMJlb.YWi3ub > div > div.qZmL0 > div:nth-child(1) > c-wiz:nth-child(4) > section > div > div.Jwxk6d > div:nth-child(5) > div > div > button > span"
comment_button = browser.find_element(by=By.CSS_SELECTOR, value=button)
comment_button.click()

modal_body = "div > div.fysCi"
elements_scrollableDiv = browser.find_element(by=By.CSS_SELECTOR, value=modal_body)

comments = "div.RHo1pe"
elements_comment = browser.find_elements(by=By.CSS_SELECTOR, value=comments)
print("Count Comment before done scroll : {}".format(len(elements_comment)))

previous_scrollHeight = 0
# browser.execute_script("var scrollableDiv = document.querySelector('div.fysCi');")
# browser.execute_script("scrollableDiv.scrollTo(0, scrollableDiv.scrollHeight);")
while True:
    # python 방식 변수 매칭
    # print("{0}.scrollTo{1},{0}.scrollHeight);".format(elements_scrollableDiv,previous_scrollHeight))
    # javascript와 python 결합 방식 변수 매칭
    browser.execute_script("arguments[0].scrollTo(arguments[1], arguments[0].scrollHeight);"
                                                  ,elements_scrollableDiv, previous_scrollHeight)
    current_scrollheight = browser.execute_script("return arguments[0].scrollHeight;"
                                                  ,elements_scrollableDiv)
    if previous_scrollHeight >= current_scrollheight:
    # 만약 전체 높이와 비교하여 남아있는 공간이 없다면 행동을 멈추도록 선언한다.
        break
    else:
        previous_scrollHeight = current_scrollheight
        # 그렇지 않다면 해당 내용이 같아질 떄까지 반복한다.
    time.sleep(5)
    # 행동을 반복할 텀을 1초정도 준다. 반복이 진행되면서 페이지가 로딩이 될 여유를 준다.
  
    comments = "div.RHo1pe"
    elements_comment = browser.find_elements(by=By.CSS_SELECTOR, value=comments)
    print("Count Comment after done scroll : {}".format(len(elements_comment)))

    pass

pass
for comment in elements_comment:
    try:
        co_date  = comment.find_element(by=By.CSS_SELECTOR, value="#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.HQdjr.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div > div > div > div.fysCi > div > div:nth-child(2) > div > header > div.Jx4nYe > span").text
    except: # 조건에 맞지 않는 것이 나와도 다른 액션을 취하지 않고 그냥 흘러가도록 지정함
        co_date = ""
    finally:
        pass

    try:
        co_review = comment.find_element(by=By.CSS_SELECTOR, value="#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.HQdjr.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div > div > div > div.fysCi > div > div:nth-child(2) > div > div.h3YV2d").text
        # 가져온 items의 내용물을 비교하여 value에 지정한 값과 같은 것을 찾는다면, 그것을 element_point라는 변수로 선언한다.
    except:
        co_review = ""
        pass
    finally:
        pass

    collection = Connect()
    collection.insert_one({"co_date":co_date,"co_review":co_review})
    time.sleep(2)
    # 페이지 로딩 대기

