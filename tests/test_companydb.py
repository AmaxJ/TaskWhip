import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from basetest import DatabaseTestCase
from api import app, db
from api.models.groups import Company, Group

group_params = {
    "name":"TestGroup",
    "description":"C'est bon"
}


class CompanyDBTests(DatabaseTestCase):

    def __init__(self, *args, **kwargs):
        super(CompanyDBTests, self).__init__(*args, **kwargs)

    def setUp(self):
        db.create_all()
        company = Company(name="skynet",
                          website="www.cyberdyne.net")
        db.session.add(company)

    def test_company_is_created(self):
        """Test company is created and stored in db"""
        #one company in db currently
        self.assertEqual(len(Company.query.all()), 1)
        company = Company(name="google",
                          website="abc.xyz")
        db.session.add(company)
        self.assertEqual(len(Company.query.all()), 2)
        self.assertEqual(company.name, "google")
        self.assertEqual(company.website, "abc.xyz")

    def test_company_is_deleted(self):
        """Test company is deleted from db"""
        self.assertEqual(len(Company.query.all()), 1)
        company = Company.query.filter_by(name="skynet").first()
        db.session.delete(company)
        self.assertEqual(len(Company.query.all()), 0)

    def test_add_a_group_to_company(self):
        """Test group is added to company roster"""
        company = Company.query.filter_by(name="skynet").first()
        self.assertEqual( len(company.groups), 0)
        group = Group(**group_params)
        company.add_group(group)
        self.assertEqual( len(company.groups), 1)

    def test_remove_a_group_from_company(self):
        """Test group is removed from company roster"""
        company = Company.query.filter_by(name="skynet").first()
        group = Group(**group_params)
        company.add_group(group)
        self.assertEqual(len(company.groups), 1)
        company.remove_group(group)
        self.assertEqual(len(company.groups), 0)

    def test_group_count_is_updated(self):
        """Test group count is updated when groups are added
        or removed"""
        company = Company.query.filter_by(name="skynet").first()
        self.assertEqual(company.group_count, 0)
        group = Group(**group_params)
        company.add_group(group)
        self.assertEqual(company.group_count, 1)
        company.remove_group(group)
        self.assertEqual(company.group_count, 0)


if __name__=='__main__':
    unittest.main()
