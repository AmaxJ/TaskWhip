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
    """Resource for all groups for all companies"""

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
    """Resource for all groups of a specific company by ID"""

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
                print e
                return {"error":"Problem retrieving groups",
                        "msg" : str(e)}, 404
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
                #admins will be passed as a string of comma separated id numbers
                admins = [int(id) for id in args["admins"].split(",")]
                for id in admins:
                    admin = User.query.filter_by(id=id).first()
                    if admin is not None:
                        newGroup.admins.append(admin)
            if args["members"] is not None:
                #members passed as a string of comma separated id numbers
                members = [int(id) for id in args["members"].split(",")]
                for id in members:
                    member = User.query.filter_by(id=id).first()
                    if member is not None:
                        newGroup.members.append(member)
            db.session.add(newGroup)
            db.session.commit()
            return {"group": marshal(newGroup, group_fields)}
        except Exception as e:
            print e
            return {"error":"Problem creating group",
                    "msg" : str(e) }


class GroupAPI(Resource):
    """Resource for an individual group."""

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("description", type=str, location="json",
                                 trim=True)
        #members and admins will be a string of id numbers separated by commas.
        self.parser.add_argument("add_members", type=str, location="json")
        self.parser.add_argument("add_admins", type=str, location="json")
        self.parser.add_argument("remove_members", type=str, location="json")
        self.parser.add_argument("remove_admins", type=str, location="json")

        super(GroupAPI, self).__init__()

    def _parse_ids(self, idString):
        return map(lambda x: int(x), idString.split(","))

    def get(self, company_id, id):
        group = Group.query.filter_by(company_id=company_id, id=id).first()
        if group is not None:
            try:
                return { "group": marshal(group, group_fields) }
            except Exception as e:
                print "Error: ", e
                return { "error": "Error retrieving group",
                         "msg" : str(e) }
        else:
            return { "error" : "Group not found" }, 404

    def put(self, company_id, id):
        group = Group.query.filter_by(company_id=company_id, id=id).first()
        if group is not None:
            try:
                args = self.parser.parse_args()
                if args["add_members"] is not None:
                    member_ids = self._parse_ids(args["add_members"])
                    members = [User.query.filter_by(id=id).first() for id in member_ids]
                    group.add_members(members)
                    return {"group" : marshal(group, group_fields) }, 200
                elif args["remove_members"] is not None:
                    member_ids = self._parse_ids(args["remove_members"])
                    members = [User.query.filter_by(id=id).first() for id in member_ids]
                    group.remove_members(members)
                    return {"group" : marshal(group, group_fields) }, 200
                elif args["add_admins"] is not None:
                    admin_ids = self._parse_ids(args["add_admins"])
                    admins = [User.query.filter_by(id=id).first() for id in admin_ids]
                    group.add_members(admins, admin=True)
                    return {"group" : marshal(group, group_fields) }, 200
                elif args["remove_admins"] is not None:
                    admin_ids = self._parse_ids(args["remove_admins"])
                    admins = [User.query.filter_by(id=id).first() for id in admin_ids]
                    group.remove_members(admins, admin=True)
                    return {"group" : marshal(group, group_fields) }, 200
                else:
                    for key, value in args.items():
                        if args[key] is not None and hasattr(group, key):
                            setattr(group, key, value)
                    db.session.commit()
                    return {"group" : marshal(group, group_fields)}, 200
            except Exception as e:
                print e
                return {"error":"Error editing group",
                        "msg" : str(e) }
        else:
            return {"error":"Group not found"}

    def delete(self, company_id, id):
        pass






