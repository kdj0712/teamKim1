# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

def function_name():
    pass
    return 0

#  기능 functioin : 한 업무에 종속성이 없는 것
#  uri에 의한 Browser 가져오기
def getBrowserFromURI(uri):
    webdriver_manager_directory = ChromeDriverManager().install()

    # ChromeDriver 실행
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

    # Chrome WebDriver의 capabilities 속성 사용
    capabilities = browser.capabilities

    # - 주소 입력(https://www.w3schools.com/)
    browser.get(uri)
    return browser



def selectCourts(browser):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    # 게시물 리스트 : #idJiwonNm > option////
    element_post = browser.find_elements(by=By.CSS_SELECTOR, value="#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr.ub-content")

    for index in range(len(element_post)) :
        select_post = Select(browser.find_element(by=By.CSS_SELECTOR, value=f"table > tbody > tr:nth-child({index+1}) > td.gall_tit.ub-word > a:nth-child(1)")) 
        select_post.click()
        time.sleep(2)
        dc_title = Select(browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > header > div > h3 > span.title_subject")) 
        dc_title_text = dc_title.text
        dc_name = Select(browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > header > div > div > div.fl > span.nickname")) 
        dc_name_text = dc_name.text
        dc_date = Select(browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > header > div > div > div.fl > span.gall_date")) 
        dc_date_text = dc_date.text
        dc_contents = Select(browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > div > div.inner.clear > div.writing_view_box > div.write_div")) 
        dc_contents_text = dc_contents.text
        print(f"title: {dc_title_text}, name: {dc_name_text}, date: {dc_date_text}, contents: {dc_contents_text}")
        browser.back()
        pass
    pass
    return len(element_post)

def quitBrowser(browser):
    # 브라우저 종료
    browser.quit()
    return 0

if __name__ == "__main__" :
    selectCourts(getBrowserFromURI(uri="https://gall.dcinside.com/mgallery/board/lists?id=raredisease"))