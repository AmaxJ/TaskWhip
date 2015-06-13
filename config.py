class Config(object):
	DEBUG = False
	TESTING = False
	PORT = 8080
	HOST = '0.0.0.0'

class DevConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI='sqlite:////tmp/task.db'



