from curses.ascii import isdigit
import json
import requests
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import Project, User, ProjectCluster, Permission, login_manager, ProjectFork, ChangedFile
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from ..analyse.analyser import get_active_forks
from ..analyse.compare_changes_crawler import fetch_commit_list, fetch_diff_code
import re
from rake_nltk import Rake
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from random import shuffle
from ..celery import celery
import spacy
from datetime import datetime
from ..analyse import project_updater 

programming_languages = ['html', 'js', 'json', 'py', 'php', 'css','md', 'babel', 'yml']
common_programming_words = ['if', 'else','for', 'return', 'and', 'or', 'merge', 'main', 'readme']
stop_words = programming_languages + common_programming_words
punctuations = ['\n', '{', '}', '.', '/', "(", ")", ":", "=", ">", "<", "=>", "==", "===", "<=", ">=", ";", "|", '||', '&&', '[', ']', "-", "$"]
rake = Rake(stopwords=stop_words, punctuations=punctuations)

def db_delete_project(project_name):
    Project.objects(project_name=project_name).delete()
    ProjectFork.objects(project_name=project_name).delete()
    ChangedFile.objects(project_name=project_name).delete()


def db_find_project(project_name):
    return Project.objects(project_name=project_name).first()
class ForkClustering(Resource):
    def __init__(self, jwt):
        self.jwt = jwt
    
    @celery.task
    def clusterRepo(repo, cluster_number, stop_words_with_user_input, update_data, github_access_token):
        cluster = ProjectCluster.objects(project_name=repo).first()
        print(f'update_data: {update_data}')
        if cluster and not(update_data):
            print('reached inside here--------------------')
            if cluster_number == 21:
                return {"nodes": cluster.nodes, "links": cluster.links}
            else:
                #top_common_words = dict(sorted(cluster.common_words.items(), key= lambda x: len(x[1]), reverse=True)[:cluster_number])
                #top_common_words = dict(sorted(cluster.top_common_words.items(), key= lambda x: len(x[1]), reverse=True)[:cluster_number])
                counter = 0
                top_common_words = []

                for i in range(len(sorted(cluster.top_common_words.items(), key= lambda x: len(x[1]), reverse=True))):
                    if counter == cluster_number:
                        break
                    print("item:", list(cluster.top_common_words.items())[i][0])
                    if list(cluster.top_common_words.items())[i][0] not in stop_words_with_user_input:
                        top_common_words.append(list(cluster.top_common_words.items())[i])
                        counter += 1 

                top_common_words = dict(top_common_words)

                nodes = [{
                    "id": repo,
                    "height": 2,
                    "size": 32,
                    "color": "rgb(244, 117, 96)"
                }]

                links = []
                wordcloud_text = ""

                for key, value in top_common_words.items():
                    wordcloud_text += ((str(key) + " ") * len(value))
                    
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

                #split = wordcloud_text.split()
                #shuffle(split)
                #wordcloud_text =  ' '.join(split)
                #wordcloud_display = WordCloud(background_color="white").generate(wordcloud_text)
                #print(wordcloud_display)

                #wordcloud_display.to_file('A.png')

                return {"nodes": nodes, "links": links, "wordcloud": list(top_common_words.items())}


        request_url = "https://api.github.com/repos/%s" % (
            repo,
        )

        res = requests.get(
            url=request_url,
            headers={
                "Accept": "application/json",
                "Authorization": "token {}".format(github_access_token),
            },
        )

        repository = res.json()

        active_forks = get_active_forks(repo, github_access_token)
        # project_updater.start_update(repo, None, forks_info=active_forks)
        key_words = {}
        common_words = {}
        project_forks = ProjectFork.objects(project_name=repo)
        key_words = {}
        
        for fork in project_forks:
            forker = fork.fork_name.split('/')[0]
            key_words[forker] = list(fork.key_words)
        print("DEBUG: {0}".format(project_forks))
        print("DEBUG: {0}".format(key_words))

        # for fork in active_forks:
        #     print("iteration")
        #     fork_name = fork["full_name"][: -(len(fork["name"]) + 1)]
        #     print(fork_name)
        #     commit_msgs = fetch_commit_list(repo, fork_name, fork["default_branch"], repository["default_branch"])
        #     code_changes = fetch_diff_code(repo, fork_name, fork["default_branch"], repository["default_branch"])

            
        #     sentences = []
        #     for msg in commit_msgs:
        #         sentences.append(msg['title'])

        #     for fork_info in code_changes:
        #         if fork_info['file_full_name']:
        #             sentences.append(fork_info['file_full_name'])
                
        #         if fork_info['added_code']:
        #             sentences.append(fork_info['added_code'])
            
        #     if sentences:
        #         rake.extract_keywords_from_sentences(sentences)
        #         key_words[fork_name] = rake.get_ranked_phrases()[:10]
            # print("PASSED fork info codes changes")
        # flipping dictionary
        for key, value in key_words.items():
            for word in value:
                if not word.isnumeric():
                    #check keyword_list to see the synonym
                    if word not in common_words:
                        common_words[word] = [key]
                    else:
                        common_words[word].append(key)

        cleaned_common_words = {}
        # cleaning the dictionary by removing "." in key names
        for word in common_words.keys(): 
            new_word = word.replace("."," ")
            cleaned_common_words[new_word] = common_words[word]

        print("passed clean common words")
        print(cleaned_common_words)

        nlp = spacy.load('en_core_web_md')
        # group by synonyms
        feature_list = {}
        for word, forks in cleaned_common_words.items():
            already_added = False
            # check if a synonym of current 'word' already in feature_list key
            for w in feature_list.keys():
                token1 = nlp(w)
                token2 = nlp(word)
                if token1.similarity(token2) > 0.7:
                    already_added = True
                    for fork in forks:
                        if fork not in feature_list[w]:
                            feature_list[w].append(fork)
            if not already_added:
                feature_list[word] = forks

            print("feature list construction")

        print("======= FEATURE LIST ========")
        print(feature_list)
        print("======= FEATURE LIST ========")
                        
        print("========== COMMON WORDS =========")
        print(f'common words: {common_words}')
        print("========== COMMON WORDS =========")

        top_common_words = dict(sorted(feature_list.items(), key= lambda x: len(x[1]), reverse=True)[:20])

        # send email

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

        ProjectCluster(project_name=repo, nodes=nodes, links=links, key_words=key_words, top_common_words=top_common_words, timestamp=datetime.utcnow()).save()

        return {
            "nodes": nodes,
            "links": links,
            "wordcloud": list(top_common_words.items())
        }

    def output_display(self,repo,cluster,cluster_number,stop_words_with_user_input):
        print("readched inside===========================================")
        if cluster_number == 21:
            return {"nodes": cluster.nodes, "links": cluster.links}
        else:
            #top_common_words = dict(sorted(cluster.common_words.items(), key= lambda x: len(x[1]), reverse=True)[:cluster_number])
            #top_common_words = dict(sorted(cluster.top_common_words.items(), key= lambda x: len(x[1]), reverse=True)[:cluster_number])
            counter = 0
            top_common_words = []

            for i in range(len(sorted(cluster.top_common_words.items(), key= lambda x: len(x[1]), reverse=True))):
                if counter == cluster_number:
                    break
                print("item:", list(cluster.top_common_words.items())[i][0])
                if list(cluster.top_common_words.items())[i][0] not in stop_words_with_user_input:
                    top_common_words.append(list(cluster.top_common_words.items())[i])
                    counter += 1 

            top_common_words = dict(top_common_words)

            nodes = [{
                "id": repo,
                "height": 2,
                "size": 32,
                "color": "rgb(244, 117, 96)"
            }]

            links = []
            wordcloud_text = ""

            for key, value in top_common_words.items():
                wordcloud_text += ((str(key) + " ") * len(value))
                
                nodes.append({
                    "id": key,
                    "height": 1,
                    "size": 60,
                    "color": "rgb(97, 205, 187)"
                })

                links.append({
                    "source": repo,
                    "target": key,
                    "distance": 400
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
                        "distance": 200
                    })

            #split = wordcloud_text.split()
            #shuffle(split)
            #wordcloud_text =  ' '.join(split)
            #wordcloud_display = WordCloud(background_color="white").generate(wordcloud_text)
            #print(wordcloud_display)

            #wordcloud_display.to_file('A.png')

            columns = [{ 'field': 'Keywords' , 'flex': 1}, { 'field': 'Repositories', 'flex':1 }]
            rows = []
            for i,keyword in enumerate(top_common_words.keys()):
                temp_row = {}
                temp_row["id"] = i
                temp_row["Keywords"] = keyword
                temp_row["Repositories"] = " , ".join(top_common_words[keyword])
                rows.append(temp_row)
            
            # print(html_table,flush=True)
            return {"nodes": nodes, "links": links, "wordcloud": list(top_common_words.items()), "table_columns": columns, "table_rows": rows,"repo":repo}

    @jwt_required()
    def get(self):
        req_data = request.args
        repo = req_data.get("repo")
        cluster_number = int(req_data.get("clusterNumber"))
        update_data = req_data.get("updateData") == "true"

        

        split_req_data = req_data.get("userInputWords").split(",")
        
        stop_words_with_user_input = stop_words + split_req_data + ["a", "the", "pull request"]
        
        

        print("req data:", req_data.get("userInputWords"))
        
        print(stop_words_with_user_input)
        print(stop_words)

        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()

        cluster = ProjectCluster.objects(project_name=repo).first()
        print(f'not(update_data): {not(update_data)}',flush=True)
        if cluster and not(update_data):
            return self.output_display(repo,cluster,cluster_number,stop_words_with_user_input)
        else:
            self.clusterRepo.delay(repo, cluster_number, stop_words_with_user_input, update_data, _user.github_access_token)
            if cluster:
                return self.output_display(repo,cluster,cluster_number,stop_words_with_user_input)
            # return self.clusterRepo(repo, cluster_number, stop_words_with_user_input, update_data, _user.github_access_token)
        return None

    