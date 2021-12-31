import requests
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from ..models import User, Permission, login_manager


class SearchGithub(Resource):
    @jwt_required()
    def post(self):
        # TODO: add ability to search by topic, size, # followers, etc..
        req_data = request.get_json()
        repo = req_data.get("repo")

        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()

        request_url = "https://api.github.com/search/repositories?q=%s" % repo

        res = requests.get(
            url=request_url,
            headers={
                "Accept": "application/json",
                "Authorization": "token {}".format(_user.github_access_token),
            },
        )

        if res.status_code != 200:
            raise AssertionError

        res_json = res.json()
        top_ten_results = res_json["items"][:10]

        return top_ten_results
