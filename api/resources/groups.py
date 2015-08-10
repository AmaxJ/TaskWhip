from api import db
from api.models.groups import Group
from api.models.users import User
from flask_restful import Resource, fields, marshal, reqparse
from flask import url_for
from datetime import datetime

group_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "company_id" : fields.Integer,
    "description" : fields.String,
    "createdOn" : fields.DateTime,
    "members" : fields.List(fields.String),
    "admins" : fields.List(fields.String),
    "uri" : fields.Url("group")
}


class GroupList(Resource):
    """Returns a list of all groups for all companies"""

    def get(self):
        groups = Group.query.all()
        if len(groups) > 0:
            try:
                return {"groups": [marshal(group, group_fields) for group in groups] }, 200
            except Exception as e:
                print e
                return {"error":"Problem retrieving groups"}, 404
        else:
            return {"error" : "No groups found"}, 404


class GroupListByCompanyId(Resource):
    """Returns a list of all groups for a specific company"""

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("name", type=str, required=True,
                                 location="json", help="Name required",
                                 trim=True)
        self.parser.add_argument("description", type=str, location="json",
                                 trim=True)
        #members and admins will be a string of id numbers separated by commas.
        self.parser.add_argument("members", type=str, location="json")
        self.parser.add_argument("admins", type=str, location="json")
        super(GroupListByCompanyId, self).__init__()

    def get(self, company_id):
        groups = Group.query.filter_by(company_id=company_id).all()
        if len(groups) > 0:
            try:
                return {"groups":[marshal(group, group_fields) for group in groups] }, 200
            except Exception as e:
                print "ERROR: ", e
                return {"error":"Problem retrieving groups"}, 404
        else:
            return {"error":"No groups found"}, 404

    def post(self, company_id):
        args = self.parser.parse_args()
        try:
            newGroup = Group(
                    name=args["name"],
                    description=args["description"],
                    company_id=company_id
            )
            if args["admins"] is not None:
                admins = [int(id) for id in args["admins"].split(",")]
                for id in admins:
                    try:
                        admin = User.query.filter_by(id=id).first()
                        if admin is not None:
                            newGroup.admins.append(admin)
                    except Exception as e:
                        print "Error adding admin id #: ", id
                        print e
            if args["members"] is not None:
                members = [int(id) for id in args["members"].split(",")]
                for id in members:
                    try:
                        member = User.query.filter_by(id=id).first()
                        if member is not None:
                            newGroup.members.append(member)
                    except Exception as e:
                        print "Error adding member id #: ", id
                        print e
            db.session.add(newGroup)
            db.session.commit()
            return {"group": marshal(newGroup, group_fields)}
        except Exception as e:
            print e
            return {"error":"Problem creating group"}, 404


class GroupAPI(Resource):
    """Returns an individual group."""

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("description", type=str, location="json",
                                 trim=True)
        #members and admins will be a string of id numbers separated by commas.
        self.parser.add_argument("members", type=str, location="json")
        self.parser.add_argument("admins", type=str, location="json")
        super(GroupAPI, self).__init__()

    def get(self, company_id, id):
        group = Group.query.filter_by(company_id=company_id, id=id).first()
        if group is not None:
            try:
                return { "group": marshal(group, group_fields) }
            except Exception as e:
                print "Error: ", e
                return { "error": "Error retrieving group" }
        else:
            return { "error" : "Group not found" }

    #TODO:
        #make an add user/admin method and also make a way to remove users.
        #clean this mess up
    def put(self, company_id, id):
        group = Group.query.filter_by(company_id=company_id, id=id).first()
        if group is not None:
            try:
                args = self.parser.parse_args()
                if args["members"] is not None:
                    members = [int(memberID) for memberID in args["members"].split(",")]
                    for userID in members:
                        member = User.query.filter_by(id=userID).first()
                        if member not in group.members:
                            group.members.append(member)
                    db.session.commit()
                    return {"group" : marshal(group, group_fields) }, 200
                elif args["admins"] is not None:
                    admins = [int(adminID) for adminID in args["admins"].split(",")]
                    for adminID in admins:
                        admin = User.query.filter_by(id=adminID).first()
                        if admin not in group.admins:
                            group.admins.append(admin)
                    db.session.commit()
                    return {"group" : marshal(group, group_fields) }, 200
                for key, value in args.items():
                    if args[key] is not None and hasattr(group, key):
                        setattr(group, key, value)
                db.session.commit()
                return {"group" : marshal(group, group_fields)}, 200
            except Exception as e:
                print e
                return {"error":"Error editing group"}
        else:
            return {"error":"Group not found"}

    def delete(self, company_id, id):
        pass






