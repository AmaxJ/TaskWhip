from api import db
from api.models.users import User
from flask import url_for, make_response
import json
from flask_restful import Resource, reqparse, fields, marshal


user_field = {
    'id' : fields.Integer,
    'username' : fields.String,
    'email' : fields.String,
    'rank' : fields.String,
    'tasks' : fields.List(fields.String),
    'uri' : fields.Url('user')
}

class UserListAPI(Resource):

    def __init__(self):
        self.parser =  reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('username', type=str, required=True,
                                location='json', help="Username required")
        self.parser.add_argument('email', type=str, required=True,
                                 location='json',help="Email required")
        self.parser.add_argument('password', type=str, required=True,
                                  location='json', help="Password required")
        self.parser.add_argument('company_id', type=int, location='json',
                                  help='Company ID required')
        super(UserListAPI, self).__init__()

    def get(self):
        users = User.query.all()
        try:
            return {"users" : [marshal(user, user_field) for user in users] }
        except Exception as e:
            print e
            return {"error" : "Failed to retrieve users."}, 404

    def post(self):
        try:
            args = self.parser.parse_args()
            user = User(username=args["username"],
                           email=args["email"])
            user.hash_password(args["password"])
            db.session.add(user)
            db.session.commit()
            return {"user": marshal(user, user_field) }, 200
        except Exception as e:
            print e
            return {"error":"Error creating new user"}, 404



class UserAPI(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('username', type=str, location='json')
        self.parser.add_argument('email', type=str, location='json')
        self.parser.add_argument('password', type=str, location='json')
        super(UserAPI, self).__init__()

    def get(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            return {"user":marshal(user, user_field) }, 200
        except Exception as e:
            print e
            return {"error" : "User not found"}, 404

    def put(self, id):
        user = User.query.filter_by(id=id).first()
        if user is not None:
            try:
                args = self.parser.parse_args()
                for key, value in args.items():
                    if args[key] is not None:
                        setattr(user, key, value)
                db.session.commit()
                return {"user":marshal(user, user_field)}, 200
            except Exception as e:
                print e
                return { "error" : "Edit failed" }
        return {"error": "User not found"}, 404

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if user is not None:
            try:
                db.session.delete(user)
                db.session.commit()
                return { 'deleted':True }
            except Exception as e:
                print e
                return { "error" : "Delete failed"}



