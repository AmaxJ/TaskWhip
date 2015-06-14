import os

_basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = False
	TESTING = False
	PORT = 8080
	HOST = '0.0.0.0'

class DevConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI='sqlite:////' + _basedir + 'task.db'

