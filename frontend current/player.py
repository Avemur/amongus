#import pygame
import pygame
from collision import colliding

#player class
class Player:

    font = None
    fontSize = 6
    #evryplayer has same sprite and hitBox
    playerSprites = {}
    colors = ["Blue","Red","Green"]
    hitBox = (8,12)
    playersInRange = []
    def loadPlayerGraphics(game):

        #loadidng player images
        for color in Player.colors:
            img = pygame.image.load("char" + color + ".png").convert()
            deadImg = pygame.image.load("char" + color + "Dead.png").convert()
            img.set_colorkey((255,255,255))
            deadImg.set_colorkey((255,255,255))
            Player.playerSprites[color] = {
            "og": img,
            "left": pygame.transform.flip( img, True, False ),
            "right": img,
            "deadOg": deadImg,
            "deadCurr": deadImg
            }

        #setting up font
        pygame.font.init()
        Player.font = pygame.font.SysFont("octin stencil", int(Player.fontSize  * game.map.mapScale))

    def updatePlayerGrpahics(game):
        for color in Player.colors:
            img = Player.playerSprites[color]["og"]
            deadImg = Player.playerSprites[color]["deadOg"]
            Player.playerSprites[color]["right"] = pygame.transform.scale(img, (int(Player.hitBox[0] * game.map.mapScale),int(Player.hitBox[1] * game.map.mapScale)))
            Player.playerSprites[color]["left"] = pygame.transform.flip( Player.playerSprites[color]["right"], True, False )
            Player.playerSprites[color]["deadCurr"] = pygame.transform.scale(deadImg, (int(Player.hitBox[0] * game.map.mapScale),int(Player.hitBox[1] * game.map.mapScale)))
        Player.font = pygame.font.SysFont("octin stencil", int( Player.fontSize * game.map.mapScale) )
        for p in game.playerList:
            if not p.isImpostor:
                p.nameSurface = Player.font.render(p.name, True, (0,0,0))
                p.tagSize = Player.font.size( p.name )
            else:
                p.nameSurface = Player.font.render(p.name + "<sus>", True, (0,0,0))
                p.tagSize = Player.font.size( p.name + "<sus>" )

    #staic method draws the players
    def drawPlayers(game):

        #drawing all the players
        for p in game.playerList:
            #drawing image
            if not p.dead:
                if p.name in Player.playersInRange and game.playerList[0].isImpostor:
                    w = Player.playerSprites[p.color]["right"].get_width()
                    h = Player.playerSprites[p.color]["right"].get_height()
                    pygame.draw.rect(game.screen, (255,255,0), pygame.Rect( game.map.scoords(p.x,p.y), (w,h) ))
                if p.direction == "right":
                    game.screen.blit(Player.playerSprites[p.color]["right"], game.map.scoords( p.x,p.y ))
                else:
                    game.screen.blit(Player.playerSprites[p.color]["left"], game.map.scoords( p.x,p.y ))
            else:
                game.screen.blit(Player.playerSprites[p.color]["deadCurr"], game.map.scoords( p.x,p.y ))

            #drawing text
            coords = list(game.map.scoords(p.x, p.y))
            coords[0] = (coords[0] + ((Player.hitBox[0] * game.map.mapScale) / 2)) - (p.tagSize[0] / 2)
            game.screen.blit( p.nameSurface, (coords[0],coords[1] - p.tagSize[1]) )

    moveDir = [0,0]
    leftDown = False
    rightDown = False
    upDown = False
    downDown = False
    #static method controls the player movment
    def updatePlayerPos(game):
        moveDir = Player.moveDir
        mainPlayer = game.playerList[0]
        truePlayerSpeed = 100
        playerSpeed = truePlayerSpeed / game.fps

        for event in game.events:
            
            if event.type == pygame.KEYDOWN:

                #setting move direction
                if event.key == pygame.K_RIGHT:
                    Player.rightDown = True
                    moveDir[0] = 1
                    mainPlayer.direction = "right"
                elif event.key == pygame.K_LEFT:
                    Player.leftDown = True
                    moveDir[0] = -1
                    mainPlayer.direction = "left"
                elif event.key == pygame.K_UP:
                    Player.upDown = True
                    moveDir[1] = -1
                elif event.key == pygame.K_DOWN:
                    Player.downDown = True
                    moveDir[1] = 1

            elif event.type == pygame.KEYUP:

                #unsetting move direction
                if event.key == pygame.K_RIGHT:
                    Player.rightDown = False
                    if moveDir[0] == 1:
                        if Player.leftDown:
                            mainPlayer.direction = "left"
                            moveDir[0] *= -1
                        else:
                            moveDir[0] = 0

                elif event.key == pygame.K_LEFT:
                    Player.leftDown = False
                    if moveDir[0] == -1:
                        if Player.rightDown:
                            mainPlayer.direction = "right"
                            moveDir[0] *= -1
                        else:
                            moveDir[0] = 0

                if event.key == pygame.K_UP:
                    Player.upDown = False
                    if moveDir[1] == -1:
                        if Player.downDown:
                            moveDir[1] *= -1
                        else:
                            moveDir[1] = 0

                elif event.key == pygame.K_DOWN:
                    Player.downDown = False
                    if moveDir[1] == 1:
                        if Player.upDown:
                            moveDir[1] *= -1
                        else:
                            moveDir[1] = 0

        #moving player
        oldX = mainPlayer.x
        oldY = mainPlayer.y
        mainPlayer.x += moveDir[0] * playerSpeed
        if colliding(game, mainPlayer):
            mainPlayer.x = oldX
        mainPlayer.y += moveDir[1] * playerSpeed
        if colliding(game, mainPlayer):
            mainPlayer.y = oldY
        #walk_sound = pygame.mixer.Sound("walking.wav")
        #pygame.mixer.Sound.play(walk_sound)            
        #if outside map, move as close to wall as possible
        if mainPlayer.x < 0:
            mainPlayer.x = 0
        elif mainPlayer.x + mainPlayer.hitBoxSize[0] > 1000:
            mainPlayer.x = 1000 - mainPlayer.hitBoxSize[0]

        if mainPlayer.y < 0:
            mainPlayer.y = 0
        elif mainPlayer.y + mainPlayer.hitBoxSize[1] > 600:
            mainPlayer.y = 600 - mainPlayer.hitBoxSize[1]

        #updating position on server
        if oldX != mainPlayer.x or oldY != mainPlayer.y:
            game.multi.updateServer()

        #do killing stuff
        if mainPlayer.isImpostor:
            Player.killTest(game)

    #handels killing crewmates
    def killTest(game):

        #finding crewmates in
        Player.playersInRange = []
        for p in game.playerList:
            if game.playerList[0].getHitBox().colliderect(p.getHitBox()):
                if p.name != game.playerList[0].name:
                    Player.playersInRange.append(p.name)

        #kill
        for event in game.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for p in game.playerList:
                        if p.name in Player.playersInRange:
                            p.dead = True
                            kill_sound = pygame.mixer.Sound("kill_sound.wav")
                            pygame.mixer.Sound.play(kill_sound)
    #constructor
    def __init__(self, game, x, y, c, n = "unnamed" ):
        self.game = game
        self.x = x
        self.y = y
        self.color = c
        self.screen = game.screen
        self.hitBoxSize = Player.hitBox
        self.direction = "right"
        self.name = n
        self.nameSurface = Player.font.render(self.name, True, (0,0,0))
        self.tagSize = Player.font.size( self.name )
        self.dead = False
        self.isImpostor = False

    #returns hitbox
    def getHitBox(self):
        return pygame.Rect( self.x, self.y, self.hitBoxSize[0], self.hitBoxSize[1] )
    