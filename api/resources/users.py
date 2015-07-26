from api import db
from api.models.users import User 
from flask import url_for, make_response
import json
from flask_restful import Resource, reqparse



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
        query = User.query.all()
        if len(query) > 0:
            users = []
            try:
                for user in query:
                    user_id = getattr(user, 'id')
                    uri = url_for("user", id=user_id)
                    users.append(user.return_dict( "id", "username", "email", 
                                                   "rank", uri=uri))
                response = make_response(json.dumps({"users" : users}))
                response.headers["content-type"] = "application/json"
                return response
            except Exception as e:
                print e
                return {"error" : "Could not retrieve users"}
        return {"error":"No users found"}

    def post(self):
        try:
            args = self.parser.parse_args()
            newUser = User(username=args["username"],
                           email=args["email"])
            newUser.hash_password(args["password"])
            db.session.add(newUser)
            db.session.commit()
            uri = url_for("user", id=newUser.id)
            #re-query so we can call the return_dict() method
            user = User.query.filter_by(username=args["username"]).first()
            user = user.return_dict("id", "username", "email", 
                                    "rank", uri=uri)
            response = make_response(json.dumps({"user":user}))
            response.headers["content-type"] = "application/json"
            return response    
        except Exception as e:
            print e
            return {"error":"Error creating new user"}

     

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
            uri = url_for("user", id=id)
            user = user.return_dict("id", "username", "email", 
                                    "rank", uri=uri)
            response = make_response(json.dumps({"user": user}))
            response.headers["content-type"] = "application/json"
            return response
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
                uri = url_for("user", id=id)
                user = user.return_dict("id", "username", "email", 
                                        "rank", uri=uri)
                response = make_response(json.dumps({"user": user}))
                response.headers["content-type"] = "application/json"
                return response
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



