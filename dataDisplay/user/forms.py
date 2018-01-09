# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length

from .models import User
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class RegisterForm(Form):
    """Register form."""

    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=3, max=25)])
    role_name = StringField('角色名称',
                            validators=[DataRequired()])
    # email = StringField('Email',
    #                     validators=[DataRequired(), Email(), Length(min=6, max=40)])

    # department = StringField('Department',
    #                          validators=[DataRequired(), Length(min=3, max=40)])
    department1 = BooleanField('农社科')
    department2 = BooleanField('专利科')
    department3 = BooleanField('法规科')
    department4 = BooleanField('合作交流科')
    department5 = BooleanField('高新科')
    department6 = BooleanField('成果科')

    output = BooleanField('导出')
    input = BooleanField('导入')
    update = BooleanField('编辑')
    delete = BooleanField('删除')
    password = PasswordField('密码',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('确认密码',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])

    town1 = BooleanField('周庄')
    town2 = BooleanField('锦溪')
    town3 = BooleanField('淀山湖')
    town4 = BooleanField('千灯')
    town5 = BooleanField('巴城')
    town6 = BooleanField('陆家')
    town7 = BooleanField('周市')
    town8 = BooleanField('张浦')
    town9 = BooleanField('花桥')
    town10 = BooleanField('高新区')
    town11 = BooleanField('开发区')
    town_all = BooleanField('全部')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already registered')
            return False
        # user = User.query.filter_by(email=self.email.data).first()
        # if user:
        #     self.email.errors.append('Email already registered')
        #     return False
        return True
