from api import db
from api.models.tasks import Task
from flask_restful import Resource, fields, marshal, reqparse
from datetime import datetime

task_fields = {
    'title' : fields.String,
    'body' : fields.String,
    'createdOn' : fields.DateTime,
    'completedOn' : fields.DateTime,
    'group_id' : fields.Integer,
    'id' : fields.Integer,
    'complete' : fields.Boolean,
    'status' : fields.String,
    'timeActive' : fields.Integer,
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

    def get(self):
        tasks = Task.query.all()
        return {'tasks':[marshal(task, task_fields) for task in tasks]}


class TasksByGroup(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, required=True,
                                 location='json', help='Title required',
                                 trim=True)
        self.parser.add_argument('body', type=str, required=False,
                                 location='json')        

    def get(self, group_id):
        tasks = Task.query.filter_by(group_id=group_id)
        if tasks:
            return { 'tasks' : [marshal(task, task_fields) for task in tasks] }, 200
        return { 'Error' : 'No tasks found'}, 404

    def post(self, group_id):
        args = self.parser.parse_args()
        try:
            newTask = Task(group_id=group_id,
                           title=args["title"],
                           body=args["body"],
                           created=datetime.now())
            db.session.add(newTask)
            db.session.commit()
            return {'task': marshal(newTask, task_fields) }
        except Exception:
            print Exception
            return { 'Error' : 'Sorry, something went wrong!' }


class TaskAPI(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, location='json', 
                                 trim=True)
        self.parser.add_argument('body', type=str, location='json'),
        self.parser.add_argument('complete', type=str, location='json')
        self.parser.add_argument('status', type=str, location='json')
        super(TaskAPI, self).__init__()

    def get(self, group_id, id): #task_id
        task = Task.query.filter_by(group_id=group_id, id=id).first()
        if task:
            return {'task': marshal(task, task_fields) }
        return {"Error": "Task not found"}, 404
    
    def put(self, group_id, id): #task_id
        task = Task.query.filter_by(group_id=group_id, id=id).first()
        args = self.parser.parse_args()
        if task:
            try: 
                #if task complete then change status and return
                if args["complete"] == "true":
                    task.toggleComplete(True)
                    db.session.commit()
                    return { 'task' : marshal(task, task_fields) }
                elif args["complete"] == "false":
                    task.toggleComplete(False)
                    return { 'task' : marshal(task, task_fields) } 
                for key, value in args.items():
                    if args[key] is not None:
                        setattr(task, key, value)
                db.session.commit()
                return {'task': marshal(task, task_fields) }
            except Exception as err:
                print err
                return { "Error" : "Sorry, something went wrong!" }
        return {"Error": "Task not found"}, 404

    def delete(self, group_id, id):#task_id
        task = Task.query.filter_by(group_id=group_id, id=id).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            return {"deleted" : True}
        return {"Error" : "Task not found"}, 404
