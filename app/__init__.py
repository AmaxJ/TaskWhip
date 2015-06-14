from flask import Flask
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config.DevConfig')

api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import views
from app.resources import UsersAPI


#register resources here:
api.add_resource(UsersAPI, '/taskx/api/v1.0/users', endpoint='users')





