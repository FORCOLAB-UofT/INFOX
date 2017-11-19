# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import auth
from .. import db
from ..models import User, Permission
from .forms import *

from ..analyse.api_crawler import get_user_starred_list
from ..main.views import db_add_project
from ..main.views import db_followed_project

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email_or_username.data)
        user_count = user.count()
        if user_count > 1:
            flash('You maybe use the same email for different accounts. Please use username to login.')            
            return redirect(url_for('auth.login'))
        elif user_count == 0:
            user = User.objects(username=form.email_or_username.data).first()
        if user is not None:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('Password Error!')
        else:
            flash('User not found!')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Login Successfully!')
    return redirect(url_for('main.start'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.objects(username=form.username.data).first() is None:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password_hash=generate_password_hash(
                            form.password.data),
                        permission=Permission.NORMAL_USER,
                        github_name=form.github_name.data).save()
            flash('Register Successful!')
            return redirect(url_for('auth.login'))
        else:
            flash('Username already exist!')
    return render_template('auth/register.html', form=form)


@auth.route('/load_from_github', methods=['GET', 'POST'])
def load_from_github():
    class ProjectSelection(FlaskForm):
        pass
    _starred_project = get_user_starred_list(current_user.username)
    for project in _starred_project:
        setattr(ProjectSelection, project, BooleanField(project))
    setattr(ProjectSelection, 'button_submit', SubmitField('Confirm'))
    form = ProjectSelection()
    if form.validate_on_submit():
        for field in form:
            if field.type == "BooleanField" and field.data:
                db_add_project(field.id)
        flash('Add successfully!')
        return redirect(url_for('main.index'))
    return render_template('auth/load_from_github.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    _user = User.objects(username=current_user.username).first()
    if _user is None:
        flash('User not found!')
        return redirect(url_for('main.index'))
    if current_user == _user and form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.old_password.data):
            User.objects(username=current_user.username).update_one(
                set__password_hash=generate_password_hash(form.new_password.data))
            flash('Password has changed!')
            return redirect(url_for('main.index'))
        else:
            flash('Original Password Error!')
            return redirect(url_for('auth.change_password'))
    return render_template('auth/change_password.html', form=form)
