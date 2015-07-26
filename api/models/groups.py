from api import db
from datetime import datetime
#provides return_dict method for each model
from mixins import DbMixin

#relationships:
members_tbl = db.Table('members_tbl',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
    )
admins_tbl = db.Table('admins_tbl',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
    )


class Group(db.Model, DbMixin):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    admins = db.relationship("User", secondary=admins_tbl,
                          backref='admin_of')
    members = db.relationship("User", secondary=members_tbl, backref="groups")
    description = db.Column(db.Text)
    createdOn = db.Column(db.DateTime, default=datetime.now)
    tasks = db.relationship('Task', backref='group', lazy='dynamic')
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return "{}: {}".format(self.company_id, self.name)


class Company(db.Model, DbMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    group_count = db.Column(db.Integer)
    website = db.Column(db.String(255))
    groups = db.relationship('Group', backref='company')
    employees = db.relationship('User', backref='company', lazy='dynamic')

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return "{}".format(self.name)




