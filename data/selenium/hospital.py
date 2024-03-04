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
    iframe = browser.find_elements(by=By.CSS_SELECTOR, value="iframe")
    time.sleep(3)
    browser.switch_to.frame(iframe[4])
    
    # 게시물 리스트 : #idJiwonNm > option////
    elements = browser.find_elements(by=By.CSS_SELECTOR, value="#_pcmap_list_scroll_container > ul > li > div.IPtqD > a:nth-child(1)")
    pass
    for element in elements :
        element.click()
        time.sleep(2)
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
    
    selectCourts(getBrowserFromURI(uri="https://map.naver.com/p/search/%EB%B3%91%EC%9B%90/"))