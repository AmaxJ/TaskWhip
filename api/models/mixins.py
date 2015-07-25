#useful method

class Dictify(object):

    def return_dict(self, *args, **kwargs):
        """Return column names and values as dictionary for JSON serialization"""
        error_msg = "Error returning model key-values as dictionary"
        if args:
            result = {}
            try:
                for arg in args:
                    if hasattr(self, arg):
                        arg = arg.encode("utf8")
                        attr = getattr(self, arg)
                        if type(attr) == unicode:
                            encoded = attr.encode('utf8')
                            result[arg] = encoded
                        else:
                            result[arg] = attr
                if kwargs and "uri" in kwargs.keys():
                    result["uri"] = kwargs["uri"]
                return result
            except Exception as e:
                print e
                return {"Error" : error_msg }
        else:
            try: 
                return { column.name : getattr(self, column.name) for column in self.__table__.columns }
            except Exception as e:
                print e
                return {"Error" : error_msg }
