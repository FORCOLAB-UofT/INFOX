import os

class Config:
    SECRET_KEY = '#+^aOjdlPHFD09)&*2P3JR-0CFE)&H12EAa;O0' # a random string.
    MONGODB_SETTINGS = {
        'db': 'test',
        'host': '127.0.0.1',
        'port': 27017
    }
    SHOW_NUMBER_FOR_PAGE = 6
    # LOCAL_DATA_PATH = '/home/luyao/infox_data/result'
    # LANGUAGE_DATA_PATH = '/home/luyao/INFOX/app/analyse/data'
    LOCAL_DATA_PATH = '/Users/fancycoder/infox_data/result'
    LANGUAGE_DATA_PATH = '/Users/fancycoder/INFOX/app/analyse/data'
    ALLOW_UPDATE = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    RECRAWLER_MODE = True

class ProductionConfig(Config):
    RECRAWLER_MODE = True

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

