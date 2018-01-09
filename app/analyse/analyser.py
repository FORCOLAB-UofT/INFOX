import time

from flask import current_app
from flask_github import GitHub
import threading
from . import project_updater
from .. import email

from ..models import *

def start_analyse(app, project_name, analyse_github):
    print("-----start analysing for %s-----" % project_name)
    with app.app_context():
        print('try fetch repo info for %s' % project_name)
        repo_info = analyse_github.get('repos/%s' % project_name)
        print('finish fetch repo info for %s' % project_name)

        project_updater.project_init(project_name, repo_info) # First updata for quick view.

        print('try fetch fork list for %s' % project_name)
        repo_forks_list = analyse_github.request('GET', 'repos/%s/forks' % project_name, True)
        print('finish fetch fork list for %s' % project_name)

        project_updater.start_update(project_name, repo_info, repo_forks_list)

        # Send email to user
        email.send_mail_for_repo_finish(project_name)
    print("-----finish analysing for %s-----" % project_name)

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
        analyse_github.get('repos/%s' % repo)
    except:
        return False
    return True

def add_repos(username, repos):
    User.objects(username=username).update_one(push_all__repo_waiting_list=repos)
    app = current_app._get_current_object()
    threading.Thread(target=check_waiting_list, args=[app, username]).start()
    return True

