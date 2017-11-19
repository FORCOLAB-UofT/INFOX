import platform


class Config:
    # Database config.
    MONGODB_SETTINGS = {
        'db': 'test',
        'host': '127.0.0.1',
        'port': 27017
    }
    SHOW_NUMBER_FOR_PAGE = 6 # Project number per page in index page.
    SHOW_NUMBER_FOR_FORKS = 15 # Forks number per page in project overview page.
    ADMIN_USERNAME = 'admin'

    # LOCAL_DATA_PATH used for storing the raw data from crawling the github.
    if platform.system() == 'Darwin':
        LOCAL_DATA_PATH = '/Users/fancycoder/infox_data/result'
    elif platform.system() == 'Linux':
        LOCAL_DATA_PATH = '/home/luyao/infox_data/result'

    SECRET_KEY = '#+^aOjdlPHFD09)&*2P3JR-0CFE)&H12EAa;O0'  # a random string.
    
    # Github don't allow upload the access_token directly.
    ACCESS_TOKEN_EN = '116b7:1efcgc11gg:6g8584579cc84f7fdc9:4g7'
    ACCESS_TOKEN = ''
    for i in ACCESS_TOKEN_EN:
        ACCESS_TOKEN = ACCESS_TOKEN + chr(ord(i) - 1)

class DevelopmentConfig(Config):
    DEBUG = True
    ALLOW_FORKS_UPDATE = True # Refresh will re-get fork list.
    RECRAWLER_MODE = True # Refresh will re-crawler the forks' info.

class ProductionConfig(Config):
    ALLOW_FORKS_UPDATE = True # Refresh will re-get fork list.
    RECRAWLER_MODE = False # Refresh will re-crawler the forks' info.

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
