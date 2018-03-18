# -*- coding: utf-8 -*-
# @Time    : 2018/2/4 14:46
# @Author  : liwugang
# @Email   : liwg@olei.me
# @File    : models.py
# @Software: PyCharm
from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/artcms_pro"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

"""
用户表：
0.编号
1.账号
2.密码
3.注册的时间
"""


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(20), nullable=False)
    pwd = db.Column(db.String(100), nullable=False)
    addtime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)

"""
文章表
1.编号
2.标题
3.分类
4.作者
5.封面
6.内容
7.发布时间
"""


class Art(db.Model):
    __tablename__ = "art"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    cate = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    addtime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.title


if __name__ == "__main__":
    db.create_all()
