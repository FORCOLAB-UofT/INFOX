from curses.ascii import isdigit
import requests
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import Project, User, ProjectCluster, Permission, login_manager
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from ..analyse.analyser import get_active_forks
from ..analyse.compare_changes_crawler import fetch_commit_list, fetch_diff_code
import re
from rake_nltk import Rake

programming_languages = ['html', 'js', 'json', 'py', 'php', 'css','md', 'babel', 'yml']
common_programming_words = ['if', 'else','for', 'return', 'and', 'or']
stop_words = programming_languages + common_programming_words
punctuations = ['\n', '{', '}', '.', '/', "(", ")", ":", "=", ">", "<", "=>", "==", "===", "<=", ">=", ";", "|", '||', '&&', '[', ']', "-"]
rake = Rake(stopwords=stop_words, punctuations=punctuations)

class ForkClustering(Resource):
    def __init__(self, jwt):
        self.jwt = jwt

    @jwt_required()
    def get(self):
        req_data = request.args
        repo = req_data.get("repo")
        cluster_number = int(req_data.get("clusterNumber"))

        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()
        cluster = ProjectCluster.objects(project_name=repo).first()

        if cluster:
            if cluster_number == 20:
                return {"nodes": cluster.nodes, "links": cluster.links}
            else:
                top_common_words = dict(sorted(cluster.common_words.items(), key= lambda x: len(x[1]), reverse=True)[:cluster_number])

                nodes = [{
                    "id": repo,
                    "height": 2,
                    "size": 32,
                    "color": "rgb(244, 117, 96)"
                }]

                links = []

                for key, value in top_common_words.items():
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
                        frk_node = {
                            "id": frk,
                            "height": 0,
                            "size": 12,
                            "color": "rgb(232, 193, 160)"
                        }

                        if(frk_node) not in nodes:
                            nodes.append(frk_node)

                        links.append({
                            "source": key,
                            "target": frk,
                            "distance": 50
                        })

                return {"nodes": nodes, "links": links}


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
            code_changes = fetch_diff_code(repo, fork_name, repository['default_branch'])

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
                if not isdigit(word):
                    if word not in common_words:
                        common_words[word] = [key]
                    else:
                        common_words[word].append(key)

        top_common_words = dict(sorted(common_words.items(), key= lambda x: len(x[1]), reverse=True)[:20])

        nodes = [{
            "id": repo,
            "height": 2,
            "size": 32,
            "color": "rgb(244, 117, 96)"
        }]

        links = []

        for key, value in top_common_words.items():
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
                frk_node = {
                    "id": frk,
                    "height": 0,
                    "size": 12,
                    "color": "rgb(232, 193, 160)"
                }

                if(frk_node) not in nodes:
                    nodes.append(frk_node)

                links.append({
                    "source": key,
                    "target": frk,
                    "distance": 50
                })

        ProjectCluster(project_name=repo, nodes=nodes, links=links, key_words=key_words, common_words=common_words, top_common_words=top_common_words).save()

        return {
            "nodes": nodes,
            "links": links
        }
