import time
import os
import json
from datetime import datetime
import requests

from flask import current_app, render_template
from flask_github import GitHub
from . import project_updater
from .util import localfile_tool
from ..models import *
from ..celery import celery
from flask_mail import Message
from .. import mail
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter


def send_mail(to, subject, template, **kwargs):
    """use async to send email
    :param to
    :param subject
    :param template
    :param kwargs
    """
    msg = Message(
        current_app.config["FLASK_MAIL_SUBJECT_PREFIX"] + subject,
        sender=current_app.config["FLASK_MAIL_SENDER"],
        recipients=[to],
    )
    msg.html = render_template(template, **kwargs)
    mail.send(msg)


def send_mail_for_repo_finish(project_name):
    _user_list = User.objects(followed_projects=project_name)
    for user in _user_list:
        if user.email is not None:
            last_email = user.repo_email_time.get(project_name, None)
            new_dict = user.repo_email_time
            new_dict[project_name] = datetime.utcnow()
            User.objects(username=user.username).update_one(repo_email_time=new_dict)
            if last_email is None:
                # Only send email when first add.
                send_mail(
                    user.email,
                    "Repo Status Update",
                    "email.html",
                    project_name=project_name,
                    username=user.username,
                )

def get_active_forks(repo, access_token):
    active_forks = []
    result_length = 100
    page = 1
    # # while result_length == 100 and page < 2:
    # # request_url = "https://api.github.com/repos/%s/forks?per_page=100&sort=stargazers&page=%d" % (
    # request_url = "https://api.github.com/repos/%s/forks?per_page=75&sort=stargazers&page=1" % (
    #     repo,
    # )

    # res = requests.get(
    #     url=request_url,
    #     headers={
    #         "Accept": "application/json",
    #         "Authorization": "token {}".format(access_token),
    #     },
    # )

    # forks = res.json()
    # # print(forks,flush=True)
    # result_length = len(forks)

    # for fork in forks:

    #     if fork["pushed_at"] > fork["created_at"]:
    #         active_forks.append(fork)

    #     # page += 1

    # active_forks = active_forks[:25]

    url = "https://github.com/%s/forks?include=active&page=1&period=1y&sort_by=stargazer_counts" % (
        repo,
    )
    active_fork_name = []

    print(f"url:{url}")
    s = requests.Session()
    s.mount("https://github.com", HTTPAdapter(max_retries=5))

    try:
        forks_page = s.get(url, timeout=1000)
        print("=============================== check status")
        print(f"++++++++++++++++++++{forks_page.status_code}",flush=True)
        print("=============================== check status")
        if forks_page.status_code != requests.codes.ok:
            raise Exception("error on fetch forks page on %s!" % repo)
    except:
        # raise Exception("error on fetch forks page on %s!" % repo)
        return []
    active_forks_page = BeautifulSoup(forks_page.content, "html.parser")

    for active_fork in active_forks_page.find_all("a", {"class":"no-underline f4"}):
        active_fork_name.append(active_fork.get('href'))

    for name in active_fork_name:
        request_url = 'https://api.github.com/repos' + name
        res = requests.get(
            url=request_url,
            headers={
                "Accept": "application/json",
                "Authorization": "token {}".format(access_token),
            },
        ) 
        active_forks.append(res.json())

    # print(active_forks)

    return active_forks

def get_commit_number_per_week(repo, access_token):

    request_url = "https://api.github.com/repos/%s/stats/participation" % repo

    res = requests.get(
        url=request_url,
        headers={
            "Accept": "application/json",
            "Authorization": "token {}".format(access_token),
        },
    )
    commit_info = res.json()
    if ('all' in commit_info.keys()):
        return commit_info['all']
    else:
        return [0] * 54

def get_commit_number_per_hour(repo, access_token):

    request_url = "https://api.github.com/repos/%s/stats/commit_activity" % repo

    res = requests.get(
        url=request_url,
        headers={
            "Accept": "application/json",
            "Authorization": "token {}".format(access_token),
        },
    )
    commit_info = res.json()
    return commit_info

def get_commit_number_per_week(repo, access_token):
    
    request_url = "https://api.github.com/repos/%s/stats/participation" % repo

    res = requests.get(
        url=request_url,
        headers={
            "Accept": "application/json",
            "Authorization": "token {}".format(access_token),
        },
    )
    commit_info = res.json()
    print(commit_info)
    if ('all' in commit_info.keys()):
        return commit_info['all']
    else:
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def get_commit_number_per_hour(repo, access_token):
    
    request_url = "https://api.github.com/repos/%s/stats/commit_activity" % repo

    res = requests.get(
        url=request_url,
        headers={
            "Accept": "application/json",
            "Authorization": "token {}".format(access_token),
        },
    )
    commit_info = res.json()
    return commit_info

@celery.task
def start_analyse(repo, access_token):
    """Start analyse on repo using github_api_caller(contains personal access token)
    Args:
        app context, repo, github_api_caller
    Returns:
        None
    """
    app = current_app._get_current_object()
    # github_api_caller = GitHub(app)

    # @github_api_caller.access_token_getter
    # def token_getter():
    #    return access_token

    print("-----start analysing for %s-----" % repo)

    # repo_info = github_api_caller.get("repos/%s" % repo)
    request_url = "https://api.github.com/repos/%s" % repo

    res = requests.get(
        url=request_url,
        headers={
            "Accept": "application/json",
            "Authorization": "token {}".format(access_token),
        },
    )
    repo_info = res.json()
    print("finish fetch repo info for %s" % repo)

    # Save forks' list into local
    forks_list_path = (
        current_app.config["LOCAL_DATA_PATH"] + "/" + repo + "/forks_list.json"
    )

    active_forks = get_active_forks(repo, access_token)

    if current_app.config["USE_LOCAL_FORKS_LIST"] and os.path.exists(forks_list_path):
        with open(forks_list_path) as read_file:
            repo_forks_list = json.load(read_file)
            project_updater.start_update(repo, repo_info, repo_forks_list)
            return
    else:
        # repo_forks_list = github_api_caller.get("repos/%s/forks" % repo)
        # request_url = "https://api.github.com/repos/%s/forks" % repo
        # res = requests.get(
        #     url=request_url,
        #     headers={
        #         "Accept": "application/json",
        #         "Authorization": "token {}".format(access_token),
        #     },
        # )
        # repo_forks_list = res.json()
        localfile_tool.write_to_file(forks_list_path, active_forks)

    print("finish fetch fork list for %s" % repo)

    project_updater.start_update(repo, repo_info, active_forks)

    # TODO: Fix email sending functionality
    # temporarily commented out to get working on local - laith
    # send_mail_for_repo_finish(repo)

    print("-----finish analysing for %s-----" % repo)


@celery.task
def check_waiting_list(username):
    """Check username's waiting list to crawl more
    Args:
        app context, username
    Returns:
        None
    """
    user = User.objects(username=username).first()
    if user.is_crawling == 1:
        return
    User.objects(username=username).update_one(set__is_crawling=1)

    access_token = user.github_access_token
    app = current_app._get_current_object()

    while True:
        waiting_list = User.objects(username=username).first().repo_waiting_list
        if (waiting_list is None) or (len(waiting_list) == 0):
            break
        for repo in waiting_list:
            print("--- repo in waiting list %s ---" % repo)
            User.objects(username=username).update_one(pull__repo_waiting_list=repo)

            with app.app_context():
                start_analyse.delay(repo, access_token)

            if not current_app.config["USE_LOCAL_FORKS_LIST"]:
                wait_time = check_repo(repo, access_token)["forks"] * 1.5 / 30
                time.sleep(wait_time)

            # thread = threading.Thread(target=start_analyse, args=[app, repo, github_api_caller])
            # thread.setDaemon(True)
            # thread.start()
            # thread.join(10 * 60) # wait for 10 mins

    User.objects(username=username).update_one(set__is_crawling=0)


def add_repos(username, repos):
    """User (username) add some repos."""
    User.objects(username=username).update_one(push_all__repo_waiting_list=repos)

    # First updata for quick view.
    access_token = User.objects(username=username).first().github_access_token
    for repo in repos:
        repo_info = check_repo(repo, access_token)
        if repo_info is not None:
            project_updater.project_init(repo, repo_info)

    app = current_app._get_current_object()
    with app.app_context():
        check_waiting_list.delay(username)

    # threading.Thread(target=check_waiting_list, args=[username]).start()
    return True


def check_repo(repo, access_token):
    """Check repo existence.
    Args:
        repo(full name), access_token
    Returns:
        None for not found,
        json result for found.
    """
    app = current_app._get_current_object()
    github_api_caller = GitHub(app)

    @github_api_caller.access_token_getter
    def token_getter():
        return access_token

    try:
        result = github_api_caller.get("repos/%s" % repo)
    except:
        return None
    return result