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

#import resources
from api.resources.users import UserListAPI, UserAPI
from api.resources.tasks import TaskListAPI, TasksByGroupId, TasksByGroupName, TaskAPI
from api.resources.companies import CompanyList, CompanyAPI
from api.resources.groups import GroupList, GroupListByCompanyId, GroupAPI
from api.resources.test import Test

API_VERSION = Config.API_VERSION
#register resources
api.add_resource(UserListAPI,
                 '/taskx/api/v{version}/users'.format(version=API_VERSION),
                 endpoint='users', strict_slashes=False)
api.add_resource(UserAPI,
                 '/taskx/api/v{version}/users/<int:id>'.format(version=API_VERSION),
                 endpoint='user', strict_slashes=False)
api.add_resource(TaskListAPI,
                 '/taskx/api/v{version}/tasks'.format(version=API_VERSION),
                 endpoint='tasks', strict_slashes=False)
api.add_resource(TasksByGroupId,
                '/taskx/api/v{version}/<int:group_id>/tasks'.format(version=API_VERSION),
                endpoint='tasksByGroupId', strict_slashes=False)
api.add_resource(TasksByGroupName,
                '/taskx/api/v{version}/<string:group_name>/tasks'.format(version=API_VERSION),
                endpoint='tasksByGroupName', strict_slashes=False)
api.add_resource(TaskAPI,
                '/taskx/api/v{version}/<int:group_id>/tasks/<int:id>'.format(version=API_VERSION),
                endpoint='task', strict_slashes=False)
api.add_resource(CompanyList,
                '/taskx/api/v{version}/companies'.format(version=API_VERSION),
                endpoint='companies', strict_slashes=False)
api.add_resource(CompanyAPI,
                '/taskx/api/v{version}/companies/<int:id>'.format(version=API_VERSION),
                endpoint='company', strict_slashes=False)
api.add_resource(GroupList,
                 '/taskx/api/v{version}/groups'.format(version=API_VERSION),
                 endpoint='groups', strict_slashes=False)
api.add_resource(GroupListByCompanyId,
                 '/taskx/api/v{version}/<int:company_id>/groups'.format(version=API_VERSION),
                 endpoint='groupsByCompanyId', strict_slashes=False)
api.add_resource(GroupAPI,
                 '/taskx/api/v{version}/<int:company_id>/groups/<int:id>'.format(version=API_VERSION),
                 endpoint='group', strict_slashes=False)


@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add('Content-Type', 'application/json')
    return response



