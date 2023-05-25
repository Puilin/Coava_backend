# Coava_backend

2022~2023 컴퓨터캡스톤디자인(졸업과제) 출품작

대화형 아바타 앱 Coava의 백엔드 파트입니다.

## Getting Started


### Prerequisites

* Poetry 

```
curl -sSL https://install.python-poetry.org | python3 -
```
* MySQL (Mac)
```
brew install mysql
```

Windows 환경은 따로 홈페이지 방문하여 설치

### Installing

```poetry.lock``` 파일이 있는 경로에서 다음 명령어 실행

```
poetry install
```

```manage.py``` 파일이 있는 경로에서 다음 명령어를 실행하면 서버를 구동할 수 있습니다.

```
poetry run python manage.py runserver
```

http://127.0.0.1 로 접속하면 api 서버 확인 가능

## Api Endpoints

|기능       |Method        |Path                        |
|----------------|--------------|----------------------------|
|회원가입            |POST          |api/join                    |
|출석체크 목록         |GET           |/api/daily                  |
|출석체크 개별 retrieve|GET, PUT      |/api/daily/<User ID>        |
|Get User ID     |GET           |/api/get_uid?nickname=홍길동   |
|유저정보 조회/수정      |GET, PUT      |api/mypage/<User ID>        |
|내 아바타 조회/수정     |GET, PUT      |api/mypage/avatar/<User ID> |
|내가 갖고 있는 아이템    |GET, PUT      |api/myitem/<User ID>        |
|상점              |GET           |api/shop?section=hat        |
|아이템 사진 받아오기     |GET           |api/item/1                  |
|밈 사전            |GET, POST, PUT|api/meme                    |
|유행어 사전          |GET, POST, PUT|api/buzz                    |
|밈/유행어 썸네일       |GET           |api/thumbnail?type=meme&id=1|
|끝말잇기            |GET           |api/word           |


## Deployment
  
  GCP에서 Computing engine을 통해 배포하였음

## Built With

* <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white"/>
* [Django Rest Framework](https://www.django-rest-framework.org)
* <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=MySQL&logoColor=white"/>

## See also
  
  [개발문서](https://truthful-galaxy-de8.notion.site/ed85d4ffedd24c6eb0c6c459b79091e6?v=c429b8a897d241d7bf9d53fbd7da41d1)
