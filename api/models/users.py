from api import db, bcrypt
from api.models.tasks import Task 

tasks_tbl = db.Table('tasks_tbl',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    rank = db.Column(db.String(10), default="user")
    tasks = db.relationship('Task', secondary=tasks_tbl,
        backref='user') #add lazy loading?
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        pw_hash = self.password_hash
        return bcrypt.check_password_hash(pw_hash, password)

    def __repr__(self):
        if self.company_id:
            return "{}:{} [{}]".format(self.company_id, self.username,
                                       self.email)
        return "{} [{}]".format(self.username, self.email)
