import os
import platform


class Config:
    # Database config.
    MONGODB_SETTINGS = {
        'db': 'test',
        'host': '127.0.0.1',
        'port': 27017
    }

    # LOCAL_DATA_PATH used for storing the raw data from crawling the github.
    if platform.system() == 'Darwin':
        LOCAL_DATA_PATH = '/Users/fancycoder/infox_data/result'
    elif platform.system() == 'Linux':
        LOCAL_DATA_PATH = '/home/luyao/infox_data/result'

    # Overview page config.
    SHOW_NUMBER_FOR_PAGE = 6 # Project number per page in index page.
    SHOW_NUMBER_FOR_FORKS = 15 # Forks number per page in project overview page.

    # User manage config.
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

    SECRET_KEY = '#+^aOjdlPHFD09)&*2P3JR-0C;O0'  # a random string.
    

class DevelopmentConfig(Config):
    DEBUG = True
    ALLOW_FORKS_UPDATE = True # Refresh will re-get fork list.
    RECRAWLER_MODE = False # Refresh will re-crawler the forks' info.

class ProductionConfig(Config):
    ALLOW_FORKS_UPDATE = True # Refresh will re-get fork list.
    RECRAWLER_MODE = False # Refresh will re-crawler the forks' info.

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
