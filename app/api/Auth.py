import requests
from flask_restful import Resource
from flask import (
    request,
    g,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    current_app,
    Response,
)
from datetime import datetime
from ..models import User, Permission, login_manager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json


@login_manager.user_loader
def load_user(username):
    # Flask-Login callback fucntion for load user
    return User.objects(username=username).first()


class Auth(Resource):
    def __init__(self, jwt, bcrypt):
        self.bcrypt = bcrypt
        self.jwt = jwt

    # @login_required
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()

        res = requests.get(
            url="https://api.github.com/user",
            headers={
                "Accept": "application/json",
                "Authorization": "token {}".format(_user.github_access_token),
            },
        )

        if res.status_code != 200:
            raise AssertionError

        return {"email": _user.email, "username": _user.username}

    def post(self):
        req_data = request.get_json()
        code = req_data.get("code")

        if code:
            # we got a code let's exchange it for an access token
            data = {
                "client_id": "2d8e058ac0d5cf153c9e",
                "client_secret": "fee47e019a3b7a9510692b07b22c80a69c326ca5",
                "code": code,
            }
            # exchange the 'code' for an access token
            res = requests.post(
                url="https://github.com/login/oauth/access_token",
                data=data,
                headers={"Accept": "application/json"},
            )

            if res.status_code != 200:
                raise AssertionError

            res_json = res.json()
            access_token = res_json["access_token"]

            # get the user details using the access token
            res = requests.get(
                url="https://api.github.com/user",
                headers={
                    "Accept": "application/json",
                    "Authorization": "token {}".format(access_token),
                },
            )
            if res.status_code != 200:
                raise AssertionError

            res_json = res.json()

            # names = res_json["name"].split()
            # first_name = names[0]
            # last_name = names[1]
            login = res_json["login"] or res_json["email"]

            g.github_access_token = access_token
            # _github_user_info = github.get("user")
            _github_username = res_json["login"]

            email_response = requests.get(
                url="https://api.github.com/user/emails",
                headers={
                    "Accept": "application/json",
                    "Authorization": "token {}".format(access_token),
                },
            )
            email_response_json = email_response.json()
            _github_user_email_list = email_response_json
            _github_user_email = None
            for email in _github_user_email_list:
                if email["primary"]:
                    _github_user_email = email["email"]
                if _github_user_email is None:
                    for email in _github_user_email_list:
                        if "noreply" not in email["email"]:
                            _github_user_email = email["email"]

            _user = User.objects(username=_github_username).first()
            if _user is None:
                User(
                    username=_github_username,
                    email=_github_user_email,
                    permission=Permission.GITHUB_USER,
                ).save()
            User.objects(username=_github_username).update(
                github_access_token=access_token
            )
            User.objects(username=_github_username).update(last_seen=datetime.utcnow())
            _user = User.objects(username=_github_username).first()

            request.authorization = {"username": login, "atk": access_token}

            # login_user(_user, True)
            accessToken = json.dumps(
                {
                    "access_token": create_access_token(identity=_user.username),
                    "username": _user.username,
                }
            )

            return Response(
                accessToken,
                mimetype="application/json",
                status=200,
            )
