# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)

from ..models import User

class LoginForm(FlaskForm):
    email_or_username = StringField('Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(1, 16)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(4, 20),
                                         EqualTo('password_confirm',
                                                 message='Entered passwords differ')])
    password_confirm = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField('Register')

    def validate_email(self, field):
        pass
        
    def validate_username(self, field):
        pass

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password',
                                 validators=[DataRequired()])
    new_password = PasswordField('New password',
                                 validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField('Change')
