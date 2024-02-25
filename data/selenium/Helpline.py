from selenium import webdriver
import time

# mongodb 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://192.168.10.236:27017")
database = mongoClient["yugyeongjo"]
collection = database['Helpline']

# chrome browser 열기
browser = webdriver.Chrome()
# 주소 입력
def getBrowserFromURI(uri):
    browser.get(uri)
    return browser

html = browser.page_source
from selenium.webdriver.common.by import By
for i in range(281):
   
    collection.delete_many({})
    browser_helpline = getBrowserFromURI(f"https://helpline.kdca.go.kr/cdchelp/ph/onlCnsl/selectOnlCnslList.do?menu=E0100&pageIndex={i+1}&schGubun=01&schText=")
    pages_elements = browser_helpline.find_elements(by=By.CSS_SELECTOR, value="frm > div > table")
    for x in pages_elements:
        xpath_expression = "//img[contains(@src, 'lock.png')]"
        private_icon = x.find_element(by=By.XPATH, value=xpath_expression)
        if private_icon == True:
            pass
        else:
            post_title = x.find_element(by=By.CSS_SELECTOR, value="tr > td.subject > a > span").click()  # click 들어가기
            # post_title_disease = browser_helpline.find_element(by=By.CSS_SELECTOR, value="div.viewT > dl > dt").text
            # post_date = browser_helpline.find_element(by=By.CSS_SELECTOR, value="dd.btNline > ul > li.tb_time")
            # post_contents = browser_helpline.find_element(by=By.CSS_SELECTOR, value="dl > dd.txt_con > pre")
            # reply_contents = browser_helpline.find_element(by=By.CSS_SELECTOR, value="dl > dd.ans_con > div")
            # post_title = browser_helpline.find_element(by=By.CSS_SELECTOR, value="#btn_list").click()
        pass
pass