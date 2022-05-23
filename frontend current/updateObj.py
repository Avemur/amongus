import json
from client import Client

class PlayerUpdateObj:

    def __init__(self, game):
        self.x = None
        self.y = None
        self.name = None
        self.color = None
        self.status = None
        self.game = game

    def getJson(self):
        return json.dumps({ "x": self.x, "y": self.y, "name": self.name, "color": self.color, "status": self.status, "vote": self.game.meeting.vote})
