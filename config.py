import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    PORT = 3000
    HOST = '127.0.0.1'
    API_VERSION = 0


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + _basedir + 'task.db'


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + _basedir + 'test.db'
    LIVESERVER_PORT = 3000
    TESTING = True
