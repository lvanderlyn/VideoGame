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
    def __init__(self, position, velocity):
        #position and velocity are tuples of 2 x and y components
        self.position = position
        self.velocity = velocity
    def setPosition(self, position):
        self.position = position
    def getPosition(self):
        return self.position
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

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
WINDOWHEIGHT = 600
WINDOWWIDTH = 600
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Gravity')

WHITE = (255, 255, 255)
BLACK = (0,0,0)

n = 100.0

man = Jumpman((0.0,100.0),(40.0,0.0))
pygame.draw.rect(DISPLAYSURF, WHITE, (man.getPosition()[0], man.getPosition()[1], n,n))

count=0
man.jump()

while True: # the main game loop
    DISPLAYSURF.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    dt = 1.0/FPS
    
    #accounts for collision with botton of window
    if(man.getPosition()[1] < (WINDOWHEIGHT-n)):
        gravity(man,dt)
    else:
        man.setPosition((man.getPosition()[0],(WINDOWHEIGHT-n)))
        man.setVelocity((0.0,0.0))

    man.updatePosition(dt)

    
    
    #draws a new jumpman rectangel
    pygame.draw.rect(DISPLAYSURF, WHITE, (man.getPosition()[0],man.getPosition()[1], n,n))

    pygame.display.update()
    fpsClock.tick(FPS)



        