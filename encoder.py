from json import JSONEncoder
from model import model


class MyEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, model.CustomerStatus):
            as_dict = o.__dict__.copy()
            del as_dict['customer']
            return as_dict
        return o.__dict__