from app import app
from flask_restful import Resource, fields, marshal


class Test(Resource):
    def get(self):
        return {'users': [marshal]}


