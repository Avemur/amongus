from client import Client
from updateObj import PlayerUpdateObj

#handels all mutiplayer aspects
class Multiplayer:

    #constructor
    def __init__(self, g):
        self.game = g
        self.client = Client(g)
        self.client.connect()
        self.updateObj = PlayerUpdateObj()
        self.updatePlayerObj()

    #update player update object
    def updatePlayerObj(self):
        self.updateObj.x = self.game.playerList[0].x
        self.updateObj.y = self.game.playerList[0].y
        self.updateObj.name = self.game.playerList[0].name
        self.updateObj.color = self.game.playerList[0].color

    #updates server
    def updateServer(self):
        self.updatePlayerObj()
        self.client.send(self.updateObj.getJson())

    #disconnects
    def disconnect(self):
        self.client.disconnect()
