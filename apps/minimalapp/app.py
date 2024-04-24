from email_validator import validate_email, EmailNotValidError
from flask import (
                    Flask,
                    current_app,
                    g,
                    redirect,
                    render_template,
                    request,
                    url_for,
                    flash,
                   )

import logging
import os
# from flask_debugtoolbar import DebugToolbarExtension

from flask_mail import Mail, Message
# 서버 프로그램 객체를 만든다.
#__name__: 실행 중인 모듈의 시스템 상의 이름
app = Flask(__name__)
# 기본주소로 요청이 왔을 때 무엇을 할지 정의하기

app.config["MAIL_SERVER"]= os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"]= os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"]= os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")


mail = Mail(app)


app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
app.logger.setLevel(logging.DEBUG)
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# toolbar = DebugToolbarExtension(app)


@app.route('/')
def index():
    return 'Hello, Flaskbook!'

# 메소드에 따른 처리를 원한다면 구별해서 정의 할수 있다.
# 엔드포인트명 지정하지 않으면 함수명이 엔포인트명이된다.
@app.route("/hello/<name>", 
           methods=['GET','POST'],
           endpoint='hello-endpoint')
def hello(name):

    return f'Hello, {name}!'
# http://127.0.0.1:5000/name/happy       index/name/happy
@app.route("/name/<name>") #<happy>
def show_name(name):#happy
    return render_template("index.html", name=name) #index , happy


with app.test_request_context():
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint",name="world"))
    #  /name/AK?page=1
    print(url_for("show_name",name="AK",page="1"))

# http://127.0.0.1:5000/contact(키워드 return 해줘라)
# 플라스크의 템플릿 문서는 앱 내 templates 폴더에 있다고 가정한다.
@app.route("/contact")
def contact():
    return render_template("contact.html")

# http://127.0.0.1:5000/contact/complete
# post 요청이 오면 필요한 데이터 관련 처리를 하고 나서
# contact_complete.html 템플릿을 주는 get 처리를 하면서 마무리 하다.
@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete(): # view
    if request.method == "POST":
        
        # form 속성을 사용해서 폼의 값을 취득합니다,
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True

        if not username:
            flash("사용자명은 필수입니다")
            is_valid = False
        
        if not email:
            flash("메일 주소는 필수 입니다")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해 주세요")
            is_valid = False
        
        if not description:
            flash("문의 내용은 필수입니다")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )



        # 이메일을 보낸다 (나중에 구현할 부분)
        # contact 앤드포인트로 리다이렉트한다.
        flash("문의해 주셔서 감사합니다.")
        return redirect(url_for("contact_complete")) #? 뒤에 붙으는게 쿼리 
    return render_template("contact_complete.html")
# get 데이터 달라고 (무조건 주라고하는것은 없다)
# => 요청 결과롤 주소에 쿼리가 추가 된다.
# post 데이터 가져가라고 하는거 (무조건 가져가라고 하는것 없다)
# =>post로그인 하면 요청 결과로 전달된 데이터가 눈에 보이지 않는다.


def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)




  