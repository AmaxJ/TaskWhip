import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from datetime import datetime
from flask.ext.testing import TestCase
from api import app, db
from api.models.users import User
from api.models.tasks import Task
from api.models.groups import Company, Group


class CompanyDbTests(TestCase):

    def create_app(self):    
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        print "teardown successful"

    def test_company_was_created(self):
        """Test company is created and saved into database"""
        self.assertEqual(len(Company.query.all()), 0)
        company = Company(name="Amazon",
                          url="www.amazon.com")
        db.session.add(company)
        db.session.commit()
        company = Company.query.filter_by(id=1).first()
        self.assertEqual(len(Company.query.all()),1)
        self.assertEqual(company.name, "Amazon")
        self.assertEqual(company.url, "www.amazon.com")

    def test_company_add_employees(self):
        """Test employees successfully added to company"""
        company = Company(name="Amazon",
                          url="www.amazon.com")
        user1 = User(username="Bob", email="Bob@amazon.com",
                     rank="employee", company_id=1)
        user2 = User(username="Ed", email="Ed@amazon.com",
                     rank="manager", company_id=1) 
        db.session.add(company)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        company = Company.query.filter_by(id=1).first()
        self.assertEqual(len(company.employees.all()), 2)
        employee = company.employees.filter_by(username="Bob").first()
        self.assertEqual(employee.username, "Bob")


class GroupDbTests(TestCase):
    def create_app(self):    
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        company = Company(name="Amazon",
                          url="www.amazon.com")
        user1 = User(username="Bob", email="Bob@amazon.com",
                     rank="employee", company_id=1)
        user2 = User(username="Ed", email="Ed@amazon.com",
                     rank="Admin", company_id=1) 
        db.session.add(company)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        print "teardown successful"

    def test_group_was_created(self):
        """Test group was created and saved to database"""
        self.assertEqual(len(Group.query.all()), 0)
        group = Group(name="Review Club",
                      company_id=1, description="desc",
                      createdOn = datetime.utcnow())
        db.session.add(group)
        db.session.commit()
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(Group.query.all()), 1)
        self.assertEqual(group.name, "Review Club")
        self.assertEqual(group.company_id, 1)
        self.assertEqual(group.description, "desc")


    def test_add_members_to_group(self):
        """Test adding members and admins to group"""
        group = Group(name="Review Club",
                      company_id=1, description="desc",
                      createdOn = datetime.utcnow())
        db.session.add(group)
        db.session.commit()
        #load
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.members), 0)
        self.assertEqual(len(group.admins), 0)
        user1 = User.query.filter_by(id=1).first()
        user2 = User.query.filter_by(id=2).first()
        group.members.append(user1)
        group.admins.append(user2)
        db.session.add(group)
        db.session.commit()
        #reload
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.members), 1)
        self.assertEqual(len(group.admins), 1)

    def test_add_tasks_to_group(self):
        """Test adding tasks to a group"""
        group = Group(name="Review Club",
                      company_id=1, description="desc",
                      createdOn = datetime.utcnow())
        db.session.add(group)
        db.session.commit()
        #load
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.tasks.all()), 0)
        task = Task(title="test", body="asdf",
                    group_id=1)
        db.session.add(task)
        db.session.commit()
        #reload group
        group = Group.query.filter_by(id=1).first()
        self.assertEqual(len(group.tasks.all()), 1)



if __name__=='__main__':
    unittest.main()
