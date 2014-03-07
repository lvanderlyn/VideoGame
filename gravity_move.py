# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 18:34:55 2014

@author: koenigin
"""

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
    def __init__(self, position, width, height):
        #position and velocity are tuples of 2 x and y components
        self.position = position
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
    def updatePosition(self, dt):
        self.position = (x,y)
    def jump(self):
        self.position = (self.position[0],self.position[1]+0.5*50)
                         
def gravity(jumpman):
    """
    updates the velocity of the jumpman after time dt has passed
    """
    acceleration = 50
    
    jumpman.setY(jumpman.getY()+0.5*acceleration)


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

MOVESPEED = 10

man = Jumpman((0.0,0.0), MAN_WIDTH, MAN_HEIGHT)
pygame.draw.rect(DISPLAYSURF, WHITE, (man.getX(), man.getY(), man.getWidth(),man.getHeight()))

mode = 0

    
moveY = 0
moveX = 0
isGravity = True
jump = False
moveUp = False
moveDown = False
moveLeft = False
moveRight = False


while True: # the main game loop
    DISPLAYSURF.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
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
            if event.key == K_SPACE:
                jump = True
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
        

                
    dt = 1.0/FPS
    


    if(man.getPosition()[1] < (WINDOWHEIGHT-MAN_HEIGHT)):
        isGravity = True
    else:
        man.setPosition((man.getPosition()[0],(WINDOWHEIGHT-MAN_HEIGHT)))
        isGravity = False
    if jump:   
        man.jump()
        jump = False
    
    if moveLeft:
        man.setX(man.getX()+ -1*MOVESPEED)
    if moveRight:
        man.setX(man.getX()+ 1*MOVESPEED)
    if moveUp:
        man.setY(man.getY()+ -1*MOVESPEED)
    if moveDown:
        man.setX(man.getY()+ 1*MOVESPEED)
        
    gravity(man)
    
    
    #draws a new jumpman rectangel
    pygame.draw.rect(DISPLAYSURF, WHITE, (man.getX(), man.getY(), MAN_WIDTH, MAN_HEIGHT))
    pygame.display.update()
    fpsClock.tick(FPS)
