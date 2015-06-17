from api import db
from api.models import Task
from flask_restful import Resource, fields, marshal, reqparse
from datetime import datetime

task_fields = {
    'title' : fields.String,
    'body' : fields.String,
    'created' : fields.DateTime,
    'user_id' : fields.Integer,
    'id' : fields.Integer,
    'uri' : fields.Url('task')
}

class TaskListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, required=True,
                                 location='json', help='Title required',
                                 trim=True)
        self.parser.add_argument('body', type=str, required=False,
                                 location='json')
        super(TaskListAPI, self).__init__()

    def get(self, user_id):
        tasks = Task.query.filter_by(user_id=user_id)
        return {'tasks':[marshal(task, task_fields) for task in tasks]}
    
    def post(self, user_id):
        args = self.parser.parse_args()
        newTask = Task(user_id=user_id,
                       title=args["title"],
                       body=args["body"],
                       created=datetime.now())
        db.session.add(newTask)
        db.session.commit()
        return {'task': marshal(newTask, task_fields) }


class TaskAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, location='json', 
                                 trim=True)
        self.parser.add_argument('body', type=str, location='json')
        super(TaskAPI, self).__init__()

    def get(self, user_id, id): #task_id
        task = Task.query.filter_by(user_id=user_id, id=id).first()
        if task:
            return {'task': marshal(task, task_fields) }
        return {"error": "Task not found"}, 404
    
    def put(self, user_id, id): #task_id
        task = Task.query.filter_by(user_id=user_id, id=id).first()
        if task is not None:
            args = self.parser.parse_args()
            for key, value in args.items():
                if args[key] is not None:
                    setattr(task, key, value)
            db.session.commit()
            return {'task': marshal(task, task_fields) }
        return {"error": "Task not found"}, 404

    def delete(self, user_id, id):#task_id
        task = Task.query.filter_by(user_id=user_id, id=id).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            return {"deleted":True}
        return {"error", "Task not found"}, 404
