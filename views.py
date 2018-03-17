# -*- coding: utf-8 -*-
# @Time    : 2018/2/4 14:46
# @Author  : liwugang
# @Email   : liwg@olei.me
# @File    : views.py
# @Software: PyCharm

from flask import Flask, render_template, redirect, flash, session, Response
from forms import LoginForm, RegisterForm, ArtForm
from models import User, db
from werkzeug.security import generate_password_hash
import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"


# 登录
@app.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
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
def logout():
    return redirect("/login/")


# 发布文章
@app.route('/art/add/', methods=["GET", "POST"])
def art_add():
    form = ArtForm()
    return render_template("art_add.html", title="发布文章", form=form)


# 编辑文章
@app.route('/art/edit/<int:id>/', methods=["GET", "POST"])
def art_edit(id):
    return render_template("art_edit.html")


# 删除文章
@app.route('/art/del/<int:id>/', methods=["GET"])
def art_del(id):
    return redirect("/art/list")


# 文章列表
@app.route('/art/list/', methods=["GET"])
def art_list():
    return render_template("art_list.html", title="文章列表")


# 验证码
@app.route('/codes/', methods=["GET"])
def codes():
    from codes import Codes
    c = Codes()
    info = c.create_code()
    image = os.path.join(os.path.dirname(__file__), "static/code") + "/" + info["img_name"]
    with open(image,"rb") as f:
        image = f.read()
    session["code"] = info["code"]
    return Response(image, mimetype="jpeg")


if __name__ == "__main__":
    app.run(debug=True)
