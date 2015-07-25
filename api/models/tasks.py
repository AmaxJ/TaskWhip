from api import db
from datetime import datetime 
from api.models.groups import Group
from mixins import Dictify


class Task(db.Model, Dictify):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    createdOn = db.Column(db.DateTime, default=datetime.now)
    completedOn = db.Column(db.DateTime)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    complete = db.Column(db.Boolean, default=False)
    #status values: pending, complete, unassigned
    status = db.Column(db.String, default="pending")
    timeActive = db.Column(db.Integer)


    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return "{}: {}".format(self.group_id, self.title)

    def toggleComplete(self, boolean=True):
        if boolean:
            setattr(self, "complete", True)
            setattr(self, "completedOn", datetime.now())
            setattr(self, "status", "completed")
            delta = self.completedOn - self.createdOn
            setattr(self, "timeActive", delta.seconds)
        else:
            setattr(self, "complete", False)
            setattr(self, "status", "pending")

            
