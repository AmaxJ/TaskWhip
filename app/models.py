from app import db, bcrypt
from datetime import datetime 

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    tasks = db.relationship('Task', backref='user',
                             lazy='dynamic')

    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        pw_hash = self.password_hash
        return bcrypt.check_password_hash(pw_hash, password)

    def __repr__(self):
        return "{}:{} [{}]".format(self.id, self.username, self.email)


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "'{}' [user#: {}]".format(self.title, self.user_id)