import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from basetest import DatabaseTestCase
from api import app, db
from api.models.groups import Company, Group
from api.models.users import User

def user_gen():
    yield {"username":"Bill", "email":"clinton@gmail.com"}
    yield {"username":"Richard", "email":"nixon@gmail.com"}
    yield {"username":"George", "email":"bush@gmail.com"}
    yield {"username":"Barack", "email":"obama@gmail.com"}

user_params = user_gen()

class GroupDbTests(DatabaseTestCase):
    def __init__(self, *args, **kwargs):
        super(GroupDbTests, self).__init__(*args, **kwargs)

    def setUp(self):
        db.create_all()
        company = Company(name="ford",
                          website="www.ford.com")
        db.session.add(company)
        group = Group(name="sedans",
                      description="4-door vehicles")
        db.session.add(group)

    def test_group_is_created_in_db(self):
        """Test group is created in the db with specified
         parameters
         """
        self.assertEqual(len(Group.query.all()), 1)
        group = Group(name="Testing",
                      description="One Two Three",
                      company_id=1)
        db.session.add(group)
        self.assertEqual(len(Group.query.all()), 2)
        self.assertEqual(group.name, "Testing")
        self.assertEqual(group.description, "One Two Three")

    def test_group_is_deleted_from_db(self):
        """Test group is deleted from the db"""
        self.assertEqual(len(Group.query.all()), 1)
        group = Group.query.filter_by(id=1).first()
        db.session.delete(group)
        self.assertEqual(len(Group.query.all()), 0)

    def test_add_single_member_to_group(self):
        """Test add single member to a group"""
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.members), 0)
        params = next(user_params)
        user = User(**params)
        group.add_members(user)
        self.assertEqual(len(group.members), 1)

    def test_add_multiple_members_to_group(self):
        """Test add an array of members to a group"""
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.members), 0)
        users = [User(**params) for params in user_gen()]
        group.add_members(users)
        self.assertEqual(len(group.members), 4)

    def test_remove_single_member_from_group(self):
        """Test remove a single user from a group"""
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.members), 0)
        params = next(user_params)
        user = User(**params)
        group.add_members(user)
        self.assertEqual(len(group.members), 1)
        group.remove_members(user)
        self.assertEqual(len(group.members), 0)

    def test_remove_multiple_members_from_group(self):
        """Test remove an array of members from a group"""
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.members), 0)
        users = [User(**params) for params in user_gen()]
        group.add_members(users)
        self.assertEqual(len(group.members), 4)
        group.remove_members(users)
        self.assertEqual(len(group.members), 0)

    def test_add_single_admin_to_group(self):
        """Test add a single admin to a group"""
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.admins), 0)
        params = next(user_params)
        user = User(**params)
        group.add_members(user, admin=True)
        self.assertEqual(len(group.admins), 1)

    def test_add_multiple_admins_to_group(self):
        """Test add an array of admins to a group"""
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.admins), 0)
        users = [User(**params) for params in user_gen()]
        group.add_members(users, admin=True)
        self.assertEqual(len(group.admins), 4)

    def test_remove_single_admin_from_group(self):
        """Test remove a single admin from a group"""
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.admins), 0)
        params = next(user_params)
        user = User(**params)
        group.add_members(user, admin=True)
        self.assertEqual(len(group.admins), 1)
        group.remove_members(user, admin=True)
        self.assertEqual(len(group.admins), 0)

    def test_remove_multiple_admins_from_group(self):
        """Test remove an array of admins from a group"""
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.admins), 0)
        users = [User(**params) for params in user_gen()]
        group.add_members(users, admin=True)
        self.assertEqual(len(group.admins), 4)
        group.remove_members(users, admin=True)
        self.assertEqual(len(group.admins), 0)


if __name__ == '__main__':
    unittest.main()

