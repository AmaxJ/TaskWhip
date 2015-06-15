from app import db
from app.models import User 
from flask_restful import Resource, fields, marshal, reqparse

user_field = {
    'id' : fields.Integer,
    'username' : fields.String,
    'email' : fields.String
}

class UserListAPI(Resource):
    def __init__(self):
        self.parser =  reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, location='json')
        self.parser.add_argument('email', type=str, required=True, location='json')
        self.parser.add_argument('password', type=str, required=True, location='json')
        super(UserListAPI, self).__init__()

    def get(self):
        users = User.query.all()
        return { 'users' : [marshal(user, user_field) for user in users]}

    def post(self):
        args = self.parser.parse_args()
        newUser = User(username=args["username"],
                       email=args["email"])
        newUser.hash_password(args["password"])
        db.session.add(newUser)
        db.session.commit()
        return {'user': marshal(args, user_field) }
     

class UserAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='json')
        self.parser.add_argument('email', type=str, location='json')
        self.parser.add_argument('password', type=str, location='json')
        super(UserAPI, self).__init__()

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return { 'user': marshal(user, user_field) }

    def put(self, id):
        pass

    def delete(self, id):
        pass



