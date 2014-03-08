# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 16:12:53 2014

@author: anneubuntu, ddiggins
"""

"""
Scaffolding -
Implementing the model-view-controller structure
Leaving some functions undefined - we can work on them later once we know what they
need to contain
THIS IS GOOD AND IMPORTANT
"""
import pygame
import math
from pygame.locals import *
import random
import time


MODE_UNDERLADDER = 1
MODE_ABOVELADDER = 2
MODE_ONLADDER = 3
MODE_ONPLATFORM = 4
MODE_FALLING = 5

WINDOWWIDTH = 400
WINDOWHEIGHT = 400


# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

J_HEIGHT = 40
J_WIDTH = 20
PLATFORM_HEIGHT = 10
LADDER_WIDTH = 30

class Model:
    def __init__(self):
        self.jumpman = Jumpman(0.0,0.0,J_WIDTH,J_HEIGHT) #need jumpman class
        self.platforms = []
        self.genPlatforms()
        self.ladders = []
        self.genLadders()
        self.mode = self.modeFinder()
    
    def update(self):
        self.jumpman.update()
        
    def modeFinder(self):
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
        for walk in self.platforms:
            #runs through all the background objects and decides the contact conditions
            #based on how the objects are interacting and they type of object
            if self.jumpman.y + self.jumpman.height >= walk.y and self.jumpman.y + self.jumpman.height < walk.y + walk.height:
                if self.jumpman.x + 0.75 * self.jumpman.width >= walk.x and self.jumpman.x + 0.25*self.jumpman.width <= walk.x + walk.width:
                    onPlatform = True      
                    break
        for up in self.ladders:
            if self.jumpman.x + 0.25 * self.jumpman.width >= up.x and self.jumpman.x + 0.75*self.jumpman.width <= up.x + up.width:
                if self.jumpman.y + self.jumpman.height <= up.y + up.height and self.jumpman.y+ self.jumpman.height >= up.y and not self.jumpman.y < up.y:
                    withinLadder = True
                elif self.jumpman.y + self.jumpman.height >= up.y and self.jumpman.y < up.y:
                    aboveLadder = True
                break

        #Assign Modes here based on the above conditions
        if onPlatform and withinLadder and not aboveLadder:
            return MODE_UNDERLADDER
        elif aboveLadder and onPlatform:
            return MODE_ABOVELADDER
        elif withinLadder or aboveLadder and not onPlatform:
            #
            return MODE_ONLADDER
        elif onPlatform and not withinLadder and not aboveLadder:
            return MODE_ONPLATFORM
        else:
            return MODE_FALLING
    
    def inContact(self, jumpman, pladder):#Not done yet either
        #determines if jumpman is in contact with a given platform or ladder
        pass
    
    def genPlatforms(self):
        #Generates platforms depending of windowheight/width    
        numLayers  = int(math.ceil(WINDOWHEIGHT/(2.0*J_HEIGHT))) #Number of layers of platforms allowed
        for layer in range(numLayers):
            y = (WINDOWHEIGHT/numLayers)*layer
            x = 0
            width = WINDOWWIDTH #change this to make variable widths
            plat = Platform(x,y,width)
            self.platforms.append(plat)
            
    
    def genLadders(self): #Not Dones
        #Generates ladders depending on the location of the platforms
        numLayers = math.ceil(WINDOWHEIGHT/(2.0*J_HEIGHT))
        h = WINDOWHEIGHT/numLayers
        height = 0
        x_pos = 0
        y_coor = 0
        for fromPlatform in self.platforms:
            r = random.randint(0,2)
            if r==0 or r==1: #2/3 chance of having a ladder going down
                possiblePlatforms = []
                for toPlatform in self.platforms:
                    for i in range(random.randint(0,4)):
                        x_pos = random.randint(fromPlatform.x, (fromPlatform.x + fromPlatform.width-LADDER_WIDTH)) #choose random x position on platform
                        if x_pos in range(toPlatform.x, toPlatform.x + toPlatform.width - LADDER_WIDTH): 
                            possiblePlatforms.append(toPlatform)
                for possPlat in possiblePlatforms:
                    if (possPlat.y > fromPlatform.y + (2*h)):
                        possiblePlatforms.remove(possPlat)
                if len(possiblePlatforms) != 0:
                    p = random.randint(0,len(possiblePlatforms))
                    ladder = Ladder(x_pos, fromPlatform.y, toPlatform.y - fromPlatform.y)
                    self.ladders.append(ladder)
            
        

class Jumpman: #Defines Jumpman the one and only
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.vx = 0.0
        self.vy = 0.0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
    
    def jump(self):
        self.vy -= 5 #fiddle with actual number, was selected arbitrarily. it felt GOOD
    
    def gravity(self):
        self.vy += 3 #selected randomly, can change
        
class Platform: #Defines platform class
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = PLATFORM_HEIGHT #Height 10px
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
class Ladder: #Defines ladder class
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.width = LADDER_WIDTH #Width 30px
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
class View:
    def __init__(self, model, screen): #View contains model and screen
        self.model = model
        self.screen = screen
        
    def draw(self):
        self.screen.fill(BLACK) #Makes screen bg black
        for platform in self.model.platforms:
            pygame.draw.rect(self.screen, GREEN, (platform.x, platform.y, platform.width, platform.height)) #Draws all of the platforms
        for ladder in self.model.ladders:
            pygame.draw.rect(self.screen, BLUE, (ladder.x, ladder.y, ladder.width, ladder.height)) #Draws all of the ladders
        pygame.draw.rect(self.screen, WHITE, (self.model.jumpman.x, self.model.jumpman.y, self.model.jumpman.width, self.model.jumpman.height))#Draws our jumpman

class Controller:
    def __init__(self,model):
        self.model = model
    
    def handleEvent(self, event): #Defines all scenarios that can happen to jumpman and movements associated with said states
        if event.type == QUIT:
            pygame.quit()
        if model.mode == MODE_UNDERLADDER: 
            #should be able to move up, left, or right, jump
            if event.type != KEYDOWN:
                return
            if event.key == pygame.K_LEFT:
                self.model.jumpman.vx -= 1.0
            if event.key == pygame.K_RIGHT:
                self.model.jumpman.vx += 1.0
            if event.key == pygame.K_UP:
                self.model.jumpman.vy -= 1.0
            if event.key == pygame.K_SPACE:
                self.model.jumpman.jump()
        elif model.mode == MODE_ABOVELADDER:
            #should be able to move, down, left, right, jump
            if event.type != KEYDOWN:
                return
            if event.key == pygame.K_LEFT:
                self.model.jumpman.vx -= 1.0
            if event.key == pygame.K_RIGHT:
                self.model.jumpman.vx += 1.0
            if event.key == pygame.K_DOWN:
                self.model.jumpman.vy += 1.0
            if event.key == pygame.K_SPACE:
                self.model.jumpman.jump()
        elif model.mode == MODE_ONLADDER:
            #should be able to move up, down
            if event.type != KEYDOWN:
                return
            if event.key == pygame.K_DOWN:
                self.model.jumpman.vx += 1.0
            if event.key == pygame.K_UP:
                self.model.jumpman.vy -= 1.0
        elif model.mode == MODE_ONPLATFORM:
            #should be able to move left, right, jump
            if event.type != KEYDOWN:
                return
            if event.key == pygame.K_LEFT:
                self.model.jumpman.vx -= 1.0
            if event.key == pygame.K_RIGHT:
                self.model.jumpman.vx += 1.0
            if event.key == pygame.K_SPACE:
                self.model.jumpman.jump()
        elif model.mode == MODE_FALLING:
            #should be able to move left, right
            if event.type != KEYDOWN:
                return
            if event.key == pygame.K_LEFT:
                self.model.jumpman.vx -= 1.0
            if event.key == pygame.K_RIGHT:
                self.model.jumpman.vx += 1.0
            if event.key == pygame.K_SPACE:
                self.model.jumpman.jump()

            
if __name__ == '__main__':
    pygame.init()

    size = (WINDOWWIDTH,WINDOWHEIGHT)
    screen = pygame.display.set_mode(size, 0, 32)
    pygame.display.set_caption('Jumpman')

    model = Model()
    view = View(model,screen)
    controller = Controller(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handleEvent(event)
        model.update()
        view.draw()
        pygame.display.update()
        time.sleep(.001)

    pygame.quit()