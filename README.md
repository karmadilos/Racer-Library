###DB 생성
1. 현재 위치를 racer-library로 이동
2. export FLASK_APP=elice_library
3. export FLASK_ENV=development
4. flask db init (최초 한번 수행. 데이터베이스를 관리하는 초기 파일들을 migrations라는 디렉터리에 생성)
5. flask db migrate (모델을 새로 생성하거나 변경할때 사용.)
6. flask db upgrade (모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용)

###실행순서
1. 현재 위치를 racer-library로 이동
2. export FLASK_APP=elice_library
3. export FLASK_ENV=development
4. export FLASK_RUN_RELOAD=False
5. flask run