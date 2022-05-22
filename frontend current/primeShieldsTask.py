import pygame
import random

#173, 43

class PrimeShields:

    #constructor
    def __init__(self, g):
        self.game = g
        self.active = False
        self.name = "shields"
        self.surface = None
        self.surfLoc = [0,0]
        self.taskDone = False
        self.hitBox = None
        self.bgImg = pygame.image.load("tasks/shields2.png").convert()
        self.currImg = None
        self.hexCoords = [(167,38),(67,98),(267,101),(166,161),(68,221),(168,280),(268,222)]
        self.redCoords = [None] * 6
        self.surfScale = None

    #starts up task
    def start(self):

        #startup
        self.active = True
        self.updateGraphics()

        for i in range(6):
            self.redCoords[i] = list(random.choice(self.hexCoords))

    #updates surface size and location
    def updateGraphics(self):

        #creating surface
        screenProp = 0.75
        if self.game.screen.get_width() < self.game.screen.get_height():
            surfSize = int( self.game.screen.get_width() * screenProp )
        else:
            surfSize = int( self.game.screen.get_height() * screenProp )
        self.surfLoc[0] = int( ((1 - (surfSize / self.game.screen.get_width())) / 2) * self.game.screen.get_width() )
        self.surfLoc[1] = int( ((1 - (surfSize / self.game.screen.get_height())) / 2) * self.game.screen.get_height() )
        self.surface = pygame.Surface( (surfSize, surfSize) )
        self.surface.fill( (50,50,50) )
        self.hitBox = pygame.Rect( self.surfLoc, (surfSize, surfSize) )
        self.currImg = pygame.transform.scale(self.bgImg, (surfSize, surfSize))
        self.surfScale = surfSize / 400

    #updates task when active
    def update(self):

        self.surface.blit( self.currImg, (0,0) )
        #drawing rectangles
        for coord in self.redCoords:
            if coord != None:
                r = pygame.Rect( (coord[0] * self.surfScale, coord[1] * self.surfScale) , (self.surfScale * 60, self.surfScale * 60) )
                pygame.draw.rect(self.surface, (255,0,0), r)

        #drawing surface
        self.game.screen.blit(self.surface, self.surfLoc)

        #looping through events
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.hitBox.collidepoint( event.pos ):
                    self.active = False
                    self.taskDone = False
                    return
                else:
                    done = True
                    for i in range(6):
                        coord = self.redCoords[i]
                        if coord != None:
                            r = pygame.Rect( (coord[0] * self.surfScale, coord[1] * self.surfScale) , (self.surfScale * 60, self.surfScale * 60) )
                            if r.collidepoint((event.pos[0] - self.surfLoc[0], event.pos[1] - self.surfLoc[1])):
                                self.redCoords[i] = None
                            else:
                                done = False
                    if done:
                        self.active = False
                        self.taskDone = True
                        return
