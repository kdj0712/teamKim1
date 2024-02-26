# co_data_engineers
#### CLI with Dockerfile and compose.xml : duration 150.4s
```
~$ docker-compose up -d --build

~$ docker-compose build
~$ docker-compose up -d

~$ docker-compose down
~$ docker-compose up -d  # reRun
```
#### samples
- connect mongodb : [samples\sample_mongodb_connection.ipynb](./samples/sample_mongodb_connection.ipynb)

프로젝트명 :RDS
프로젝트 기간: 2023.01.08~2023.01.17

||이름|담당|
|--|--|--|
|1|박요한|PM|
|2|조유경|만능|
|3|김경하|만능|


## 마일스톤
|시작날짜|업무|기간|완료여부|
|--|--|--|--|
|01.10|기획 1차 종합|1d|완|
||업무 분장|당일|완|
|01.11|페이지 프론트 기본 틀 제작|2d|완|
||벡엔드 구상|1d|완|
|01.12|로그인페이지 기본잡기|1d|완|
||로그인 데이터베이스 테스트|1d|완|
||프론트, 데이터베이스 연결 및 확인|1d|완|
|01.13|[질병 데이터 크롤링 제작](https://github.com/entangelk/study_gatheringdatas/blob/main/docs/selenium/disease_save.py)|1d|완|
|01.14|데이터 베이스 더미 제작 및 점검|1d|완|
|01.15|질병 검색 페이지 제작|2d|완|
||페이지네이션 적용|1d|완|
||질병 검색 페이지 데이터베이스 연결|1d|완|
|01.16|유저 데이터베이스, 로그인 회원가입 연결|2d|완|
|01.17|최종 확인(테스트 케이스 작성)|1d||
||각종 문서 작업|1d||



## 주요 파일 리스트
### html
|구분|위치|설명|비고|
|--|--|--|--|
|user|[mainpage.html](./templates/mainpage.html)|메인페이지||
||[login.html](./templates/user/user_login.html)|로그인|ID,PW 유효성 포함|
||[join.html](./templates/user/user_join.html)|회원가입|ID,email 유효성 포함|
||[infosearch.html](./templates/user/user_infosearch.html)|회원정보찾기|email 유효성 포함|
||[privacypolicy.html](./templates/user/user_privacypolicy.html)|약관페이지||
|search|[raredisease.html](./templates/search/search_raredisease.html)|희귀질환 리스트||
|other|[FAQ.html](./templates/other/other_FAQ.html)|FAQ||
||[QnA.html](./templates/other/other_QnA.html)|QnA|게시글 읽기, 쓰기|
|manag|[manager.html](./templates/manag/manag_manager.html)|관리자 페에지|QnA 댓글 작성, 삭제|

### py
|구분|위치|설명|비고|
|--|--|--|--|
|라우트|[mainpage.py](./mainpage.py)|메인페이지 라우트||
||[user.py](./route/user.py)|user하위 라우트||
||[search.py](./route/search.py)|정보찾기 하위 라우트||
||[manag.py](./route/manag.py)|관리자 하위 라우트||
||[other.py](./route/other.py)|기타 하위 라우트||
|컨넥터|[connection.py](./database/connection.py)|서버 컨넥터||
|모델|[member.py](./models/member.py)|user 스키마 모델||
||[QnA.py](./route/QnA.py)|QnA 스키마 모델||
||[FAQ.py](./route/FAQ.py)|FAQ 스키마 모델||
||[disease.py](./route/disease.py)|질병정보 스키마 모델||









```
~$ pip install fastapi uvicorn jinja2
~$ pip install python-multipart
~$ pip install beanie
~$ pip install pydantic
~$ pip install pydantic-settings
~$ pip install pydantic[email]
~$ pip install python-dotenv
```

