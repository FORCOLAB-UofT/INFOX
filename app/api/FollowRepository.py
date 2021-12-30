import requests
from datetime import datetime
from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from ..models import User, Project, Permission, login_manager
from ..analyse import project_updater
from ..analyse.analyser import check_waiting_list


def db_find_project(project_name):
    return Project.objects(project_name=project_name).first()


def db_followed_project(user, project_name):
    if project_name not in user.followed_projects:
        User.objects(username=user.username).update_one(
            push__followed_projects=project_name
        )
    # Update project followed time
    tmp_dict = user.followed_projects_time
    tmp_dict[project_name] = datetime.utcnow()
    User.objects(username=user.username).update_one(
        set__followed_projects_time=tmp_dict
    )


def add_repo(username, repo, repo_info):
    User.objects(username=username).update_one(push_all__repo_waiting_list=[repo])

    # First updata for quick view.

    project_updater.project_init(repo, repo_info)

    app = current_app._get_current_object()
    with app.app_context():
        check_waiting_list.delay(username)


class FollowRepository(Resource):
    def __init__(self, jwt):
        self.jwt = jwt

    @jwt_required()
    def post(self):
        req_data = request.get_json()
        repo = req_data.get("repo")

        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()

        request_url = "https://api.github.com/repos/%s" % repo

        res = requests.get(
            url=request_url,
            headers={
                "Accept": "application/json",
                "Authorization": "token {}".format(_user.github_access_token),
            },
        )

        if res.status_code != 200:
            raise AssertionError

        res = res.json()

        if db_find_project(repo) is not None:
            db_followed_project(_user, repo)
            msg = (
                'The repo (%s) is already in INFOX. Followed successfully! Please click <a href="/project/%s" class="alert-link">here</a> to view.'
                % (repo, repo)
            )
        else:
            add_repo(_user.username, repo, res)
            db_followed_project(_user, repo)
            msg = (
                "The repo (%s) starts loading into INFOX. We will send you an email when it is finished. Please wait."
                % repo
            )

        project_list = Project.objects(
            project_name__nin=_user.followed_projects,
            activate_fork_number__ne=-1,
            analyser_progress="100%",
        )

        return msg
