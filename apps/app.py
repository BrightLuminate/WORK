from pathlib import Path # 경로 처리를 위한 기본 라이브러리
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy를 인스턴스화한다.
db = SQLAlchemy()   # 객체 생성 db로 다룰것이다.


# create_app 함수를 작성한다.
def create_app():
    # 플라스크 인스턴스 생성
    app = Flask(__name__)
# 앱의 config 설정을 한다.
    app.config.from_mapping(
      SECRET_KEY="2AZSMss3p5QPbcYBsJ", # 자체적으로 이름 정할수도 있다.
        SQLALCHEMY_DATABASE_URI=
            f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",  #경로 현파일에 경로를 가져온다. / parent 지금 파일 들어온 경로
        SQLALCHEMY_TRACK_MODIFICATIONS=False # 경과 안나온못 False를 쓴다.
  )

    # SQLAlchemy 와 앱을 연계한다. 
    db.init_app(app)
    # Migrate와 앱을 연계한다. 
    Migrate(app, db)

   
    from apps.crud import views as crud_views
    # blueprint 는 기본주소뒤에는 루트에 키워드 있다. 
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app

