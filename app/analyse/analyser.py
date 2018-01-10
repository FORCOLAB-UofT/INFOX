import time
import os
import json

from flask import current_app
from flask_github import GitHub
import threading
from . import project_updater
from .util import localfile_tool
from .. import email
from ..models import *

def start_analyse(app, repo, analyse_github):
    print("-----start analysing for %s-----" % repo)
    with app.app_context():
        repo_info = analyse_github.get('repos/%s' % repo)
        print('finish fetch repo info for %s' % repo)

        forks_list_path = current_app.config['LOCAL_DATA_PATH'] + "/" + repo + '/forks_list.json'
        if current_app.config['USE_LOCAL_FORKS_LIST'] and os.path.exists(forks_list_path):
            with open(forks_list_path) as read_file:
                repo_forks_list = json.load(read_file)
        else:
            repo_forks_list = analyse_github.request('GET', 'repos/%s/forks' % repo, True)
            localfile_tool.write_to_file(forks_list_path, repo_forks_list)
        
        print('finish fetch fork list for %s' % repo)

        project_updater.start_update(repo, repo_info, repo_forks_list)

        # Send email to user
        email.send_mail_for_repo_finish(repo)
    print("-----finish analysing for %s-----" % repo)

def check_waiting_list(app, username):
    user = User.objects(username=username).first()
    if user.is_crawling == 1:
        return
    User.objects(username=username).update_one(set__is_crawling=1)

    analyse_github = GitHub(app)
    @analyse_github.access_token_getter
    def token_getter():
        return user.github_access_token
    
    while True:
        waiting_list = User.objects(username=username).first().repo_waiting_list
        if (waiting_list is None) or (len(waiting_list) == 0):
            break
        for repo in waiting_list:
            User.objects(username=username).update_one(pull__repo_waiting_list=repo)
            thread = threading.Thread(target=start_analyse, args=[app, repo, analyse_github])
            thread.setDaemon(True)
            thread.start()
            thread.join(60 * 60) # wait for 1 hour

    User.objects(username=username).update_one(set__is_crawling=0)

def check_repo(repo, access_token):
    app = current_app._get_current_object()
    analyse_github = GitHub(app)
    @analyse_github.access_token_getter
    def token_getter():
        return access_token
    try:
        result = analyse_github.get('repos/%s' % repo)
    except:
        return None
    return result

def add_repos(username, repos):
    User.objects(username=username).update_one(push_all__repo_waiting_list=repos)
    app = current_app._get_current_object()

    # First updata for quick view.
    access_token = User.objects(username=username).first().github_access_token
    for repo in repos:
        repo_info = check_repo(repo, access_token)
        if repo_info is not None:
            project_updater.project_init(repo, repo_info)

    threading.Thread(target=check_waiting_list, args=[app, username]).start()
    return True

