import requests
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import User, Project, Permission, login_manager
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from ..analyse.analyser import get_active_forks
from ..analyse.compare_changes_crawler import fetch_commit_list
import re
from rake_nltk import Rake

rake = Rake()

class ForkClustering(Resource):
    def __init__(self, jwt):
        self.jwt = jwt

    @jwt_required()
    def get(self):
        req_data = request.args
        repo = req_data.get("repo")

        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()

        request_url = "https://api.github.com/repos/%s" % (
            repo,
        )

        res = requests.get(
            url=request_url,
            headers={
                "Accept": "application/json",
                "Authorization": "token {}".format(_user.github_access_token),
            },
        )

        repository = res.json()

        active_forks = get_active_forks(repo, _user.github_access_token)
        key_words = {}
        common_words = {}

        for fork in active_forks:
            fork_name = fork["full_name"][: -(len(fork["name"]) + 1)]
            commit_msgs = fetch_commit_list(repo, fork_name, repository['default_branch'])

            sentences = []
            for msg in commit_msgs:
                sentences.append(msg['title'])
            
            if sentences:
                rake.extract_keywords_from_sentences(sentences)
                key_words[fork_name] = rake.get_ranked_phrases()

        for key, value in key_words.items():
            for word in value:
                if word not in common_words:
                    common_words[word] = [fork]
                else:
                    common_words[word].append(fork)

        check = ""

        nodes = [{
            "id": repo,
            "height": 2,
            "size": 32,
            "color": "rgb(244, 117, 96)"
        }]

        links = []

        for key, value in common_words.items():
            nodes.append({
                "id": key,
                "height": 1,
                "size": 30,
                "color": "rgb(97, 205, 187)"
            })

            links.append({
                "source": repo,
                "target": key,
                "distance": 80
            })

            for frk in value:
                nodes.append({
                    "id": frk["name"],
                    "height": 0,
                    "size": 12,
                    "color": "rgb(232, 193, 160)"
                })

                links.append({
                    "source": key,
                    "target": frk["name"],
                    "distance": 50
                })

        fndsk = ""
