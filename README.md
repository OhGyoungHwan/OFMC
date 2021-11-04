# OFMC
깔맞춤을 최적화해주는 서비스
SPA로 작동할 것이고 기존 avgcolor를 최적화해서 사용자의 지속적이 사용의 도모한다.

## 필요한 명령어 모음:
pip install --upgrade pip
pip install fastapi
pip install uvicorn[standard]
uvicorn main:app --reload --host=0.0.0.0 --port=80 유니콘을 사용해서 main서버의 앱라우터를 열어서 사용

## 사용한 라이브러리
pip install opencv-python 색상추출을 위해서 사용함
pip install python-multipart multipart/form-data(파일 전송) 형식을 사용하기 위해 쓴다.
pip install jinja2 jinja2템플릿사용함
pip install pandas pandas라이브러리 사용