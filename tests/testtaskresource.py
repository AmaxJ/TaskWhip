import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from flask.ext.testing import LiveServerTestCase
from api import app, db
from api.models.tasks import Task
import requests as req 

class TaskResourceTests(LiveServerTestCase):

    def create_app(self):
        self.app = app.test_client()
        self.app.config.from_object('config.TestConfig')
        return self.app

    def test_server_is_up(self):
        response = r.get('http://127.0.0.1:8080/taskx/api/v0/tasks')
        self.assertEqual(response.response_code, 200)


if __name__ == '__main__':
    unittest.main()
