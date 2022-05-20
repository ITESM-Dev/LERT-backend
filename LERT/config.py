import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    HOST = '0.0.0.0'
    PORT = 8000

class ProductionConfig(Config):
    DEBUG = False 

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True