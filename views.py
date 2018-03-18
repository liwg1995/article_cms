# -*- coding: utf-8 -*-
# @Time    : 2018/2/4 14:46
# @Author  : liwugang
# @Email   : liwg@olei.me
# @File    : views.py
# @Software: PyCharm

# python2中设置默认字符集
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")


from flask import Flask, render_template, redirect, flash, session, Response, url_for, request
from forms import LoginForm, RegisterForm, ArtForm
from models import User, db
from werkzeug.security import generate_password_hash
import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"


# 登录装饰器，避免没有登录的情况下仍能访问/art/list或者/art/add/
def user_login_req(f):
    @wraps(f)
    def login_req(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return login_req


# 登录
@app.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        session["user"] = data["name"]
        flash("登录成功！", "ok")
        return redirect("/art/list/")
    return render_template("login.html", title="登录", form=form)


# 注册
@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        # 保存数据
        user = User(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            addtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(user)
        db.session.commit()
        # 定义一个会话的闪现
        flash("注册成功，请登录！", "ok")
        return redirect('/login/')
    else:
        flash("请输入正确信息", "err")
        # return redirect("/register/")
    return render_template("register.html", title="注册", form=form)


# 退出(302跳转到登录页面)
@app.route('/logout/', methods=["GET"])
@user_login_req
def logout():
    session.pop("user", None)
    return redirect("/login/")


# 发布文章
@app.route('/art/add/', methods=["GET", "POST"])
@user_login_req
def art_add():
    form = ArtForm()
    return render_template("art_add.html", title="发布文章", form=form)


# 编辑文章
@app.route('/art/edit/<int:id>/', methods=["GET", "POST"])
@user_login_req
def art_edit(id):
    return render_template("art_edit.html")


# 删除文章
@app.route('/art/del/<int:id>/', methods=["GET"])
@user_login_req
def art_del(id):
    return redirect("/art/list")


# 文章列表
@app.route('/art/list/', methods=["GET"])
@user_login_req
def art_list():
    return render_template("art_list.html", title="文章列表")


# 验证码
@app.route('/codes/', methods=["GET"])
def codes():
    from codes import Codes
    c = Codes()
    info = c.create_code()
    image = os.path.join(os.path.dirname(__file__), "static/code") + "/" + info["img_name"]
    with open(image, "rb") as f:
        image = f.read()
    session["code"] = info["code"]
    return Response(image, mimetype="jpeg")


if __name__ == "__main__":
    app.run(debug=True)
