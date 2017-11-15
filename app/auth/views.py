# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import auth
from .. import db
from ..models import User, Permission
from .forms import LoginForm, RegistrationForm, ChangePasswordForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email_or_username.data).first()
        if user is None:
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
                        permission=Permission.NORMAL_USER).save()
            flash('Register Successful!')
            return redirect(url_for('auth.login'))
        else:
            flash('Username already exist!')
    return render_template('auth/register.html', form=form)


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
