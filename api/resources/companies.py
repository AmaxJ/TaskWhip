from api import db
from api.models.groups import Company
from flask_restful import Resource, fields, marshal, reqparse

company_fields = {
    'name' : fields.String,
    'website' : fields.String,
    'uri' : fields.Url('company')
}

class CompanyList(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('name', type=str,
                                  location='json')
        self.parser.add_argument('website', type=str, location='json')

    def get(self):
        companies = Company.query.all()
        return { 'companies' : [ marshal(company, company_fields) for company in companies ] }

    def post(self):
        try:
            args = self.parser.parse_args()
            newCompany = Company(name=args["name"])
            if args["website"] is not None:
                setattr(newCompany, 'website', args['website'])
            db.session.add(newCompany)
            db.session.commit()
            return {'company' : marshal(newCompany, company_fields) }
        except Exception as e:
            print e
            return {"error" : str(e) }


class CompanyAPI(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('website', type=str, location='json')

    def get(self, id):
        try:
            company = Company.query.filter_by(id=id).first()
            return { 'company' : marshal(company, company_fields) }
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
                return { "company" : marshal(company, company_fields) }
            except Exception as e:
                print e
                return { 'error' : "Edit failed" }
        return { 'error' : "Company not found" }, 404

        