from flask import Flask

# create_app 함수를 작성한다.
def create_app():
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    from apps.crud import views as crud_views
    # blueprint 는 기본주소뒤에는 루트에 키워드 있다. 
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app

