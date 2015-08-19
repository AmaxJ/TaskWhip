import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from basetest import DatabaseTestCase
from api import app, db
from api.models.users import User
from api.models.groups import Company

class UserDBTests(DatabaseTestCase):

    def __init__(self, *args, **kwargs):
        super(UserDBTests, self).__init__(*args, **kwargs)

    def setUp(self):
        db.create_all()
        company = Company(name="test company")
        user = User(username='guido',
                    email='vanRossum@gmail.com',
                    rank='Admin', company_id=1)
        db.session.add(company)
        db.session.add(user)

    def test_user_is_created_in_db(self):
        """Test user is successfuly created and stored
        in the database"""
        #One user in db currently
        self.assertEqual(len(User.query.all()), 1)
        user = User(username='patrice',
                    email='oneal@gmail.com',
                    rank='Admin', company_id=1)
        db.session.add(user)
        self.assertEqual(len(User.query.all()), 2)
        self.assertEqual(user.email, 'oneal@gmail.com')
        self.assertEqual(user.username, 'patrice')
        self.assertEqual(user.rank, 'Admin')
        self.assertEqual(user.company_id, 1)

    def test_user_is_deleted_from_db(self):
        """Test user is successfully deleted from the database"""
        #one user in db currently
        self.assertEqual(len(User.query.all()), 1)
        user = User.query.filter_by(username="guido").first()
        db.session.delete(user)
        self.assertEqual(len(User.query.all()), 0)


    def test_password_verification(self):
        """Test user's password is registered and
        successfully verified"""
        user = User.query.filter_by(username="guido").first()
        user.hash_password('python')
        self.assertEqual(user.verify_password('python'), True)


if __name__=='__main__':
    unittest.main()




