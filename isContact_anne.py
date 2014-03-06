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

LADDER_HEIGHT = 100
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
    def __init__(self, position, width, height):
        self.position = position
        self.velocity = (0,0)
        self.width = width
        self.height = height



player = Jumpman((0,0),(0,0), MAN_WIDTH, MAN_HEIGHT)
pygame.draw.rect(windowSurface, WHITE, (player.getX(), player.getY(), player.getWidth(),player.getHeight()))

ladder = Platform((200,200),LADDER_WIDTH,LADDER_HEIGHT)
pygame.draw.rect(windowSurface, GREEN, (ladder.getX(), ladder.getY(), ladder.getWidth(),ladder.getHeight()))

plat = Platform((0,300),PLATFORM_WIDTH,PLATFORM_HEIGHT)
pygame.draw.rect(windowSurface, BLUE, (plat.getX(), plat.getY(), plat.getWidth(),plat.getHeight()))


MODE_CLIMB = 1
MODE_WALK = 2
MODE_FALL = 3
MODE_CANCLIMB = 4


    


def isContact(actor, other):
    '''takes in the jumpman actor and an object and determines if there is contact between the two'''
    actor_rect = pygame.Rect(actor.getX(),actor.getY(),actor.getWidth()+1,actor.getHeight()+1)
    other_rect = pygame.Rect(actor.getX(),actor.getY(),other.getWidth()+1,other.getHeight()+1)
    contact = other_rect.colliderect(actor_rect)
    if contact:
        print "True"
    else:
        print "False"
    return contact


def modeSelect(actor, climb, walk):
    '''take in a list of climable object called 'climb', and list of platforms
    called 'walk' and determines the mode (controls allowed) based on what
    the jumperman is in contact with'''
    mode = 0
    Climb = False
    Walk = False
    for up in climb:
        if isContact(actor, up):
            Climb = True
            break
    for platform in walk:
        if isContact(actor, platform):
            Walk = True
            break
    if Walk and Climb:
        return MODE_CANCLIMB
    elif Walk and (not Climb):
        return MODE_WALK
    elif Climb and (not Walk):
        return MODE_CLIMB
    else:
        return MODE_FALL
        
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

    for event in pygame.event.get():
        mode = modeSelect(player, [ladder], [plat])
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if mode == MODE_CANCLIMB:
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
            if event.type == KEYUP:                     #denotes that no keys are pushed down
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
        elif mode == MODE_CLIMB:
            if event.type == KEYDOWN:                   #denotes that one or more keys are pushed down
            # change the keyboard variables
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:                     #denotes that no keys are pushed down
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
        elif mode == MODE_WALK:
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
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = False
            if event.type == KEYUP:                     #denotes that no keys are pushed down
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
        elif mode == MODE_FALL:
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
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = False
             if event.type == KEYUP:
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
        else:
            moveRight = False
            moveLeft = False
            moveUp = False
            moveDown = False   
            
    print mode
      
    # draw the black background onto the surface
    windowSurface.fill(BLACK)
    # move the player
    player.setVelocity((0,0))
    if moveDown and player.getY()+player.getHeight() < WINDOWHEIGHT:
        player.setVelocity((0,MOVESPEED))
    if moveUp and player.getY() > 0:
        player.setVelocity((0,-1*MOVESPEED))
    if moveLeft and player.getX() > 0:
        player.setVelocity((-1*MOVESPEED,0))
    if moveRight and player.getX()+player.getWidth() < WINDOWWIDTH:
        player.setVelocity((MOVESPEED,0))


    # draw the player onto the surface
    gravity(player,dt)
    player.updatePosition(dt)
    pygame.draw.rect(windowSurface, WHITE, (player.getX(), player.getY(), MAN_WIDTH,MAN_HEIGHT))
    pygame.draw.rect(windowSurface, GREEN, (ladder.getX(), ladder.getY(), ladder.getWidth(),ladder.getHeight()))
    pygame.draw.rect(windowSurface, BLUE, (plat.getX(), plat.getY(), plat.getWidth(),plat.getHeight()))

    
    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(FPS)
pygame.quit()

        
            
            
        
        