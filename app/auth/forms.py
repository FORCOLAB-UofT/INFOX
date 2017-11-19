# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)

from ..models import User

class LoginForm(FlaskForm): 
    email_or_username = StringField(
        'Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 80), Email()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(1, 30)])
    github_name = StringField('Github Name', validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(4, 20),
                                         EqualTo('password_confirm',
                                                 message='Entered passwords differ')])
    password_confirm = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField('Register')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password',
                                 validators=[DataRequired()])
    new_password = PasswordField('New password',
                                 validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField('Change')
