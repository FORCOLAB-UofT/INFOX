from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_mail import Mail

from config import config

bootstrap = Bootstrap()
db = MongoEngine()

def create_app(config_name):
    """ factory function for create app
    :param config_name
    :return: app object
    """
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config[config_name])
    
    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint # main blue print
    # from .api import api as api_blueprint # api blue print
    app.register_blueprint(main_blueprint)
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app

from app.main import views
