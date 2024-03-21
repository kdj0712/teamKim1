from apscheduler.schedulers.background import BackgroundScheduler

# 정의한 함수 불러오기
from schedular.news_scrappnig_weekly import bosascrapping
from schedular.news_recommend import

if __name__ == "__main__" : 
    schedular = BackgroundScheduler()
    schedular.add_job(bosascrapping("http://www.bosa.co.kr/", "희귀질환"), trigger="interval", seconds=604800, coalesce=True, max_instances=1) #주기 설정 필요
    