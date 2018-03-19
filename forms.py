# -*- coding: utf-8 -*-
# @Time    : 2018/2/4 14:46
# @Author  : liwugang
# @Email   : liwg@olei.me
# @File    : forms.py
# @Software: PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired,EqualTo,ValidationError
from models import User
from flask import session

"""
登录表单：
1.账号
2.密码
3.登录按钮
"""


class LoginForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("账号不能为空！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码"

        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_pwd(self,field):
        pwd = field.data
        user = User.query.filter_by(name=self.name.data).first()
        if not user.check_pwd(pwd):
            raise ValidationError("密码不正确")



"""
注册表单：
1.账号
2.密码
3.确认密码
4.验证码
5.注册按钮
"""


class RegisterForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("账号不能为空")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码"

        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("确认密码不能为空"),
            EqualTo('pwd',message="两次输入密码不一致")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请再一次输入密码!!!!"

        }
    )
    code = StringField(
        label="验证码",
        validators=[
            DataRequired('验证码不能为空')
        ],
        description="验证码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入验证码"
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class": "btn btn-success"
        }
    )
    # 自定义字段验证规则：validate_字段名
    def validate_name(self,field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user > 0:
            raise ValidationError("账号已存在，不能重新注册")

    # 自定义验证码验证功能
    def validate_code(self,field):
        code = field.data
        # if not session.has_key("code"): python2写法
        if "code" not in session:
            raise ValidationError("没有验证码")
        # if session.has_key("code") and session["code"].lower() != code.lower():python2写法
        if "code" in session and session["code"].lower() != code.lower(): # 从views中获取session的"code"
            raise ValidationError("验证码错误")
"""
发布文章表单
1.标题
2.分类
3.logo
4.内容
5.发布文章的按钮
"""


class ArtForm(FlaskForm):
    title = StringField(
        label="标题",
        validators=[
            DataRequired("标题不能为空")
        ],
        description="标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入文章标题"

        }
    )
    cate = SelectField(
        label="分类",
        description="分类",
        validators=[
            DataRequired("分类不能为空")
        ],
        choices=[(1, "科技"), (2, "搞笑"), (3, "军事")],
        default=1,
        render_kw={
            "class": "form-control"
        }
    )
    logo = FileField(
        label="封面",
        description="封面",
        validators=[
            DataRequired("封面不能为空")
        ],
        render_kw={
            "class": "form-control-file"
        }
    )
    content = TextAreaField(
        label="内容",
        description="内容",
        validators=[
            DataRequired("内容不能为空")
        ],
        render_kw={
            "style": "height:300px;",
            "id": "content"
        }
    )
    submit = SubmitField(
        "发布文章",
        render_kw={
            "class": "btn btn-primary"
        }
    )
