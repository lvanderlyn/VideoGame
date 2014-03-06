# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 18:28:41 2014

@author: anneubuntu
"""

    
import pygame, sys
from pygame.locals import *

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
        vy = -10
        self.velocity = (vx,vy)
        
def gravity(jumpman, dt):
    """
    updates the velocity of the jumpman after time dt has passed
    """
    acceleration = 50
    speed = jumpman.getVelocity()[1] #jumpman velocity should be a tuple with x-comp and y-comp
    yPos = jumpman.getPosition()[1] #position should be tuple of x-coor and y-coor of top right corner
    
    dy = speed*dt + 0.5*acceleration*dt**2
    
    jumpman.setVelocity((jumpman.getVelocity()[0], speed+(acceleration*dt)))


pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
WINDOWHEIGHT = 600
WINDOWWIDTH = 600
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Gravity')

#colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)

#modes
MODE_FALL = 1
MODE_WALK = 2
MODE_CLIMB = 3
MODE_CANCLIMB = 4

MAN_HEIGHT = 100.0
MAN_WIDTH = 50.0

MOVESPEED = 5

man = Jumpman((0.0,100.0),(40.0,0.0), MAN_WIDTH, MAN_HEIGHT)
pygame.draw.rect(DISPLAYSURF, WHITE, (man.getPosition()[0], man.getPosition()[1], man.getWidth(),man.getHeight()))

mode = 0

    
moveY = 0
moveX = 0
jump = False
isGravity = True

while True: # the main game loop
    DISPLAYSURF.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:                   #denotes that one or more keys are pushed down
            if event.key == K_LEFT or event.key == ord('a'):
                moveX = -1*MOVESPEED
            if event.key == K_RIGHT or event.key == ord('d'):
                moveX = 1*MOVESPEED
            if event.key == K_UP or event.key == ord('w'):
                moveY = -1*MOVESPEED
            if event.key == K_DOWN or event.key == ord('s'):
                moveY = MOVESPEED
            if event.key == K_SPACE:
                man.jump()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                moveX = 0
            if event.key == K_RIGHT or event.key == ord('d'):
                moveX = 0
            if event.key == K_UP or event.key == ord('w'):
                moveY = 0
            if event.key == K_DOWN or event.key == ord('s'):
                moveY = 0
            if event.key == K_SPACE:
                jump = False
                
        

                
    dt = 0.1
    
    print mode
    
    
    if mode == MODE_FALL:
        man.setY(man.getY() + moveY)
        isGravity = True
    if mode == MODE_WALK:
        isGravity=False
        man.setX(man.getX() + moveX)
    if jump:
        mode == MODE_FALL
        isGravity = True
        man.jump()

    if isGravity:
        gravity(man, dt)
    
    if(man.getY() < (WINDOWHEIGHT-MAN_HEIGHT)):
        mode = MODE_FALL
    else:
        man.setPosition((man.getX(),(WINDOWHEIGHT-MAN_HEIGHT)))
        man.setVelocity((0.0,0.0))
        mode = MODE_WALK
    
    man.updatePosition(dt)


    
    
    #draws a new jumpman rectangel
    pygame.draw.rect(DISPLAYSURF, WHITE, (man.getX(), man.getY(), MAN_WIDTH, MAN_HEIGHT))
    pygame.display.update()
    fpsClock.tick(FPS)



        