#imports
import pygame
from map import Map
from player import Player
from taskManager import TaskManager
from netMain import Multiplayer
from meeting import Meeting

#main class
class Game:

    #constructor
    def __init__(self, s):

        #setting up map
        self.screen = s
        self.map = Map(self)

        #setting up players
        Player.loadPlayerGraphics(self)
        self.playerList = []
        p = Player( self, 400, 300, "Red")
        n = input("enter name: ")
        if n != "":
            p.name = n
        c = input("enter color: ")
        if c in Player.colors:
            p.color = c
        x = input("enter player number:")
        if int(x) % 2 == 0:
            p.isImpostor = True
        else:
            p.isImpostor = False 
        spawn_sound = pygame.mixer.Sound("spawn.wav")
        pygame.mixer.Sound.play(spawn_sound)
        #game attributes
        self.playerList.append(p)
        self.events = []
        self.gameOver = False
        self.fps = 0

        #setting up task TaskManager
        self.taskManager = TaskManager(self)

        #setting up Multiplayer
        self.multi = Multiplayer(self)

        #setting up meetings
        self.meeting = Meeting(self)

        self.multi.updateServer()

        #update all graphics
        width = self.screen.get_width()
        height = self.screen.get_height()
        if width > height:
            self.map.mapScale = width / 250
        else:
            self.map.mapScale = height / 250
        self.map.updateMapGraphics()
        Player.updatePlayerGrpahics(self)
        self.taskManager.updateIcons()
        self.meeting.updateGraphics()

    #runs every game tick
    def update(self):

        #poll all events from queue
        self.events = pygame.event.get()
        if not self.taskManager.taskActive and not self.meeting.active:
            Player.updatePlayerPos(self)

        #minimun window size
        for event in self.events:
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                if width < 250:
                    width = 250
                if height < 250:
                    height = 250
                self.screen = pygame.display.set_mode( (width,height), pygame.RESIZABLE )
                if width > height:
                    self.map.mapScale = width / 250
                else:
                    self.map.mapScale = height / 250
                self.map.updateMapGraphics()
                Player.updatePlayerGrpahics(self)
                self.taskManager.updateIcons()
                self.meeting.updateGraphics()

        #seeing is game is over
        for event in self.events:
            if event.type == pygame.QUIT:
                self.multi.disconnect()
                self.gameOver = True

        #drawing Map
        if not self.meeting.active:
            self.screen.fill((0,0,0))
            self.map.draw()
            self.taskManager.updateTasks()
        else:
            self.meeting.update()
