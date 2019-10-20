# _*_ coding: utf-8 _*_

from flask_wtf import FlaskForm
from flask_wtf.file import  FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, RadioField,SelectField,IntegerField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin

class FoodForm(FlaskForm):
    name = StringField(
        label="菜品名称",
        validators=[
            DataRequired("菜品名称不能为空！")
        ],
        description="菜品名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入菜品名称！"
        }
    )
    cate_id = SelectField(
        label="所属菜系",
        validators=[
            DataRequired("请选择所属菜系！")
        ],
        coerce=int,
        description="所属菜系",
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )
