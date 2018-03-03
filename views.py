# -*- coding: utf-8 -*-
# @Time    : 2018/2/4 14:46
# @Author  : liwugang
# @Email   : liwg@olei.me
# @File    : views.py
# @Software: PyCharm

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


# 登录
@app.route('/login/', methods=["GET", "POST"])
def login():
    return render_template("login.html", title="登录")


# 注册
@app.route('/register/', methods=["GET", "POST"])
def register():
    return render_template("register.html", title="注册")


# 退出(302跳转到登录页面)
@app.route('/logout/', methods=["GET"])
def logout():
    return redirect("/login/")


# 发布文章
@app.route('/art/add/', methods=["GET", "POST"])
def art_add():
    return render_template("art_add.html", title="发布文章")


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


if __name__ == "__main__":
    app.run(debug=True)
