from api import db
from api.models.groups import Company
from flask import make_response, url_for
import json
from flask_restful import Resource, reqparse


class CompanyList(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('name', type=str,
                                  location='json')
        self.parser.add_argument('website', type=str, location='json')

    def get(self):
        query = Company.query.all()
        if len(query) > 0:
            companies = []
            try:
                for company in query:
                    company_id = getattr(company, 'id')
                    uri = url_for("company", id=company_id)
                    companies.append(company.return_dict("name", "website", uri=uri))
                response = make_response(json.dumps( {"companies" : companies } ))
                response.headers["content-type"] = "application/json"
                return response
            except Exception as e:
                print e
                return {"error" : "Could not retrieve companies"}
        return {"error" : "No companies found"}


    def post(self):
        try:
            args = self.parser.parse_args()
            newCompany = Company(name=args["name"])
            if args["website"] is not None:
                setattr(newCompany, 'website', args['website'])
            db.session.add(newCompany)
            db.session.commit()
            uri = url_for("company", id=newCompany.id)
            company = Company.query.filter_by(name=args["name"]).first()
            company = company.return_dict("name", "website", uri=uri)
            response = make_response(json.dumps({"company" : company }))
            response.headers["content-type"] = "application/json"
            return response
        except Exception as e:
            print e
            return {"error" : "Error creating new company" }


class CompanyAPI(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('website', type=str, location='json')

    def get(self, id):
        try:
            company = Company.query.filter_by(id=id).first()
            uri = url_for("company", id=id)
            company = company.return_dict("name", "website", uri=uri)
            response = make_response(json.dumps({"company":company}))
            response.headers["content-type"] = "application/json"
            return response 
        except Exception as e:
            print e
            return { 'error' : "Sorry, company not found" }, 404

    def put(self, id):
        company = Company.query.filter_by(id=id).first()
        if company is not None:
            try:
                args = self.parser.parse_args()
                for key, value in args.items():
                    if args[key] is not None:
                        setattr(company, key, value)
                db.session.commit()
                uri = url_for("company", id=id)
                company = company.return_dict("name", "website", uri=uri)
                response = make_response(json.dumps({"company":company}))
                response.headers["content-type"] = "application/json"
                return response 
            except Exception as e:
                print e
                return { 'error' : "Edit failed" }
        return { 'error' : "Company not found" }, 404

    def delete(self, id):
        company = Company.query.filter_by(id=id).first()
        if company:
            try:
                db.session.delete(company)
                db.session.commit()
                return {"deleted" : True }
            except Exception as e:
                print e
                return { "error" : "Delete unsuccessful" }

        