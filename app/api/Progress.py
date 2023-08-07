from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json
from flask import request
import requests
from ..models import User, ProjectFork, Project
from ..analyse.compare_changes_crawler import fetch_commit_list, fetch_diff_code
from ..analyse.analyser import get_active_forks
from ..analyse.analyser import get_commit_number_per_week
from ..analyse.analyser import get_commit_number_per_hour
from rake_nltk import Rake

def db_find_project(project_name):
    return Project.objects(project_name=project_name).first()


class Progress(Resource):
    def __init__(self, jwt):
        self.jwt = jwt

    @jwt_required()
    def post(self):

        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()

        req_data = request.get_json()
        repoName = req_data.get("repo")
        index = req_data.get("index")
        repo = repoName

        forks_info = ProjectFork.objects(project_name=repo)
        fork = forks_info[index]
        return_list = []

        return_list.append(
            {
                "fork_name": fork["fork_name"],
                "project_name": fork["project_name"],
                "num_changed_files": fork["total_changed_file_number"],
                "num_changed_lines": fork["total_changed_line_number"],
                "changed_files": fork["file_list"],
                "key_words": fork["key_words"],
                "tags": fork["tags"],
                "total_commit_number": fork["total_commit_number"],
                "last_committed_time": str(fork["last_committed_time"]),
                "created_time": str(fork["created_time"]),
                "weekly_commit_freq": get_commit_number_per_week(fork["fork_name"],  _user.github_access_token),
                "hourly_commit_freq": get_commit_number_per_hour(fork["fork_name"],  _user.github_access_token),
            }
        )
        
        return {"forks": return_list}

    @jwt_required()
    def get(self):


        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()

        req_data = request.args
        repoName = req_data.get("repo")
        repo = repoName

        forks_info = ProjectFork.objects(project_name=repo)
        
        return len(forks_info)

        
