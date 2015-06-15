from app import db
from app.models import User 
from flask_restful import Resource, fields, marshal, reqparse

user_field = {
    'id' : fields.Integer,
    'username' : fields.String,
    'email' : fields.String
}

class UsersAPI(Resource):
    def __init__(self):
        self.parser =  reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, location='json')
        self.parser.add_argument('email', type=str, required=True, location='json')
        self.parser.add_argument('password', type=str, required=True, location='json')
        super(UsersAPI, self).__init__()

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
        
    def delete(self):
        pass



