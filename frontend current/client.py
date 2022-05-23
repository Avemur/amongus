#import socketing and threading
import socket
import threading
import json
from player import Player

#client class
class Client:

    #constructor
    def __init__(self, game):

        #constants
        self.HEADER = 64
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "leave"
        self.SERVER_IP = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER_IP, self.PORT)
        self.game = game
        self.votes = []

        #creating socket
        print("[cleint] socket created")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connects
    def connect(self):
        self.client.connect(self.ADDR)
        print("[cleint] connected")

        #starting reciving
        thread = threading.Thread(target=self.recever)
        thread.start()

    #sends stuff
    def send(self, msg):

        #formatting
        message = msg.encode(self.FORMAT)

        #creating length header
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))

        #sending header then message
        self.client.send(send_length)
        self.client.send(message)

    #stays reciving things
    def recever(self):
        while not self.game.gameOver:
            msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:

                #processing message
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(self.FORMAT)
                serverUpdate = json.loads(msg)
                serverPlayers = serverUpdate["players"]

                #updating game state


                if serverUpdate["gameStatus"] == "voting" and not self.game.meeting.active:
                    self.game.meeting.updateGraphics()
                    self.game.meeting.active = True

                #updaitng votes
                self.votes = []

                #updating players
                for sp in serverPlayers:
                    if sp != None:
                        found = False
                        self.votes.append( sp["vote"] )
                        for lp in self.game.playerList:
                            if lp != None and sp != None:
                                if sp["name"] == lp.name:
                                    lp.x = sp["x"]
                                    lp.y = sp["y"]
                                    found = True
                        if not found:
                            if sp != None:
                                p = Player( self.game, sp["x"], sp["y"], sp["color"], n = sp["name"])
                                self.game.playerList.append(p)

                #removing players that no longer exist
                for lpi in reversed( range( len( self.game.playerList ) ) ):
                    found = False
                    for sp in serverPlayers:
                        if sp != None and sp["name"] == self.game.playerList[lpi].name:
                            found = True
                    if not found:
                        del self.game.playerList[lpi]

                #voting
                if serverUpdate["gameStatus"] == "results" and self.game.multi.status == "voting":
                    self.game.meeting.vote = None
                    self.game.multi.updateServer()
                    self.game.meeting.tallyResults()
                    self.game.multi.status = serverUpdate["gameStatus"]
                    self.game.meeting.updateGraphics()
                self.game.multi.status = serverUpdate["gameStatus"]
    #disconnecting
    def disconnect(self):
        self.send(self.DISCONNECT_MESSAGE)
        print("[cleint] disconnected")
