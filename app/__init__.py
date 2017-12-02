from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_github import GitHub
from flask_mail import Mail

from config import config

bootstrap = Bootstrap()
db = MongoEngine()
mail = Mail()
github = GitHub()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """ factory function for create app
    :param config_name
    :return: app object
    """
    app = Flask(__name__, static_folder='static')

    # set up config
    app.config.from_object(config[config_name])

    # setup github-flask
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    github.init_app(app)
    login_manager.init_app(app)

    if app.config.get('SSL_DISABLE', None):
        from flask_sslify import flask_SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint  # main blue print
    from .auth import auth as auth_blueprint  # auth blue print
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


from app import models
from app.main import views
