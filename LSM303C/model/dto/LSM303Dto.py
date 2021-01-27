import json
from utilities.JSONSerializator import JSONSerializator

from datetime import datetime as dt


class LSM303Dto(JSONSerializator):

    def __init__(self):
        self.uuid = None
        self.x = None
        self.y = None
        self.z = None
        self.status = None
        self.created = None




    def getJson(self):
        MSG_TXT = '{{"uuid": "{uuid}", "x": {x},"y": {y}, "z": {z}, "status":{status}, "created":{created}}}'
        msg_txt_formatted = MSG_TXT.format(uuid=self.uuid, x=self.x, y=self.y, z=self.z, status=self.status, created=int(dt.now().timestamp()))
            # "UUID": str(self.uuid),
            # "x": float(self.x),
            # "y": float(self.y),
            # "z": float(self.z),
            # "status": int(self.status),
            # "created": str(int(dt.now().timestamp()))
        return msg_txt_formatted
