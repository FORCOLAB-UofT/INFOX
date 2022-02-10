from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json
from flask import request
import requests
from ..models import User


class ImportRepositories(Resource):
    def __init__(self, jwt):
        self.jwt = jwt

    @jwt_required()
    def get(self):

        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()

        request_url = "https://api.github.com/users/%s/repos" % current_user

        res = requests.get(
            url=request_url,
            headers={
                "Accept": "application/json",
                "Authorization": "token {}".format(_user.github_access_token),
            },
        )

        if res.status_code != 200:
            raise AssertionError

        res = res.json()

        return_list = {"importRepositories": []}
        for repo in res:
            return_list["importRepositories"].append(
                {
                    "repo": repo["full_name"],
                    "description": repo["description"],
                    "language": repo["language"],
                    "timesForked": repo["forks_count"],
                }
            )

        return return_list
