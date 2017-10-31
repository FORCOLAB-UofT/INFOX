import os
here = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '#+^aOjdlPHFD09)&*2P3JR-0CFE)&H12EAa;O0'
    MONGODB_SETTINGS = {
        'db': 'test',
        'host': '127.0.0.1',
        'port': 27017
    }

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'default': DevelopmentConfig
}

