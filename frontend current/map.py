#imports
import pygame
import json
from player import Player

#map class
class Map:

    #constructor
    def __init__(self, game):
        self.screen = game.screen
        self.game = game
        with open("map.json") as f:
            self.sprites = json.load(f)
        self.spriteAsssets = {}
        self.mapScale = 0.5
        self.mapOffsets = [0,0]
        self.loadMapGraphics()

    #drawing function
    def draw(self):

        #setting up map pos
        mapScale = self.mapScale
        c = self.game.playerList[0].x * mapScale, self.game.playerList[0].y * mapScale
        self.mapOffsets = ((c[0] * - 1) + (self.screen.get_width()  / 2) - (self.game.playerList[0].hitBoxSize[0] / 2)), ((c[1] * -1)  + (self.screen.get_height()  / 2)  - (self.game.playerList[0].hitBoxSize[1] / 2))

        #draw map and then tasks and then players on top
        self.drawMapGraphics()
        self.game.taskManager.drawTasks()
        Player.drawPlayers(self.game)

    #loading map graphics
    def loadMapGraphics(self):
        for sprite in self.sprites:
            if sprite["type"] == "image":
                img = pygame.image.load( sprite["source"] ).convert()

                self.spriteAsssets[ sprite["source"] ] = {
                "og": img,
                "active": pygame.transform.scale(img,
                ( int(img.get_width() * self.mapScale) , int(img.get_height() * self.mapScale)))
                }

    #update mapGraphics
    def updateMapGraphics(self):
        for sprite in self.sprites:
            if sprite["type"] == "image":
                img = self.spriteAsssets[ sprite["source"] ]["og"]
                self.spriteAsssets[ sprite["source"] ]["active"] = pygame.transform.scale(img,
                ( int(img.get_width() * self.mapScale) , int(img.get_height() * self.mapScale)))

    #drawing map graphics
    def drawMapGraphics(self):
        mapScale = self.mapScale
        #looping through all the sprites
        for sprite in self.sprites:
            if sprite["type"] == "rect":
                r = pygame.Rect(
                *self.scoords( sprite["x"], sprite["y"] ),
                sprite["width"] * mapScale, sprite["height"] * mapScale )
                pygame.draw.rect( self.screen, sprite["color"], r )
            elif sprite["type"] == "image":
                img = self.spriteAsssets[ sprite["source"]]["active"]
                self.screen.blit(
                img,
                self.scoords( sprite["x"], sprite["y"] ) )

    #converts global to screen coords
    def scoords(self, x, y):
        return ( ( x * self.mapScale) + self.mapOffsets[0], (y * self.mapScale) + self.mapOffsets[1])
