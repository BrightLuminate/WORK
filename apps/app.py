from pathlib import Path # 경로 처리를 위한 기본 라이브러리
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import  CSRFProtect
# SQLAlchemy를 인스턴스화한다.
from apps.config import config

db = SQLAlchemy()   # 객체 생성 db로 다룰것이다.
csrf = CSRFProtect() 

# LoginManager 를 인스턴스화한다.
login_manager = LoginManager()
# login_view 속성에 미로그인 시 사용할수 없다.리다이렉트하는 엔드포인트를 지정한다.
login_manager.login_view = "auth.signup"
#login_message 속성에 로그인 후에 표시할 메시지를 지정한다.
#여기에서는 아무것도 표시하지 않도록 공백을 저장한다.
login_manager.login_message = ""

#import json  from_file 를 사용하는 방법

# def create_app(): config를 읽어 들이는 다른 방법 from_pyfile 를 사용하는 방법

# create_app 함수를 작성한다.
# config의 키를 전달한다.
def create_app(config_key):
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    #앱의 config 설정 from_file 사용하는 방법
    #app.config.from_file("config.json", load=json.load)

    # 앱의cofing 설정  from_pyfile 를 사용하는 방법
    # app.config.from_pyfile("config.py")

    # from_envvar 를 사용하는 방법
    #app.config.from_envvar("APPLICATION_SETTINGS")

  # config_key에 매치하는 환경의 config 클래스를 읽어 들인다.
    app.config.from_object(config[config_key])

# 앱의 config 설정을 한다.    만약에 config 읽어들이는 방법은 app.config.from_object(config[config_key]) 제외 한다.
    app.config.from_mapping(
      SECRET_KEY="2AZSMss3p5QPbcYBsJ", # 자체적으로 이름 정할수도 있다.
        SQLALCHEMY_DATABASE_URI=
            f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",  #경로 현파일에 경로를 가져온다. / parent 지금 파일 들어온 경로
        SQLALCHEMY_TRACK_MODIFICATIONS=False, # 경과 안나온못 False를 쓴다.
        # SQL을 콘솔 로그에 출력하는 설정 
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY="AuzyszU5sugKN7KZs6f",  # 아무거나 써도된다.
  )
    
    csrf.init_app(app)

    # SQLAlchemy 와 앱을 연계한다. 
    db.init_app(app)
    # Migrate와 앱을 연계한다. 
    Migrate(app, db)

    # login_manager 는 이미 사용자 로그인 상태를 사용 할 수 있게 애플리케이션과 연계이다.
    login_manager.init_app(app)

    from apps.crud import views as crud_views
    # blueprint 는 기본주소뒤에는 루트에 키워드 있다. 
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

  # 이제부터 작성하는 auth 패키지로부터 view를 inport 한다.
    from apps.auth import views as auth_views
    # register_blueprint를 사용해 views의 auth를  앱에 등록한다.
    app.register_blueprint(auth_views.auth, url_prefix="/auth")


    return app

