from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json
from flask import request
import requests
from ..models import User, ProjectFork


class ForkList(Resource):
    def __init__(self, jwt):
        self.jwt = jwt

    @jwt_required()
    def get(self):

        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()

        req_data = request.args
        repoName = req_data.get("repo")

        forks_info = ProjectFork.objects(project_name=repoName)

        return_list = []
        for fork in forks_info:
            return_list.append(
                {
                    "fork_name": fork["fork_name"],
                    "project_name": fork["project_name"],
                    "num_changed_files": fork["total_changed_file_number"],
                    "num_changed_lines": fork["total_changed_line_number"],
                    "key_words": fork["key_words"],
                    "tags": fork["tags"],
                    "total_commit_number": fork["total_commit_number"]
                }
            )

        return {"forks": return_list}
