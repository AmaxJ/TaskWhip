import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from flask.ext.testing import TestCase
from app import app, db
from app.models import User, Task


class UserDBTests(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()

    def test_create_user(self):
        """Tests that a user is successfuly created and stored
        in the database"""
        #test no users first:
        self.assertEqual(len(User.query.all()), 0)
        user = User(username='guido',
                    email='vanRossum@gmail.com')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.email, 'vanRossum@gmail.com')
        self.assertEqual(user.username, 'guido')
        self.assertEqual(len(User.query.all()), 1)

    def test_password_verification(self):
        """Tests that a users password is registered and
        successfully verified"""
        user = User(username='Shane',
                    email='Vendrell@gmail.com')
        user.hash_password('python')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.verify_password('python'), True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TaskDBTests(TestCase):
    
    def create_app(self):    
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        user = User(username="Oscar",
                    email="acosta@yahoo.com")
        db.session.add(user)
        db.session.commit()

    def test_task_was_created(self):
        """tests task was created and stored in db with
        specified parameters."""
        #no tasks:
        self.assertEqual(len(Task.query.all()), 0)
        task = Task(title="Go to store",
                    body="Get eggs and milk.",
                    user_id=1)
        db.session.add(task)
        db.session.commit()
        self.assertEqual(len(Task.query.all()), 1)
        self.assertEqual(task.title, 'Go to store')
        self.assertEqual(task.body, 'Get eggs and milk.')
        self.assertEqual(task.user_id, 1)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__=='__main__':
    unittest.main()




