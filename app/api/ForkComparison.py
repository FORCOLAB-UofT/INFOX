from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json
from flask import request
import requests
from ..models import User, ProjectFork
from ..analyse.compare_changes_crawler import fetch_commit_list, fetch_diff_code
from ..analyse.analyser import get_active_forks
from rake_nltk import Rake

programming_languages = ['html', 'js', 'json', 'py', 'php', 'css','md', 'babel', 'yml']
common_programming_words = ['if', 'else','for', 'return', 'and', 'or']
stop_words = programming_languages + common_programming_words
punctuations = ['\n', '{', '}', '.', '/', "(", ")", ":", "=", ">", "<", "=>", "==", "===", "<=", ">=", ";", "|", '||', '&&', '[', ']', "-"]
rake = Rake(stopwords=stop_words, punctuations=punctuations)

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

        forks_info = ProjectFork.objects(project_name=repoName)

        key_words = {}
        common_words = {}

        # active_forks = get_active_forks(repoName, _user.github_access_token)
        active_forks = get_active_forks(repoName, _user.github_access_token)
        for fork in active_forks:
            fork_name = fork["full_name"][: -(len(fork["name"]) + 1)]
            commit_msgs, dummy = fetch_commit_list(repoName, fork_name)
            code_changes = fetch_diff_code(repoName, fork_name)

            sentences = []
            for msg in commit_msgs:
                sentences.append(msg['title'])

            for fork_info in code_changes:
                if fork_info['file_full_name']:
                    sentences.append(fork_info['file_full_name'])
                
                if fork_info['added_code']:
                    sentences.append(fork_info['added_code'])
            
            if sentences:
                rake.extract_keywords_from_sentences(sentences)
                key_words[fork_name] = rake.get_ranked_phrases()

        for key, value in key_words.items():
            for word in value:
                if word not in common_words:
                    common_words[word] = [key]
                else:
                    common_words[word].append(key)

        return {
            "keywords" : common_words,
            "forks" : forks_info
        }
