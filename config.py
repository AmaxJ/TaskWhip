import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    PORT = 8080
    HOST = '0.0.0.0'
    API_VERSION = 0.1


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + _basedir + 'task.db'


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + _basedir + 'test.db'
    LIVESERVER_PORT = 8080
    TESTING = True
