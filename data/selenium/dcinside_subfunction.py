# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from pymongo import MongoClient
def dbconnect(collection_name) :
    # MongoDB 클라이언트 설정
    mongoClient = MongoClient("mongodb://192.168.10.236:27017/")
    database = mongoClient["project"]
    collection = database[collection_name]
    return collection

#  uri에 의한 Browser 가져오기
def getBrowserFromURI(uri):
    webdriver_manager_directory = ChromeDriverManager().install()
    # ChromeDriver 실행
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
    
    # - 주소 입력
    browser.get(uri)
    return browser


def selectCourts(browser):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    # 게시물 리스트 : #idJiwonNm > option////
    element_post = browser.find_elements(by=By.CSS_SELECTOR, value="#container > section.left_content > article > div.gall_listwrap.list > table > tbody > tr.ub-content.us-post")

    for element in element_post :
        time.sleep(2)
        # dc_select_post = browser.find_element(by=By.CSS_SELECTOR, value=f"table > tbody > tr:nth-child({index+2}) > td.gall_tit.ub-word > a:nth-child(1)")
        # dc_select_post.click()
        dc_cate = element.find_element(by=By.CSS_SELECTOR, value="#container > section.left_content > article > div.gall_listwrap.list > table > tbody > tr > td.gall_num")
        dc_cate_text = dc_cate.text
        if dc_cate.text !='공지' and dc_cate.text != '설문' :
            element.find_element(by=By.CSS_SELECTOR, value="a").click()    
            dc_title = browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article > div.view_content_wrap > header > div > h3 > span.title_subject")
            dc_title_text = dc_title.text
            dc_date = browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article > div.view_content_wrap > header > div > div > div.fl > span.gall_date")
            dc_date_text = dc_date.text
            dc_content = browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article > div.view_content_wrap > div > div.inner.clear > div.writing_view_box > div.write_div")
            dc_content_text = dc_content.text
            try : 
                dc_up = browser.find_element(by=By.CSS_SELECTOR, value=f"#recommend_view_up_{dc_cate_text}")
                dc_up_text = dc_up.text
            except : 
                dc_up_text = ''
            try : 
                dc_down = browser.find_element(by=By.CSS_SELECTOR, value=f"#recommend_view_down_{dc_cate_text}")
                dc_down_text = dc_down.text
            except : 
                dc_down_text = ''
            try :
                dc_comments = [] 
                dc_comment = browser.find_elements(by=By.CSS_SELECTOR, value="div > p.usertxt.ub-word")
                for comment in dc_comment :
                    dc_comments.append(comment.text)
            except : 
                dc_comment_text = ''
            dcinside = dbconnect('dcinside')
            dcinside.insert_one({'title': dc_title_text, 'date':dc_date_text, 'contents': dc_content_text, 'up':dc_up_text, 'down':dc_down_text, 'comment':dc_comments})
            browser.set_page_load_timeout(10)
            browser.back()
        
        pass
    pass
    return len(element_post)

def quitBrowser(browser):
    # 브라우저 종료
    browser.quit()
    return 0

if __name__ == "__main__" :
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    # Chrome 옵션 설정
    options = Options()
    options.add_argument('--ignore-certificate-errors')

    for dc_page_num in [1,2,3,4,5,6,7,8,9,10] :
        time.sleep(2)
        browser = getBrowserFromURI(uri=f"https://gall.dcinside.com/mgallery/board/lists?id=raredisease&page={dc_page_num}")
        selectCourts(browser)
        quitBrowser(browser)