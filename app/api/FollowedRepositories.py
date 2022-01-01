from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from ..models import User, Project
import json


class FollowedRepositories(Resource):
    def __init__(self, jwt):
        self.jwt = jwt

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()

        project_list = Project.objects(project_name__in=_user.followed_projects)

        return_list = []
        for project in project_list:
            if project["last_updated_time"]:
                updated = project["last_updated_time"].strftime("%m/%d/%Y")
            else:
                updated = "Never"

            return_list.append(
                {
                    "language": project["language"],
                    "description": project["description"],
                    "timesForked": project["fork_number"],
                    "repo": project["project_name"],
                    "updated": updated,
                }
            )
        return return_list
