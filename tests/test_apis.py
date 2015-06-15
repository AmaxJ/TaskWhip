import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from flask.ext.testing import LiveServerTestCase
from app import app, db
from app.models import User, Task
import db_util

class TestUserAPI(LiveServerTestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db_utils.set_users()

    def tearDown(self):
        pass
        
