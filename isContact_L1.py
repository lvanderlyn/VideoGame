# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 16:53:22 2014

@author: koenigin
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 14:32:50 2014

@author: koenigin
"""
import pygame, sys, random
from pygame.locals import *

#working meh
#by which i mean not working
# i mean, it does some shit
# just not the shit we want it to do

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()
FPS = 30

# set up the window
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Ladders')

# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


# set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = .1

MAN_WIDTH = 30
MAN_HEIGHT = 60

LADDER_HEIGHT = 110
LADDER_WIDTH = 40

PLATFORM_HEIGHT = 10
PLATFORM_WIDTH = 300

dt = FPS/1.0

class Jumpman(object):
    """
    Basic jumpman object that stores a tuple position and a tuple velocity
    """
    def __init__(self, position, velocity, width, height):
        #position and velocity are tuples of 2 x and y components
        self.position = position
        self.velocity = velocity
        self.width = width
        self.height = height
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def setPosition(self, position):
        self.position = position
    def getPosition(self):
        return self.position
    def getX(self):
        return self.position[0]
    def setX(self, x):
        self.position = (x, self.position[1])
    def getY(self):
        return self.position[1]
    def setY(self, y):
        self.position = (self.position[0],y)
    def setVelocity(self,velocity):
        self.velocity = velocity
    def getVelocity(self):
        return self.velocity
    def updatePosition(self, dt):
        x = self.position[0] + self.velocity[0]*dt
        y = self.position[1] + self.velocity[1]*dt
        self.position = (x,y)
    def jump(self):
        vx = self.velocity[0]
        vy = -100
        self.velocity = (vx,vy)
        

class Platform(Jumpman):
    #The platform class has the below attributes
    def __init__(self, position, width, height, identity):
        self.position = position
        self.velocity = (0,0)
        self.width = width
        self.height = height
        self.identity = identity
    def getIdentity(self):
        return self.identity


#the below code creates a jumpman actor, two platforms and a ladder
player = Jumpman((0,0),(0,0), MAN_WIDTH, MAN_HEIGHT)
pygame.draw.rect(windowSurface, WHITE, (player.getX(), player.getY(), player.getWidth(),player.getHeight()))

ladder = Platform((100,200),LADDER_WIDTH,LADDER_HEIGHT, 'ladder')
pygame.draw.rect(windowSurface, GREEN, (ladder.getX(), ladder.getY(), ladder.getWidth(),ladder.getHeight()))

plat1 = Platform((0,300),PLATFORM_WIDTH,PLATFORM_HEIGHT, 'platform')
pygame.draw.rect(windowSurface, BLUE, (plat1.getX(), plat1.getY(), plat1.getWidth(),plat1.getHeight()))

plat2 = Platform((0,200), PLATFORM_WIDTH, PLATFORM_HEIGHT, 'platform')
pygame.draw.rect(windowSurface, BLUE, (plat2.getX(), plat2.getY(), plat2.getWidth(), plat2.getHeight()))

platforms = [plat1, plat2]
ladders = [ladder]
#MODE_CLIMB = 1
#MODE_WALK = 2
#MODE_FALL = 3
#MODE_CANCLIMB = 4




def modeSelect(actor, platforms, ladders):
    '''Let's think about things logically:
    We have a problem -> ie we want to be able to determine the mode that we
    are based on the things that we are contacting
    Basically, there are several modes that we need to consider:
        1) under a ladder
            - actor would have contact with the ladder at the top, bottom and sides and platform 
            - needs to be able to climb up or walk side to side
        2) above a ladder
            - actor would have contact only at the bottom and with the platform
            - needs to be able to climb down or walk side to side
        3) on a ladder
            - actor would have contact with ladder, but not platform
            - needs to be able to move up and down, but not sideways
        4 on ground
            - actor would have contact with platform and not ladder
            -actor would need to move side to side but not up or down
        5 falling
            -actor is in contact with now objects
            - can move side to side, and fall due to gravity'''
            
    withinLadder = False
    aboveLadder = False
    onPlatform = False
    #not quite working yet (need to figure out why -> figure out problem, loop iteration is not fast enough)
    for walk in platforms:
        #runs through all the background objects and decides the contact conditions
        #based on how the objects are interacting and they type of object
        if actor.getY() + actor.getHeight() >= walk.getY() and actor.getY() + actor.getHeight() < walk.getY() + walk.getHeight():
            if actor.getX() + 0.75 * actor.getWidth() >= walk.getX() and actor.getX() + 0.25*actor.getWidth() <= walk.getX() + walk.getWidth():
                onPlatform = True      
                break
    for up in ladders:
        print actor.getY()
        print actor.getY() + actor.getHeight()        
        print up.getY()
        if (actor.getX() + 0.25 * actor.getWidth() >= up.getX()) and (actor.getX() + 0.75*actor.getWidth() <= up.getX() + up.getWidth()):
            if actor.getY() + actor.getHeight() <= up.getY() + up.getHeight() and actor.getY()+ actor.getHeight() >= up.getY() and not actor.getY() < up.getY():
                withinLadder = True
            elif actor.getY() + actor.getHeight() >= up.getY() and actor.getY() < up.getY():
                aboveLadder = True
                break

    #Assign Modes here based on the above conditions
    if onPlatform and withinLadder and not aboveLadder:
        return 1
    elif aboveLadder and onPlatform:
        return 2
    elif withinLadder or aboveLadder and not onPlatform:
        #
        return 3
    elif onPlatform and not withinLadder and not aboveLadder:
        return 4
    else:
        return 5
    
    
        
def gravity(jumpman, dt):
    """
    updates the velocity of the jumpman after time dt has passed
    """
    acceleration = .005
    speed = jumpman.getVelocity()[1] #jumpman velocity should be a tuple with x-comp and y-comp
    yPos = jumpman.getPosition()[1] #position should be tuple of x-coor and y-coor of top right corner
    
    dy = speed*dt + 0.5*acceleration*dt**2
    
    jumpman.setVelocity((jumpman.getVelocity()[0], speed+(acceleration*dt)))


while True:
    mode = modeSelect(player, platforms, ladders)    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:                   #denotes that one or more keys are pushed down
        # change the keyboard variables
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == ord('w'):
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == ord('s'):
                moveUp = False
                moveDown = True
        if event.type == KEYUP:                     #denotes that no keys are pushed down (ie and reset)
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == K_UP or event.key == ord('w'):
                moveUp = False
            if event.key == K_DOWN or event.key == ord('s'):
                moveDown = False
        
            
    print mode
      
    # draw the black background onto the surface
    windowSurface.fill(BLACK)
    # move the player
    player.setVelocity((0,0))
    if mode == 1:
        if moveUp and player.getY() > 0:
            player.setVelocity((0,-1*MOVESPEED))
        if moveLeft and player.getX() > 0:
            player.setVelocity((-1*MOVESPEED,0))
        if moveRight and player.getX()+player.getWidth() < WINDOWWIDTH:
            player.setVelocity((MOVESPEED,0))
    if mode == 2:
        if moveDown and player.getY()+player.getHeight() < WINDOWWIDTH:
            player.setVelocity((0, MOVESPEED))
        if moveLeft and player.getX() > 0:
            player.setVelocity((-1*MOVESPEED,0))
        if moveRight and player.getX()+player.getWidth() < WINDOWWIDTH:
            player.setVelocity((MOVESPEED,0))
    if mode == 3:
        if moveDown and player.getY()+player.getHeight() < WINDOWHEIGHT:
            player.setVelocity((0,MOVESPEED))
        if moveUp and player.getY() > 0:
            player.setVelocity((0,-1*MOVESPEED))
    if mode == 4:
        if moveLeft and player.getX() > 0:
            player.setVelocity((-1*MOVESPEED,0))
        if moveRight and player.getX()+player.getWidth() < WINDOWWIDTH:
            player.setVelocity((MOVESPEED,0))        
    if mode == 5:
        if moveLeft and player.getX() > 0:
            player.setVelocity((-1*MOVESPEED,0))
        if moveRight and player.getX()+player.getWidth() < WINDOWWIDTH:
            player.setVelocity((MOVESPEED,0))        
        gravity(player,dt)

    # draw the player onto the surface
    pygame.draw.rect(windowSurface, GREEN, (ladder.getX(), ladder.getY(), ladder.getWidth(),ladder.getHeight()))
    pygame.draw.rect(windowSurface, BLUE, (plat1.getX(), plat1.getY(), plat1.getWidth(),plat1.getHeight()))
    pygame.draw.rect(windowSurface, BLUE, (plat2.getX(), plat2.getY(), plat1.getWidth(),plat2.getHeight()))    
    player.updatePosition(dt)
    pygame.draw.rect(windowSurface, WHITE, (player.getX(), player.getY(), MAN_WIDTH,MAN_HEIGHT))
    
    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(FPS)
pygame.quit()