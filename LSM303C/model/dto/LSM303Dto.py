import json
from utils.JSONSerializator import JSONSerializator

class LSM303Dto(JSONSerializator):

    def __init__(self):
        self.x = None
        self.y = None
        self.z = None


    def getJson(self):
        lsm = {
            'x': self.x,
            'y': self.y,
            'z': self.z
        }
        return json.dumps(lsm)