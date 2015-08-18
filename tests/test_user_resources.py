from basetest import ResourceTestCase
import json
import unittest
from api import app, db
from api.models.users import User
from api.models.groups import Company
from config import TestConfig


class UserListResourceTest(ResourceTestCase):
    """Test of the UserListAPI resource"""

    def __init__(self, *args, **kwargs):
        ResourceTestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        db.create_all()
        company = Company(name="testcompany")
        user1 = User(
            username="Oscar",
            email="acosta@yahoo.com",
            company_id=1
        )
        user2 = User(
            username="Raoul",
            email="duke@gmail.com",
            company_id=1
        )
        db.session.add(company)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def test_get_all_users(self):
        """Test GET to /users resource returns list of users"""
        rv = self.app.get(self.URLROOT + "/users")
        data = json.loads(rv.data)
        self.assertEqual(len(data["users"]), 2)

    def test_create_new_user(self):
        """Test POST to /users resource"""
        rv = self.app.get(self.URLROOT + "/users")
        self.assertEqual(len(json.loads(rv.data)["users"]), 2)
        rv = self.app.post(self.URLROOT + "/users",
            data=json.dumps(dict(username="Guido",
                                email="vanRossum@gmail.com",
                                company_id=1)),
            content_type='application/json')
        rv = self.app.get(self.URLROOT + "/users")
        data = json.loads(rv.data)
        self.assertEqual(len(data["users"]), 3)


class UserApiResourceTest(ResourceTestCase):
    """Test of the UserAPI resource"""

    def __init__(self, *args, **kwargs):
        ResourceTestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        db.create_all()
        company = Company(name="testcompany")
        user = User(
            username="Oscar",
            email="acosta@yahoo.com",
            company_id=1
        )
        db.session.add(company)
        db.session.add(user)
        db.session.commit()

    def test_get_single_user(self):
        """Test GET to users/<user_id>/ returns a single user"""
        rv = self.app.get(self.URLROOT + "/users/1" )
        data = json.loads(rv.data)
        self.assertEqual(data["user"]["username"], "Oscar")

    def test_put_change_email(self):
        """Test change email with PUT to users/<user_id>/"""
        rv = self.app.get(self.URLROOT + "/users/1" )
        data = json.loads(rv.data)
        self.assertEqual(data["user"]["email"], "acosta@yahoo.com")
        rv = self.app.put(self.URLROOT + "/users/1",
            data=json.dumps(dict(email="testing@yahoo.com")),
            content_type='application/json')
        rv = self.app.get(self.URLROOT + "/users/1" )
        data = json.loads(rv.data)
        self.assertEqual(data["user"]["email"], "testing@yahoo.com")

    def test_put_change_username(self):
        """Test change email with PUT to users/<user_id>/"""
        rv = self.app.get(self.URLROOT + "/users/1" )
        data = json.loads(rv.data)
        self.assertEqual(data["user"]["username"], "Oscar")
        rv = self.app.put(self.URLROOT + "/users/1",
            data=json.dumps(dict(username="Bob")),
            content_type='application/json')
        rv = self.app.get(self.URLROOT + "/users/1" )
        data = json.loads(rv.data)
        self.assertEqual(data["user"]["username"], "Bob")

    def test_delete_a_single_user(self):
        """Test GET to users/<user_id>/ returns a single user"""
        rv = self.app.get(self.URLROOT + "/users" )
        data = json.loads(rv.data)
        self.assertEqual(len(data["users"]), 1)
        rv = self.app.delete(self.URLROOT + "/users/1")
        data = json.loads(rv.data)
        self.assertEqual(data["deleted"], True)
        rv = self.app.get(self.URLROOT + "/users")
        data = json.loads(rv.data)
        self.assertEqual(len(data["users"]), 0)




if __name__ == '__main__':
    unittest.main()





