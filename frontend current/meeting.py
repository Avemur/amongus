#imports
import pygame
import time

class Meeting:

    #constructor
    def __init__(self, g):
        self.game = g
        self.active = False
        self.hovVote = None
        self.vote = None
        self.finalTally = {}
        self.resultTimer = None

        #setting up fonts
        self.fontSize = 12
        pygame.font.init()
        self.updateGraphics()

    #function tallys all the results
    def tallyResults(self):
        print(self.game.multi.client.votes)
        for v in self.game.multi.client.votes:
            if v in self.finalTally:
                self.finalTally[v] += 1
            else:
                self.finalTally[v] = 1
        print(self.finalTally)
        self.resultTimer = time.time()
        print(self.resultTimer)

    #update function while meeting in progress
    def update(self):
        self.game.screen.fill((255,255,255))
        self.game.screen.blit( self.titleSurf, (0,0) )

        #polling events
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovVote != None:
                    self.vote = self.hovVote
                    self.game.multi.updateServer()
                    self.updateGraphics()

        #drawing rects for players
        h = int((self.game.screen.get_height() - self.titleSurf.get_height()) / 5)
        w = int(self.game.screen.get_width() / 2)
        pi = 0
        color = (0,255,0)
        self.hovVote = None
        for row in range(5):
            for col in range(2):
                if pi < len(self.game.playerList):
                    x = (col * w) + 10
                    y = h * row + self.titleSurf.get_height()
                    r = pygame.Rect( ( x, y), (w - 20, int(h * 0.9) ) )
                    if color != (0,255,0) and r.collidepoint( pygame.mouse.get_pos() ) and self.vote == None:
                        color = (255,0,0)
                        self.hovVote = self.game.playerList[pi].name
                    if self.vote == self.game.playerList[pi].name:
                        color = (255,0,0)
                    if self.game.multi.status == "results":
                        color = (100,100,100)
                    pygame.draw.rect( self.game.screen, color,r )
                    x += int((r.width / 2) - (self.nameSurfs[pi].get_width() / 2))
                    y += int((r.height / 2) - (self.nameSurfs[pi].get_height() / 2))
                    self.game.screen.blit( self.nameSurfs[pi], (x,y) )
                pi += 1
                color = (100,100,100)
        #seeing if result has been shown long enough
        if self.game.multi.status == "results" and self.resultTimer != None:
            if (time.time() - self.resultTimer) > 10:
                self.vote = None
                self.resultTimer = None
                self.finalTally = {}
                self.hovVote = None
                self.active = False

    #updates graphics
    def updateGraphics(self):

        #setting up font
        self.font = pygame.font.SysFont("octin stencil", int(self.fontSize  * self.game.map.mapScale))
        if self.game.multi.status == "results":
            self.titleSurf = self.font.render("Results:", True, (0,0,0))
        else:
            self.titleSurf = self.font.render("Who Is the Imposter?", True, (0,0,0))

        #updating player name plates
        self.nameSurfs = []
        for p in self.game.playerList:
            if self.game.multi.status == "results":
                if p.name in self.finalTally:
                    self.nameSurfs.append(  self.font.render(p.name + " : " + str(self.finalTally[p.name]) + " votes", True, (0,0,0)) )
                else:
                    self.nameSurfs.append(  self.font.render(p.name + " : 0 votes", True, (0,0,0)) )
            elif p.name == self.game.playerList[0].name:
                self.nameSurfs.append(  self.font.render(p.name + " (you)", True, (0,0,0)) )
            elif p.name == self.vote:
                self.nameSurfs.append(  self.font.render(p.name + " (your vote)", True, (0,0,0)) )
            else:
                self.nameSurfs.append(  self.font.render(p.name, True, (0,0,0)) )
