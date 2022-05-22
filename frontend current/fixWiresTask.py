import pygame
import random

class FixWiring:

    #constructor
    def __init__(self, g):
        self.game = g
        self.active = False
        self.name = "fixWiring"
        self.surface = None
        self.surfLoc = [0,0]
        self.taskDone = False
        self.hitBox = None
        self.leftC = ( (0,0,255),(255,0,0),(255,255,0),(255,0,255) )
        self.rightC = []
        self.wireStatus = ["free"] * 4
        self.wireDown = False
        self.wireSrc = None
        self.wiresDone = 0
        self.bgImg = pygame.image.load("tasks/eletrical2.png").convert()
        self.currImg = None

    #starts up task
    def start(self):

        #startup
        self.active = True
        self.updateGraphics()
        self.wireStatus = ["free"] * 4
        self.wireDown = False
        self.wiresDone = 0

        #random order of right column
        self.rightC = []
        for i in range(4):
            rc = random.choice(self.leftC)
            while rc in self.rightC:
                rc = random.choice(self.leftC)
            self.rightC.append(rc)

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

    #updates task when active
    def update(self):

        self.surface.blit( self.currImg, (0,0) )
        relMousePos = list(pygame.mouse.get_pos())
        relMousePos[0] -= self.surfLoc[0]
        relMousePos[1] -= self.surfLoc[1]

        #drawing circles
        s = self.surface.get_width()
        radius = int( 3 * (s / 100) )
        for row in range( 1, 5 ):
            pygame.draw.circle(self.surface, self.leftC[row - 1], (int(s * 0.1), int(s * row * (1/5))), radius)
            pygame.draw.circle(self.surface, self.rightC[row - 1], (int(s * 0.9), int(s * row * (1/5))), radius)

        #drawing placed wires
        for rowL in range(4):
            if self.wireStatus[rowL] == "done":
                for rowR in range(4):
                    if self.leftC[rowL] == self.rightC[rowR]:
                        pygame.draw.line( self.surface, self.leftC[rowL],
                        (int(s * 0.1), int(s * (rowL + 1) * (1/5))),
                        (int(s * 0.9), int(s * (rowR + 1) * (1/5))),
                        radius )

        #active wire
        if self.wireDown:
            pygame.draw.line( self.surface, self.leftC[self.wireSrc], (int(s * 0.1), int(s * (self.wireSrc + 1) * (1/5))), relMousePos, radius )

        #drawing surface
        self.game.screen.blit(self.surface, self.surfLoc)

        #looping through events
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hitBox.collidepoint( event.pos ):

                    #looping through all circles to see if one was clicked
                    wasDown = self.wireDown
                    self.wireDown = False
                    for row in range(4):
                        for col in range(2):
                            if self.findHitBox(row, col).collidepoint(event.pos):
                                if col == 0 and self.wireStatus[row] == "free":
                                    self.wireDown = True
                                    self.wireSrc = row
                                elif wasDown:
                                    if self.leftC[self.wireSrc] == self.rightC[row]:
                                        self.wireStatus[self.wireSrc] = "done"
                                        self.wiresDone += 1
                                        if self.wiresDone == 4:
                                            self.taskDone = True
                                            self.active = False
                                            return

                else:
                    self.active = False
                    return

    #function returns hit box of circle in row and column
    def findHitBox(self, row, col):
        row += 1
        s = self.surface.get_width()
        radius = int( 3 * (s / 100) )
        if col == 0:
            x = int(s * 0.1)
        else:
            x = int(s * 0.9)
        return pygame.Rect( (x + self.surfLoc[0] - radius, int(s * row * (1/5)) + self.surfLoc[1] - radius), (radius * 2, radius * 2))
