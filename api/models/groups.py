from api import db
from datetime import datetime
#provides return_dict method for each model
from mixins import DbMixin


class InvalidUserError(Exception):
    """Raise when object passed is not a User instance"""
    pass

class InvalidGroupError(Exception):
    """Raise when object passed is not a Group instance"""
    pass


# relationship tables for members and admins
members_tbl = db.Table('members_tbl',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
    )
admins_tbl = db.Table('admins_tbl',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
    )


class Group(db.Model, DbMixin):
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

    def add_members(self, users, admin=False):
        """ Adds users to group.

        Can take either a single user or a list of users as the first argument.
        Setting admin flag to 'True' adds the users to the group's admin list.
        """
        try:
            usr = getattr(self, "members") if not admin else getattr(self, "admins")
            if isinstance(users, list):
                usr.extend(users)
                db.session.commit()
                return True
            else:
                usr.append(users)
                db.session.commit()
                return True
        except Exception as e:
            raise InvalidUserError(e)

    def remove_members(self, users, admin=False):
        """ Removes users from group.

        Can take either a single user or list of users as the first argument.
        Setting admin flag to 'True' removes the users from the group's admin
        list.
        """
        try:
            usr = getattr(self, "members") if not admin else getattr(self, "admins")
            if isinstance(users, list):
                for user in users:
                    usr.remove(user)
                db.session.commit()
            else:
                usr.remove(users)
                db.session.commit()
                return True
        except Exception as e:
            raise InvalidUserError(e)


class Company(db.Model, DbMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    group_count = db.Column(db.Integer, default=0)
    website = db.Column(db.String(255))
    groups = db.relationship('Group', backref='company')
    employees = db.relationship('User', backref='company', lazy='dynamic')

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return "{}".format(self.name)

    def add_group(self, group):
        """Adds a group to a company's list of groups."""
        try:
            groups = getattr(self, "groups")
            groups.append(group)
            db.session.commit()
            return True
        except Exception as e:
            raise InvalidGroupError(e)

    def remove_group(self, group):
        """Removes a group from a company's list of groups."""
        try:
            groups = getattr(self, "groups")
            groups.remove(group)
            db.session.commit()
            return True
        except Exception as e:
            raise InvalidGroupError(e)

    def update_group_count(self):
        """Updates the group_count attribute if the number of groups has
        changed.
        """
        group_count = getattr(self, "group_count")
        groups = getattr(self, "groups")
        if len(groups) != group_count:
            setattr(self, "group_count", len(groups))
            db.session.commit()
            return True
        return False

    def add_employees(self, user):
        """Registers users as a company employees.

        Accepts a single user or list of users as an argument.
        """
        pass

