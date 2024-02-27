from selenium import webdriver
import time

# mongodb 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://192.168.10.236:27017")
database = mongoClient["project"]
collection = database['Helpline_info']

# chrome browser 열기
browser = webdriver.Chrome()
# 주소 입력
def getBrowserFromURI(uri):
    browser.get(uri)
    return browser

html = browser.page_source
from selenium.webdriver.common.by import By

collection.delete_many({})
for i in range(126):
    browser_helpline = getBrowserFromURI(f"https://helpline.kdca.go.kr/cdchelp/ph/rdiz/selectRdizInfList.do?menu=A0100&pageIndex={i+1}&fixRdizInfTab=&rdizCd=&schKor=&schEng=&schCcd=&schGuBun=dizNm&schText=&schSort=kcdCd&schOrder=desc")
    pages_elements = browser_helpline.find_elements(by=By.CSS_SELECTOR, value="#frm > div > table")
    for x in range(len(pages_elements)):
        browser_helpline.find_element(by=By.CSS_SELECTOR, value="td:nth-child(3) > a").click()
        time.sleep(2)
        disease_name = browser_helpline.find_element(by=By.CSS_SELECTOR, value="tr > td.subject > em").text
        relative_disease = browser_helpline.find_element(by=By.CSS_SELECTOR, value="table.dic_viewT > tbody > tr:nth-child(1) > td:nth-child(2)").text
        symptom = browser_helpline.find_element(by=By.CSS_SELECTOR, value="tr:nth-child(2) > td:nth-child(2) > pre").text
        cause = browser_helpline.find_element(by=By.CSS_SELECTOR, value="tr:nth-child(2) > td:nth-child(4) > pre").text
        browser_helpline.find_element(by=By.CSS_SELECTOR, value="#frm > div > p.btn_areaR.three > button").click()
        time.sleep(2)
        collection.insert_one({'disease_name': disease_name, 'relative_disease': relative_disease, 'symptom': symptom, 'cause': cause})
    