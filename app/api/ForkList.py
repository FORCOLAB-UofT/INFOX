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

programming_languages = ["html", "js", "json", "py", "php", "css", "md", "babel", "yml", "java", "python", "javascript"]
common_programming_words = [
    "if",
    "else",
    "for",
    "return",
    "and",
    "or",
    "merge",
    "in",
    "to",
    "init",
    "is",
    "not",
    "a",
    "main",
    "src",
    "com",
    "xml",
    "txt",
]
stop_words = programming_languages + common_programming_words
punctuations = [
    "\n",
    "{",
    "}",
    ".",
    "/",
    "(",
    ")",
    ":",
    "=",
    ">",
    "<",
    "=>",
    "==",
    "===",
    "<=",
    ">=",
    ";",
    "|",
    "||",
    "&&",
    "[",
    "]",
    "-",
    "$",
    "+",
    "-",
    ",",
    "'",
    "`",
    "()",
    "())",
    "__",
    "_",

]
rake = Rake(stopwords=stop_words, punctuations=punctuations)


class ForkList(Resource):
    def __init__(self, jwt):
        self.jwt = jwt

    # @jwt_required()
    # def get(self):

    #     current_user = get_jwt_identity()
    #     _user = User.objects(username=current_user).first()

    #     req_data = request.args
    #     repoName = req_data.get("repo")
    #     repo = repoName

    #     forks_info = ProjectFork.objects(project_name=repoName)
    #     # parentRepo = Project.objects(project_name=repoName)

    #     request_url = "http://forks-insight.com/flask/follow"
    #     if not forks_info:
    #         return {"forks": []}
    #         response = requests.post(request_url, json={"repo":repo}, headers={"Authorization": request.headers.get("Authorization")})
            

    #     key_words = {}
    #     common_words = {}
    #     top_common_words = []

    #     # active_forks = get_active_forks(repoName, _user.github_access_token)
    #     active_forks = get_active_forks(repoName, _user.github_access_token)
    #     alreadyAnalzyed = False

    #     for fork in forks_info:
    #         if len(fork["key_words"]) > 0:
    #             alreadyAnalzyed = True
    #             break
    #     if not alreadyAnalzyed:
    #         for fork in active_forks:
    #             fork_name = fork["full_name"][: -(len(fork["name"]) + 1)]
    #             commit_msgs = fetch_commit_list(repoName, fork_name)
    #             code_changes = fetch_diff_code(repoName, fork_name)

    #             sentences = []
    #             for msg in commit_msgs:
    #                 sentences.append(msg["title"])

    #             for fork_info in code_changes:
    #                 if fork_info["file_full_name"]:
    #                     sentences.append(fork_info["file_full_name"])

    #                 # if fork_info["added_code"]:
    #                 #     sentences.append(fork_info["added_code"])

    #             if sentences:
    #                 rake.extract_keywords_from_sentences(sentences)
    #                 key_words[fork_name] = rake.get_ranked_phrases()
    #                 print("key words found for ", fork_name, ":", key_words[fork_name])
    #                 ProjectFork.objects(fork_name=fork["full_name"]).update(
    #                     key_words=key_words[fork_name]
    #                 )
    #             else:
    #                 print("No keywords found for", fork_name)
    #                 ProjectFork.objects(fork_name=fork["full_name"]).update(
    #                     key_words=[]
    #                 )
    #             # for key, value in key_words.items():
    #             #     for word in value:
    #             #         if not word.isnumeric():
    #             #             if word not in common_words:
    #             #                 common_words[word] = [key]
    #             #             else:
    #             #                 common_words[word].append(key)
    #             # top_common_words = dict(
    #             #     sorted(common_words.items(), key=lambda x: len(x[1]), reverse=True)[:20]
    #             # )
    #             # Project.objects(project_name=repoName).update(common_fork_keywords=top_common_words)

    #         # print("Common words found by rake", top_common_words)

    #     # forks_info = ProjectFork.objects(project_name=repoName)
    #     # db_keyword_dict = {}
    #     # top_common_words = {}
    #     # for fork in forks_info:
    #     #     db_keyword_dict[fork["fork_name"]] = fork["key_words"]

    #     #     for key, value in db_keyword_dict.items():
    #     #         for word in value:
    #     #             if word not in common_words:
    #     #                 common_words[word] = [key]
    #     #             else:
    #     #                 common_words[word].append(key)

    #     return_list = []
    #     for fork in forks_info:
    #         return_list.append(
    #             {
    #                 "fork_name": fork["fork_name"],
    #                 "project_name": fork["project_name"],
    #                 "num_changed_files": fork["total_changed_file_number"],
    #                 "num_changed_lines": fork["total_changed_line_number"],
    #                 "changed_files": fork["file_list"],
    #                 "key_words": fork["key_words"],
    #                 "tags": fork["tags"],
    #                 "total_commit_number": fork["total_commit_number"],
    #                 "last_committed_time": str(fork["last_committed_time"]),
    #                 "created_time": str(fork["created_time"]),
    #             }
    #         )

    #     return {"forks": return_list}

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

        repoName = request.args.get("repo")
        repo = repoName

        return ProjectFork.objects(project_name=repo).count()