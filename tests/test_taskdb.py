import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from datetime import datetime
from flask.ext.testing import TestCase
from api import app, db
from api.models.users import User
from api.models.tasks import Task
from api.models.groups import Group 


class TaskDBTests(TestCase):
    
    def create_app(self):    
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        user = User(username="Oscar",
                    email="acosta@yahoo.com")
        group = Group(name="Test group",
                      created=datetime.utcnow(),
                      description="test 1 2 3")
        db.session.add(group)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_task_was_created(self):
        """Test task created and stored in db with
        specified parameters."""
        #no tasks:
        self.assertEqual(len(Task.query.all()), 0)
        task = Task(title="Go to store",
                    body="Get eggs and milk.",
                    group_id=1, created=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        task = Task.query.filter_by(id=1).first();
        self.assertEqual(len(Task.query.all()), 1)
        self.assertEqual(task.title, 'Go to store')
        self.assertEqual(task.body, 'Get eggs and milk.')
        self.assertEqual(task.group_id, 1)

    def test_task_toggleComplete(self):
        """Test toggleCommplete() method"""
        task = Task(title="Go to store",
                    body="Get eggs and milk.",
                    group_id=1, created=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        task = Task.query.filter_by(id=1).first()
        self.assertEqual(task.completed, False)
        task.toggleComplete()
        self.assertEqual(task.completed, True)
        task.toggleComplete(False)
        self.assertEqual(task.completed, False)


if __name__=='__main__':
    unittest.main()
