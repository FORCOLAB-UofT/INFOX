# -*- coding: utf-8 -*-
from datetime import datetime
from flask import g, render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user

from . import auth

from .. import github
from ..models import User, Permission
from ..analyse.util import localfile_tool

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return github.authorize(scope="user:email")

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.start'))

@github.access_token_getter
def token_getter():
    if current_user.is_authenticated:
        # print("user token %s: %s" % (current_user.username, current_user.github_access_token))
        return current_user.github_access_token
    else:
        # print("token get from g! %s" % g.github_access_token)
        return g.get('github_access_token', None)

def get_user_repo_list(username):
    try:
        raw_data = github.request('GET', 'users' + '/' + username + '/' + 'repos', True)
        return [x["full_name"] for x in raw_data]
    except:
        pass
    return None

def get_upperstream_repo(repo):
    try:
        raw_data = github.request('GET', 'repos' + '/' + repo)
        if raw_data["fork"] == True:
            # print("R=",raw_data["source"]["full_name"])
            return raw_data["source"]["full_name"]
    except:
        pass
    return None

@auth.route('/callback', methods=['GET', 'POST'])
@github.authorized_handler
def github_login(access_token):
    g.github_access_token = access_token
    _github_user_info = github.get('user')
    _github_username = _github_user_info["login"]
    _github_user_email_list = github.get('user/emails')
    _github_user_email = None
    for email in _github_user_email_list:
        if email["primary"]:
            _github_user_email = email["email"]
    if _github_user_email is None:
        for email in _github_user_email_list:
            if 'noreply' not in email["email"]:
                _github_user_email = email["email"]
    
    _user = User.objects(username=_github_username).first()
    if _user is None:
        User(username=_github_username,
             email=_github_user_email,
             permission=Permission.GITHUB_USER).save()
    User.objects(username=_github_username).update(github_access_token=access_token)
    User.objects(username=_github_username).update(last_seen=datetime.utcnow())
    _user = User.objects(username=_github_username).first()
    login_user(_user, True)
    
    # print("login acc=%s" % g.github_access_token)
    
    return redirect(request.args.get('next') or url_for('main.index'))

