import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from flask.ext.testing import LiveServerTestCase
from api import app, db
from api.models.tasks import Task

class TaskResourceTests(LiveServerTestCase):

    def create_app(self):
        self.app = app.test_client()
        self.app.config.from_object('config.TestConfig')
        return app

    def test_server_is_up(self):
        pass
