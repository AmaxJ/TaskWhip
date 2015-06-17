from api import db
from api.models import User 
from flask_restful import Resource, fields, marshal, reqparse

user_field = {
    'id' : fields.Integer,
    'username' : fields.String,
    'email' : fields.String,
    'uri' : fields.Url('user')
}

class UserListAPI(Resource):
    def __init__(self):
        self.parser =  reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, 
                                location='json', help="Username required")
        self.parser.add_argument('email', type=str, required=True,
                                 location='json',help="Email required")
        self.parser.add_argument('password', type=str, required=True, 
                                  location='json', help="Password required")
        super(UserListAPI, self).__init__()

    def get(self):
        users = User.query.all()
        return { 'users' : [marshal(user, user_field) for user in users] }

    def post(self):
        args = self.parser.parse_args()
        newUser = User(username=args["username"],
                       email=args["email"])
        newUser.hash_password(args["password"])
        db.session.add(newUser)
        db.session.commit()
        return { 'user': marshal(newUser, user_field) }
     

class UserAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='json')
        self.parser.add_argument('email', type=str, location='json')
        self.parser.add_argument('password', type=str, location='json')
        super(UserAPI, self).__init__()

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user is not None:
            return { 'user': marshal(user, user_field) }
        return {"error":"User not found"}, 404

    def put(self, id): 
        user = User.query.filter_by(id=id).first()
        if user is not None:
            args = self.parser.parse_args()
            for key, value in args.items():
                if args[key] is not None:
                    setattr(user, key, value)
            db.session.commit()
            return {"user": marshal(user,user_field) }
        return {"error": "User not found"}, 404

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return { 'deleted':True }



