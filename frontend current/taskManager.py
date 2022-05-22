import pygame

#loading tasks
from fixWiresTask import FixWiring
from primeShieldsTask import PrimeShields

#controls task activation and deactivation
class TaskManager:

    #static varaibles
    activationDis = 10
    font = None
    fontSize = 12

    #constructor
    def __init__(self, g):
        self.game = g
        self.tasks = []
        self.inRangeTask = None
        self.inRangeSurface = None
        self.taskActive = False

        #finding all tasks on map
        for s in g.map.sprites:
            if s["type"] == "task":
                self.tasks.append(s)
                s["done"] = False

        self.loadIcons()
        TaskManager.loadTaskObjs( g )

        #setting up font
        pygame.font.init()
        TaskManager.font = pygame.font.SysFont("octin stencil", int(TaskManager.fontSize  * self.game.map.mapScale))

    #loads task media
    taskIconSize = [10,10]
    def loadIcons(self):
        for t in self.tasks:
            img = pygame.image.load( t["icon"] ).convert()
            t["img"] = { "og": img }
        self.updateIcons()

    #updates task media
    def updateIcons(self):
        for t in self.tasks:
            img = t["img"]["og"]
            t["img"]["active"] = pygame.transform.scale(img,
            ( int(TaskManager.taskIconSize[0]  * self.game.map.mapScale) , int(TaskManager.taskIconSize[1]  * self.game.map.mapScale)))
        TaskManager.font = pygame.font.SysFont("octin stencil", int(TaskManager.fontSize  * self.game.map.mapScale))

        #update the tasks
        if self.taskActive:
            for t in self.taskObjs:
                if t.active:
                    t.updateGraphics()

    #draws all the tasks onto map
    def drawTasks(self):
        self.findInRangeTask()
        for t in self.tasks:
            r = pygame.Rect( *self.game.map.scoords( t["x"], t["y"]), 10 * self.game.map.mapScale, 10 * self.game.map.mapScale)
            self.game.screen.blit(t["img"]["active"],self.game.map.scoords( t["x"], t["y"] ) )
            if t["name"] == self.inRangeTask:
                pygame.draw.rect( self.game.screen, (0,255,0), r, 5)

        #draw text if a task is in range and not active and not done and not impostor (sus)
        if self.inRangeTask != None and not self.taskActive:
            pygame.draw.rect(self.game.screen, (200,255,200), pygame.Rect( 0, self.game.screen.get_height() - self.inRangeSurface.get_height(), self.game.screen.get_width(), self.inRangeSurface.get_height() ) )
            self.game.screen.blit( self.inRangeSurface, ( (self.game.screen.get_width() / 2) - (self.inRangeSurface.get_width() / 2) , self.game.screen.get_height() - self.inRangeSurface.get_height()))

    #determine which task (if any) is viable to be within activation distance
    def findInRangeTask(self):
        hb = self.game.playerList[0].getHitBox()
        self.inRangeTask = None
        for t in self.tasks:
            r = pygame.Rect( t["x"], t["y"], 10, 10)

            #if impostor not tasks will ever be in range
            if r.colliderect( hb ) and not t["done"] and not self.game.playerList[0].isImpostor:
                self.inRangeTask = t["name"]
                self.inRangeSurface = TaskManager.font.render( "press space to start " + t["name"] + " task", True, (0,0,0))

    #updates tasks
    def updateTasks(self):

        #seeing if space was pressed
        for event in self.game.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.inRangeTask != None:
                for tObj in self.taskObjs:
                    if self.inRangeTask == tObj.name and not self.taskActive:
                        tObj.start()
                        self.taskActive = True

        #updating tasks
        if self.taskActive:
            for tObj in self.taskObjs:
                if tObj.active:
                    tObj.update()
                    if not tObj.active:

                        #task ended itself
                        self.taskActive = False
                        if tObj.taskDone:
                            for t in self.tasks:
                                if t["name"] == self.inRangeTask:
                                    t["done"] = True

    taskObjs = []
    #loads tasks
    def loadTaskObjs( game ):
        TaskManager.taskObjs.append( FixWiring( game ) )
        TaskManager.taskObjs.append( PrimeShields( game ) )
