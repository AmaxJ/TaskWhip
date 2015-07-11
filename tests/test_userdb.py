import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from flask.ext.testing import TestCase
from api import app, db
from api.models.users import User
from api.models.groups import Company


class UserDBTests(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        company = Company(name="Test Company")

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        """Test user is successfuly created and stored
        in the database"""
        #test no users first:
        self.assertEqual(len(User.query.all()), 0)
        user = User(username='guido',
                    email='vanRossum@gmail.com',
                    rank='Admin', company_id=1)
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 1)
        self.assertEqual(user.email, 'vanRossum@gmail.com')
        self.assertEqual(user.username, 'guido')
        self.assertEqual(user.rank, 'Admin')
        self.assertEqual(user.company_id, 1)
        
    def test_password_verification(self):
        """Test user's password is registered and
        successfully verified"""
        user = User(username='Shane',
                    email='Vendrell@gmail.com')
        user.hash_password('python')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.verify_password('python'), True)


if __name__=='__main__':
    unittest.main()




