import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from api import db, app
import unittest
from config import TestConfig

app.config.from_object('config.TestConfig')


class BaseTestCase(unittest.TestCase):
    """Base class for all test cases"""

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.app = app.test_client()

    def setUp(self):
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class ResourceTestCase(BaseTestCase):
    """Base class for all resource test cases"""

    def __init__(self, *args, **kwargs):
        super(ResourceTestCase, self).__init__(*args, **kwargs)
        self.URLROOT = "/taskx/api/v{version}".format(version=TestConfig.API_VERSION)


class DatabaseTestCase(BaseTestCase):
    """Base class for all database test cases"""
    pass





