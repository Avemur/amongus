import pygame

class DivertPower:

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
