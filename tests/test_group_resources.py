import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
import json
from basetest import ResourceTestCase
from api import app, db
from api.models.groups import Company, Group
from api.models.users import User

#TODO put these generators in utils
def user_gen():
    yield {"username":"Bill", "email":"clinton@gmail.com"}
    yield {"username":"Richard", "email":"nixon@gmail.com"}
    yield {"username":"George", "email":"bush@gmail.com"}
    yield {"username":"Barack", "email":"obama@gmail.com"}

def group_gen():
    yield {"name":"Cops", "description":"Drink Whiskey", "company_id":1}
    yield {"name":"Robbers", "description":"Drink Rum", "company_id":1}
    yield {"name":"Politicians", "description":"Drink Vodka", "company_id":1}
    yield {"name":"Civilians", "description":"Drink Gin", "company_id":1}

user_params = user_gen()

class GroupList(ResourceTestCase):
    """Test of the GroupList resource"""

    def __init__(self, *args, **kwargs):
        super(GroupList, self).__init__(*args, **kwargs)

    def setUp(self):
        db.create_all()
        company = Company(name="TestCompany")
        db.session.add(company)
        #just for fun:
        # [db.session.add(Group(**group)) for group in group_gen()]
        # map(lambda params: db.session.add(Group(**params)), group_gen())
        # filter(lambda params: db.session.add(Group(**params)), group_gen())
        for params in group_gen():
            db.session.add(Group(**params))
        db.session.commit()

    def test_get_all_groups(self):
        """Test GET to /groups resource"""
        rv = self.app.get(self.URLROOT + '/groups')
        data = json.loads(rv.data)
        self.assertEqual(len(data['groups']), 4)


class GroupListByCompanyID(ResourceTestCase):
    """Test of the GroupListByCompanyID resource"""

    def __init__(self, *args, **kwargs):
        super(GroupListByCompanyID, self).__init__(*args, **kwargs)

    def setUp(self):
        db.create_all()
        company = Company(name="TestCompany")
        db.session.add(company)
        for params in group_gen():
            db.session.add(Group(**params))
        db.session.commit()

    def test_get_all_groups_by_company(self):
        """Test GET to /<company_id>/groups resource"""
        rv = self.app.get(self.URLROOT + '/1/groups')
        data = json.loads(rv.data)
        self.assertEqual(len(data['groups']), 4)

    def test_create_new_group_no_members(self):
        """Test POST to /<company_id>/groups resource no members"""
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 4)
        rv = self.app.post(self.URLROOT + '/1/groups',
                          data=json.dumps(dict(name="Test",
                                              description="group test")),
                          content_type='application/json')
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 5)
        group = groupList[4]
        self.assertEqual(group['name'], 'Test')
        self.assertEqual(group['description'], 'group test')

    def test_create_new_group_one_member(self):
        """Test POST to /<company_id>/groups resource add one member"""
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 4)
        params = next(user_params)
        user = User(**params)
        db.session.add(user)
        rv = self.app.post(self.URLROOT + '/1/groups',
                          data=json.dumps(dict(name="Test",
                                              description="group test",
                                              company_id=1,
                                              members="1")),
                          content_type='application/json')
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 5)
        members = groupList[4]["members"]
        self.assertEqual(len(members), 1)

    def test_create_new_group_multiple_members(self):
        """Test POST to /<company_id>/groups resource add multiple members"""
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 4)
        users = [db.session.add(User(**params)) for params in user_gen()]
        rv = self.app.post(self.URLROOT + '/1/groups',
                          data=json.dumps(dict(name="Test",
                                              description="group test",
                                              company_id=1,
                                              members="1,2,3,4")),
                          content_type='application/json')
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 5)
        members = groupList[4]["members"]
        self.assertEqual(len(members), 4)

    def test_create_new_group_one_admin(self):
        """Test POST to /<company_id>/groups resource add one admin"""
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 4)
        params = next(user_params)
        user = User(**params)
        db.session.add(user)
        rv = self.app.post(self.URLROOT + '/1/groups',
                          data=json.dumps(dict(name="Test",
                                              description="group test",
                                              company_id=1,
                                              admins="1")),
                          content_type='application/json')
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 5)
        admins = groupList[4]["admins"]
        self.assertEqual(len(admins), 1)

    def test_create_new_group_multiple_admins(self):
        """Test POST to /<company_id>/groups resource add multiple admins"""
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 4)
        users = [db.session.add(User(**params)) for params in user_gen()]
        rv = self.app.post(self.URLROOT + '/1/groups',
                          data=json.dumps(dict(name="Test",
                                              description="group test",
                                              company_id=1,
                                              admins="1,2,3,4")),
                          content_type='application/json')
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 5)
        admins = groupList[4]["admins"]
        self.assertEqual(len(admins), 4)

    def test_create_new_group_multiple_admins_and_members(self):
        """Test POST to /<company_id>/groups resource add multiple admins"""
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 4)
        users = [db.session.add(User(**params)) for params in user_gen()]
        rv = self.app.post(self.URLROOT + '/1/groups',
                          data=json.dumps(dict(name="Test",
                                              description="group test",
                                              company_id=1,
                                              admins="1,2",
                                              members="3,4")),
                          content_type='application/json')
        rv = self.app.get(self.URLROOT + '/1/groups')
        groupList = json.loads(rv.data)["groups"]
        self.assertEqual(len(groupList), 5)
        admins = groupList[4]["admins"]
        members = groupList[4]["members"]
        self.assertEqual(len(admins), 2)
        self.assertEqual(len(members), 2)


class GroupAPI(ResourceTestCase):
    pass

if __name__ == '__main__':
    unittest.main()