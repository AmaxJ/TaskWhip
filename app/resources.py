from app import db
from app.models import User 
from flask_restful import Resource, fields, marshal


class UsersAPI(Resource):
    def get(self):
        return {'test':'Hello world'}
    def post(self):
        pass
    def delete(self):
        pass



