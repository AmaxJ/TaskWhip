import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import unittest
from datetime import datetime
from basetest import DatabaseTestCase
from api import app, db
from api.models.users import User
from api.models.tasks import Task
from api.models.groups import Group


class TasksDBTests(DatabaseTestCase):

    def __init__(self, *args, **kwargs):
        super(TasksDBTests, self).__init__(*args, **kwargs)

    def setUp(self):
        db.create_all()
        group = Group(name="Test group",
                      created=datetime.utcnow(),
                      description="test 1 2 3")
        task = Task(title="Go to store",
                    body="Get eggs and milk.",
                    group_id=1, createdOn=datetime.utcnow())
        db.session.add(group)
        db.session.add(task)

    def test_task_was_created_with_params(self):
        """Test task created and stored in db with the
        specified parameters."""
        #one task in db currently
        self.assertEqual(len(Task.query.all()), 1)
        task = Task(title="Go to beach",
                    body="Get a tan.",
                    group_id=1, createdOn=datetime.utcnow())
        db.session.add(task)
        task = Task.query.filter_by(id=2).first();
        self.assertEqual(len(Task.query.all()), 2)
        self.assertEqual(task.title, 'Go to beach')
        self.assertEqual(task.body, 'Get a tan.')
        self.assertEqual(task.group_id, 1)

    def test_task_is_deleted(self):
        """Test task is deleted from the db"""
        self.assertEqual(len(Task.query.all()), 1)
        task = Task.query.filter_by(id=1).first()
        db.session.delete(task)
        self.assertEqual(len(Task.query.all()), 0)

    def test_task_toggleComplete(self):
        """Test toggleCommplete() method"""
        task = Task.query.filter_by(id=1).first()
        self.assertEqual(task.complete, False)
        task.toggleComplete()
        self.assertEqual(task.complete, True)
        task.toggleComplete(False)
        self.assertEqual(task.complete, False)

    def test_task_createdOn_is_datetime(self):
        """Test createdOn attribute is datetime object"""
        task = Task.query.filter_by(id=1).first()
        self.assertIsInstance(task.createdOn, datetime)

    def test_task_completedOn_is_datetime(self):
        """Test completedOn attribute is datetime object"""
        task = Task.query.filter_by(id=1).first()
        task.toggleComplete()
        self.assertIsInstance(task.completedOn, datetime)



if __name__ == '__main__':
    unittest.main()