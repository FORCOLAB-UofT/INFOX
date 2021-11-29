from flask import Flask
from flask import request, url_for
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_github import GitHub
from flask_mail import Mail
from flask_cors import CORS
from flask_restful import Api
from .api.FollowedRepositories import FollowedRepositories

# from flask_celery import Celery

from celery import Celery

from config import config

bootstrap = Bootstrap()
db = MongoEngine()
mail = Mail()
github = GitHub()
login_manager = LoginManager()
# celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
celery = Celery()

login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message = None


def create_app(config_name):
    """factory function for create app
    :param config_name
    :return: app object
    """
    app = Flask(__name__, static_folder="static")
    CORS(app)
    api = Api(app)
    api.add_resource(FollowedRepositories, "/flask/followed")

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

    # setup github-flask
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    github.init_app(app)
    login_manager.init_app(app)
    celery.conf.update(app.config)

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
