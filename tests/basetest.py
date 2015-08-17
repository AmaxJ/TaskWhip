import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from api import db, app
from datetime import datetime
from api.models.users import User
from api.models.tasks import Task
from api.models.groups import Group
import unittest
import json
from config import TestConfig

app.config.from_object('config.TestConfig')


class BaseTestCase(unittest.TestCase):
    """Base class for all test cases"""

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.app = app.test_client()

    def setUp(self):
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class ResourceTestCase(BaseTestCase):
    """Base class for all resource test cases"""

    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, *args, **kwargs)
        self.URLROOT = "/taskx/api/v{version}".format(version=TestConfig.API_VERSION)


class DatabaseTestCase(BaseTestCase):
    """Base class for all database test cases"""
    pass





