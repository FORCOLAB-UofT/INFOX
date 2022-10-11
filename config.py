import os


class Config:
    # TODO: get mongo host from environment
    # Database config.
    # MONGODB_SETTINGS = {
    #    "db": "infox",
    #    "host": "127.0.0.1",
    #    "port": 27017,
    #    "connect": False,
    #    # 'username': os.environ.get('INFOX_DATABASE_USERNAME'),
    #    # 'password': os.environ.get('INFOX_DATABASE_PASSWORD'),
    # }

    MONGODB_SETTINGS = {
        "db": "forks-insights",
        "host": "mongodb+srv://admin:f5U!g$hMXtZP4@forks-insights.wgrvb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true",  # Replace this with the host string mongodb+srv://....
    }

    # TODO: get this from environment
    # LOCAL_DATA_PATH used for storing the raw data from crawling the github.
    # LOCAL_DATA_PATH = os.environ.get("INFOX_LOCAL_DATA_PATH")
    LOCAL_DATA_PATH = (
        "~/DATA"
    )

    # Overview page config.
    SHOW_NUMBER_FOR_PAGE = 10  # Project number per page in index page.

    # TODO: set up to get from environment based on dev versus prod
    # Github Oauth Apps config.
    GITHUB_CLIENT_ID = "5255e9520f2c9ed5c860"  # insert client id
    GITHUB_CLIENT_SECRET = "bed341d2f7b9a14828efc8e18afba9e316eebd47"  # insert secret key
    # GITHUB_CLIENT_ID = "5255e9520f2c9ed5c860"
    # GITHUB_CLIENT_SECRET = "bed341d2f7b9a14828efc8e18afba9e316eebd47"

    # secret key is a random string.
    SECRET_KEY = os.environ.get("INFOX_SECRET_KEY")

    # E-mail config.
    MAIL_SERVER = "smtp.126.com"  # Change it to your mail server
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get("INFOX_MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("INFOX_MAIL_PASSWORD")
    MAIL_USE_SSL = True
    FLASK_MAIL_SENDER = "<infox_help@126.com>"  # Change it to your mail sender
    FLASK_MAIL_SUBJECT_PREFIX = "[Forks-Insight]"

    # The cralwer worker config.
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


class DevelopmentConfig(Config):
    DEBUG = True
    USE_LOCAL_FORKS_LIST = True
    USE_LOCAL_FORK_INFO = True
    FORCED_UPDATING = (
        True  # Refresh will re-crawler the forks' info even if it's up-to-date.
    )


class ProductionConfig(Config):
    USE_LOCAL_FORKS_LIST = False
    USE_LOCAL_FORK_INFO = False
    FORCED_UPDATING = False  # Refresh will not re-crawler the up-to-date forks' info.


class TestingConfig(Config):
    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,
    "testing": TestingConfig,
}
