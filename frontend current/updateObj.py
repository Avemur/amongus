import json
from client import Client

class PlayerUpdateObj:

    def __init__(self):
        self.x = None
        self.y = None
        self.name = None
        self.color = None

    def getJson(self):
        return json.dumps({ "x": self.x, "y": self.y, "name": self.name, "color": self.color})
