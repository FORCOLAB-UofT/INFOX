from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json
from flask import request
import requests
from ..models import User
from ..analyse.compare_changes_crawler import fetch_commit_list
from ..analyse.analyser import get_active_forks
from rake_nltk import Rake

class ForkComparison(Resource):
    def __init__(self, jwt):
        self.jwt = jwt

    @jwt_required()
    def get(self):

        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()
        
        req_data = request.get_json()
        forkNames = req_data.get("forks")
        repoName = req_data.get("repo")

        # a dictionary where each key (fork name) contains all commit messages of that fork  
        forkCommits = dict()

        # a list of all commits for each fork to be analyzed by Rake
        forkSentences = []

        # active_forks = get_active_forks(repoName, _user.github_access_token)

        for fork in forkNames:
            forkCommits[fork] = fetch_commit_list(repoName, fork)
            forkSentences.append(fetch_commit_list(repoName, fork))

        # extract common keywords between all selected forks
        common_keywords = Rake.extract_keywords_from_sentences(forkSentences)

        return {
            "keywords" : common_keywords,
        }
