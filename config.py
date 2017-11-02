import os
here = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '#+^aOjdlPHFD09)&*2P3JR-0CFE)&H12EAa;O0' # a random string.
    MONGODB_SETTINGS = {
        'db': 'test',
        'host': '127.0.0.1',
        'port': 27017
    }
    SHOW_NUMBER_FOR_PAGE = 6
    LOCAL_DATA_PATH = '/Users/fancycoder/infox_data/result'
    ACCESS_TOKEN = '' #your_access_token
    
class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'default': DevelopmentConfig
}

