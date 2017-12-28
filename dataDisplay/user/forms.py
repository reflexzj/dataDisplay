# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class RegisterForm(Form):
    """Register form."""

    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=3, max=25)])
    # email = StringField('Email',
    #                     validators=[DataRequired(), Email(), Length(min=6, max=40)])

    # department = StringField('Department',
    #                          validators=[DataRequired(), Length(min=3, max=40)])
    department = SelectField('部门', choices=[
        ('department1', '农社科'),
        ('department2', '专利科'),
        ('department3', '法规科'),
        ('department4', '合作交流科'),
        ('department5', '高新科'),
        ('department6', '成果科')])
    password = PasswordField('密码',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('确认密码',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])

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
