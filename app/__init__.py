from flask import Flask
from flask import request, url_for
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_github import GitHub
from flask_cors import CORS
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .api.FollowedRepositories import FollowedRepositories
from .api.ImportRepositories import ImportRepositories
from .api.SearchGithub import SearchGithub
from .api.FollowRepository import FollowRepository
from .api.Auth import Auth
from .api.ForkList import ForkList
from .db import initialize_db
from .loginmanager import login_manager
from .mail import mail
from datetime import timedelta

# from flask_celery import Celery

from .celery import celery

from config import config

bootstrap = Bootstrap()
github = GitHub()
# celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def create_app(config_name):
    """factory function for create app
    :param config_name
    :return: app object
    """
    app = Flask(__name__, static_folder="static")
    CORS(app)
    api = Api(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    def url_for_other_page(page):
        args = request.view_args.copy()
        args.update(request.args.to_dict())
        args["page"] = page
        return url_for(request.endpoint, **args)

    def word_length_limit_filter(s):
        return [x for x in s if len(x) <= 20]

    app.jinja_env.globals["url_for_other_page"] = url_for_other_page
    app.jinja_env.filters["word_length_limit"] = word_length_limit_filter

    # TODO: Get app secret key from environment
    # set up config
    app.config.from_object(config[config_name])
    app.secret_key = "super secret key"
    app.config["JWT_SECRET_KEY"] = "not-so-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=43800)
    app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
    app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}

    # setup github-flask
    initialize_db(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    github.init_app(app)
    login_manager.init_app(app)
    celery.conf.update(app.config)

    api.add_resource(
        FollowedRepositories,
        "/flask/followed",
        resource_class_kwargs={"jwt": jwt},
    )
    api.add_resource(
        ImportRepositories, 
        "/flask/import",
        resource_class_kwargs={"jwt": jwt},
    )
    api.add_resource(SearchGithub, "/flask/search")
    api.add_resource(
        Auth,
        "/flask/auth",
        resource_class_kwargs={"bcrypt": bcrypt, "jwt": jwt},
    )
    api.add_resource(
        FollowRepository,
        "/flask/follow",
        resource_class_kwargs={"jwt": jwt},
    )

    api.add_resource(
        ForkList,
        "/flask/forklist",
        resource_class_kwargs={"jwt": jwt},
    )

    # TODO: get correct host, broker and backend depending on environment
    redis_host = "redis://localhost:6379/0"
    celery.conf.broker_url = redis_host
    celery.conf.result_backend = redis_host
    # celery.init_app(app)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    if app.config.get("SSL_DISABLE", None):
        from flask_sslify import flask_SSLify

        sslify = SSLify(app)

    from .main import main as main_blueprint  # main blue print
    from .auth import auth as auth_blueprint  # auth blue print

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app


from app import models
from app.main import views
