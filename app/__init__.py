from flask import Flask
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from config import Config

app = Flask(__name__)
app.config.from_object('config.DevConfig')

api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import views
from app.resources import UserListAPI, UserAPI

API_VERSION = Config.API_VERSION
#register resources here:
api.add_resource(UserListAPI, '/taskx/api/v{version}/users'.format(version=API_VERSION),
                 endpoint='users')
api.add_resource(UserAPI, '/taskx/api/v{version}/users/<int:id>'.format(version=API_VERSION),
                 endpoint='user')





