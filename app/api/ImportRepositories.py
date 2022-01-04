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
        # TODO: REPLACE FAKE DATA
        # TODO: add active forks, last updated, forks containing unmerged code

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
        # print("Repo import GET Request Response: ", res)
        
        return res
