#hello world

#imports
import pygame
from game import Game
import time
from pygame.locals import *

#initilizing pygame stuff
pygame.init()
screen = pygame.display.set_mode( (1010,610), RESIZABLE )

#timing
fps = 100
waitTime = 1 / fps

#creating new game object
gameObj = Game(screen)
gameObj.fps = fps
gameObj.update()
pygame.display.flip()

#main loop
while not gameObj.gameOver:
    currTime = time.time()
    gameObj.update()
    pygame.display.flip()
    if( waitTime - ( time.time() - currTime ) > 0):
        time.sleep(waitTime - ( time.time() - currTime ) )

#end of loop
pygame.quit()
