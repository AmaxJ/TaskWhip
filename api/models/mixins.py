from datetime import datetime 
from flask import make_response
import json

class DbMixin:

    def return_dict(self, uri=None, *args):
        """Return column names and values as dictionary for JSON serialization.
        Encodes unicode to utf-8 and datetime objects to ISO 8601."""
        if args:
            result = {}
            try:
                if uri is not None:
                    result["uri"] = uri
                for arg in args:
                    if hasattr(self, arg):
                        arg = arg.encode("utf8")
                        attr = getattr(self, arg)
                        if type(attr) == unicode:
                            attr = attr.encode('utf8')
                            result[arg] = attr
                        elif isinstance(attr, datetime):
                            attr = attr.isoformat()
                            result[arg] = attr
                        else:
                            result[arg] = attr
                return result
            except Exception as e:
                print e
        else:
            try:
                result = { column.name : getattr(self, column.name) for column in self.__table__.columns }
                if uri is not None:
                    result["uri"] = uri
            except Exception as e:
                print e



