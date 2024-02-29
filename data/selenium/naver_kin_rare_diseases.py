from selenium import webdriver                                        
from selenium.webdriver.chrome.service import Service as ChromeService  
from webdriver_manager.chrome import ChromeDriverManager              
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import csv
import os
def Connect(database_name, collection_name): 
    from pymongo import MongoClient  
    mongoClient = MongoClient("mongodb://trainings.iptime.org:48001/")
    database = mongoClient[database_name] 
    collection = database[collection_name]
    return collection 

dise_names = []
diseases_col = Connect('teamplays','diseases')
dise_name = list(diseases_col.find({},{"dise_name_kr" : 1 }))
for j in range(len(dise_name)):
    dise_names.append(dise_name[j]['dise_name_kr'])
pass

if os.path.isfile('last_processed.txt') and os.path.getsize('last_processed.txt') > 0:
    with open('last_processed.txt', 'r', encoding='utf-8') as f:
        content = f.read().strip()
        last_dise_name, last_page_num = content.rsplit(',', 1)
        last_dise_name = last_dise_name.strip('"')
        last_page_num = int(last_page_num.strip('"'))

else:
    last_dise_name = dise_names[0]
    last_page_num = 1

last_dise_index = dise_names.index(last_dise_name)
last_page_num = int(last_page_num)
webdriver_manager_directory = ChromeDriverManager().install()
options = Options()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=ChromeService(webdriver_manager_directory),options=options)
driver.set_page_load_timeout(10) 
driver.implicitly_wait(10)
apabilities = driver.capabilities
for k in range(last_dise_index, len(dise_names)):
    if k == last_dise_index:
        start_page_num = last_page_num
        page_num = start_page_num
    else:
        start_page_num = 1
    for page_num in range(start_page_num, 21):
        page_num
        driver.get(f"https://kin.naver.com/search/list.naver?query={dise_names[k]}&page={page_num}")
        origin_tab = driver.current_window_handle
        html = driver.page_source
        from selenium.webdriver.common.by import By
        main_board = "#s_content > div.section"
        element_body = driver.find_elements(by=By.CSS_SELECTOR, value=main_board) 
        main_body = driver.find_elements(by=By.CSS_SELECTOR, value=main_board) 
        main_question_title = "#s_content > div.section > ul > li > dl > dt > a"
        main_questions = driver.find_elements(by=By.CSS_SELECTOR,value=main_question_title)
        for question in main_questions:
            question.click()
            all_tabs = driver.window_handles
            new_tab = [tab for tab in all_tabs if tab != origin_tab][0]
            driver.switch_to.window(new_tab)
            wait = WebDriverWait(driver, 10)
            try:
                elements_switched_tab = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content")))

                for items in elements_switched_tab:
                    try:
                        element_question_title = items.find_element(by=By.CSS_SELECTOR, value="div.c-heading._questionContentsArea.c-heading--default-old > div.c-heading__title > div > div.title")
                        
                        question_title = element_question_title.text
                    except:
                        question_title = ""
                        pass
                    finally:
                        pass
                    try:
                        element_question_content  = items.find_element(by=By.CSS_SELECTOR, value="div.c-heading._questionContentsArea.c-heading--default-old > div.c-heading__content")
                        question_content  = element_question_content.text
                    except: 
                        question_content = ""
                    finally:
                        pass
                    try:
                        element_question_datetime = items.find_element(by=By.CSS_SELECTOR, value="div.c-userinfo__left > span:nth-child(2)")
                        question_datetime = element_question_datetime.text
                    except:
                        question_datetime = ""
                        pass
                    finally:
                        pass
                    answers = {}
                    answer_elements = driver.find_elements(by=By.CSS_SELECTOR, value="div._endContents.c-heading-answer__content")
                    for i in range(1, 4):
                        if i <= len(answer_elements):
                            answer_element = answer_elements[i-1]
                            content_elements = answer_element.find_elements(by=By.CSS_SELECTOR, value="div._endContentsText.c-heading-answer__content-user")
                            if content_elements:
                                content = content_elements[0].text
                            else:
                                content = None
                            datetime_elements = answer_element.find_elements(by=By.CSS_SELECTOR, value="p.c-heading-answer__content-date")
                            if datetime_elements:
                                datetime = datetime_elements[0].text
                            else:
                                datetime = None
                        else:
                            content = None
                            datetime = None

                        answers[f"answer{i}_content"] = content
                        answers[f"answer{i}_datetime"] = datetime
                driver.close()
                driver.switch_to.window(origin_tab)
                collection = Connect('project','naver_kin_rare_diseases')
                collection.insert_one({"dise_name":dise_names[k],"question_title":question_title,"question_content":question_content,"question_datetime":question_datetime,**answers})
                with open('last_processed.txt', 'w', encoding='utf-8') as f:
                    f.write(f'"{dise_names[k]}","{page_num}"')
            except TimeoutException:
                driver.close()
                driver.switch_to.window(origin_tab)
                continue  # 다음 반복으로 넘어가기
        try:
            next_page_button = driver.find_element(by=By.CSS_SELECTOR, value="#s_content > div.section > div.s_paging > a.next._nclicks\:kin\.next")
            page_num += 1
           
        except NoSuchElementException:
            break


