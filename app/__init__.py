from flask import Flask
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.DevConfig')

api = Api(app)
db = SQLAlchemy(app)

from app import views



