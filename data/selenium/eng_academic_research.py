from selenium import webdriver
import time

# mongodb 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://192.168.10.236:27017")
database = mongoClient["Seleniums"]
collection = database['eng_academic_research']

# chrome browser 열기
browser = webdriver.Chrome()
from selenium.webdriver.common.by import By

# mongo reset
collection.delete_many({})

# 주소 입력
for i in range(1467):
    uri = f"https://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery=rare+diseases&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount={i*10}&orderBy=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&ccl_code=&inside_outside=&fric_yn=&db_type=&image_yn=&gubun=&kdc=&ttsUseYn=&l_sub_code=&fsearchMethod=search&sflag=1&isFDetailSearch=N&pageNumber=1&resultKeyword=rare+diseases&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=re_a_kor&colName=re_a_kor&pageScale=10&isTab=Y&regnm=&dorg_storage=&language=&language_code=&clickKeyword=&relationKeyword=&query=rare+diseases"
    browser.get(uri)
    html = browser.page_source

    num_button = browser.find_elements(by=By.CSS_SELECTOR, value="#divContent > div > div.rightContent.wd756 > div > div.paging > a")

    while True:
        try : 
            pages_elements = browser.find_elements(by=By.CSS_SELECTOR, value="#divContent > div > div.rightContent.wd756 > div > div.srchResultW > div.srchResultListW")
            posts_elements = browser.find_elements(by=By.CSS_SELECTOR, value="div.cont.ml60 > p.title > a")
            for element in posts_elements:
                element.click()
                research_title = browser.find_element(by=By.CSS_SELECTOR, value="#thesisInfoDiv > div.thesisInfoTop > h3").text
                research_url = browser.find_element(by=By.CSS_SELECTOR, value="#thesisInfoDiv > div.infoDetail.on > p").text
                research_author = browser.find_element(by=By.CSS_SELECTOR, value="ul > li:nth-child(1) > div > p").text
                research_institution = browser.find_element(by=By.CSS_SELECTOR, value="ul > li:nth-child(2) > div > p > a").text
                research_name = browser.find_element(by=By.CSS_SELECTOR, value="ul > li:nth-child(3) > div > p > a").text
                research_volumn = browser.find_element(by=By.CSS_SELECTOR, value="ul > li:nth-child(4) > div > p").text
                research_year = browser.find_element(by=By.CSS_SELECTOR, value="ul > li:nth-child(5) > div > p").text
                research_language = browser.find_element(by=By.CSS_SELECTOR, value="ul > li:nth-child(6) > div > p").text
                research_subject = browser.find_element(by=By.CSS_SELECTOR, value="ul > li:nth-child(7) > div > p").text
                research_type = browser.find_element(by=By.CSS_SELECTOR, value="ul > li:nth-child(8) > div > p").text
                research_page = browser.find_element(by=By.CSS_SELECTOR, value="ul > li:nth-child(9) > div > p").text
                # browser.back()
            
                collection.insert_one({'research_title': research_title
                                    , 'research_url': research_url
                                    , 'research_author': research_author
                                    , 'research_institution': research_institution
                                    , 'research_name': research_name
                                    , 'research_volumn': research_volumn
                                    , 'research_year': research_year
                                    , 'research_language': research_language
                                    , 'research_subject': research_subject
                                    , 'research_type': research_type
                                    , 'research_page': research_page
                                    })
                browser.back()
                time.sleep(3)
        except : 
            break