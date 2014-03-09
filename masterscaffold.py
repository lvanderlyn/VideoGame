# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 15:20:32 2014

@author: anneubuntu
"""

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
MODE_UPDOWNLADDER = 6

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

MOVESPEED = 0.3

class Model:
    def __init__(self):
        self.jumpman = Jumpman(0.0,40.0,J_WIDTH,J_HEIGHT) #need jumpman class
        self.platforms = []
        self.genPlatforms()
        self.ladders = []
        self.genLadders()
        self.mode = self.modeFinder()
    
    def update(self):
        self.jumpman.update()
        pastMode = self.mode
        self.mode = self.modeFinder()
        if self.mode == MODE_FALLING:
            self.jumpman.gravityOn()
        if pastMode == MODE_FALLING and self.mode != MODE_FALLING:
            self.jumpman.gravityOff()
        print self.mode
        

    def modeFinder(self):
        bottomInPlatform = False #includes top edge of platform
        topInLadder = False 
        bottomInLadder = False #needs to be inclusive - if bottom edge of man touching bottom edge of ladder, tru
        #or bottom of jumpman touching top edge of ladder        
        sideInLadder = False #needs to be 50% in  ladder
        
        """
        1 - UNDERLADDER         
        bottom in platform and top in ladder and sideInLadder and not bottom in ladder
        
        2 - ABOVELADDER
        bottom in platform and bottom in ladder and not top in ladder and side in ladder
        
        3 - ONLADDER
        bottom in ladder and bottom not in platform
    
        
        4 -  ONPLATFROM
        bottom in platform and not bottom in ladder
        
        5 - FALLING
        not any of above
        
        6 - UPDOWNLADDER
        bottom in ladder and top in ladder and bottom in platform
        """
        
        for platform in self.platforms:
            xMid = platform.rect.left + (0.5*platform.width) # VERTICAL line
            yMid = platform.rect.top + (0.5*platform.height) #HORIZONTAL line
            jxMid = self.jumpman.rect.left + (0.5*J_WIDTH) #  VERTICAL line
            jyMid = self.jumpman.rect.top + (0.5*J_HEIGHT) #HORIZONTAL line
            if platform.rect.collidepoint(jxMid,yMid):
                if platform.rect.collidepoint(xMid,self.jumpman.rect.bottom):
                    bottomInPlatform = True
                    break
        for ladder in self.ladders:
            xMid = ladder.rect.left + (0.5*LADDER_WIDTH) # VERTICAL line
            yMid = ladder.rect.top + (0.5*ladder.height) #HORIZONTAL line
            jxMid = self.jumpman.rect.left + (0.5*J_WIDTH) #  VERTICAL line
            #jyMid = self.jumpman.top + (0.5*J_HEIGHT) #HORIZONTAL line
            #checks if sideInLadder, at least 50% of jumpman in the ladder
            if ladder.rect.collidepoint(jxMid,yMid):
                if ladder.rect.collidepoint(xMid, self.jumpman.rect.top):
                    topInLadder = True
                if ladder.rect.collidepoint(xMid, self.jumpman.rect.bottom):
                    bottomInLadder = True
        if bottomInPlatform and topInLadder and not bottomInLadder:
            return MODE_UNDERLADDER
        if bottomInPlatform and bottomInLadder and not topInLadder:
            return MODE_ABOVELADDER
        if bottomInLadder and topInLadder and not bottomInPlatform:
            return MODE_ONLADDER
        if bottomInLadder and topInLadder and bottomInPlatform:
            return MODE_UPDOWNLADDER
        if bottomInPlatform and not bottomInLadder and not topInLadder:
            return MODE_ONPLATFORM
        if not bottomInPlatform and not bottomInLadder and not topInLadder:
            return MODE_FALLING
        
    
    def inContact(self, jumpman, pladder):#Not done yet either
        #determines if jumpman is in contact with a given platform or ladder
        pass
    
    def genPlatforms(self):
        #Generates platforms depending of windowheight/width    
        numLayers  = int(math.ceil(WINDOWHEIGHT/(2.0*J_HEIGHT))) #Number of layers of platforms allowed
        h = WINDOWHEIGHT/numLayers
        initPlat = Platform(0, WINDOWHEIGHT-PLATFORM_HEIGHT, WINDOWWIDTH)
        self.platforms.append(initPlat)
        for i in range(0,10):
            y = random.randint(0, numLayers)*h + h
            width = random.randint(50,150) #change this to make variable widths
            x = random.randint(0,WINDOWWIDTH-width)           
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
            possiblePlatforms = []
            #print "do we try to build ladder? ", r
            if r==0 or r==1: #2/3 chance of having a ladder going down              
                for toPlatform in self.platforms:
                    if not (toPlatform==fromPlatform):
                        for i in range(random.randint(0,4)):#generate 0 to 8 ladders
                            x_pos = random.randint(fromPlatform.x, (fromPlatform.x + fromPlatform.width-LADDER_WIDTH)) #choose random x position on platform                                               
                            if x_pos in range(toPlatform.x, toPlatform.x + toPlatform.width-LADDER_WIDTH):
                                if toPlatform.y>fromPlatform.y:
                                    possiblePlatforms.append(toPlatform)
                                    break
                #print "fromPlatform.y = ", fromPlatform.y
                for possPlat in possiblePlatforms: #Can't go higher than 2h
                    #print "possPlat.y = ", possPlat.y
                    if (possPlat.y > (fromPlatform.y + (2*h))):
                        #print "removed", possPlat.y
                        possiblePlatforms.remove(possPlat)       
                if len(possiblePlatforms) != 0:
                    p = random.randint(0,len(possiblePlatforms)-1)
                    endPlatform = possiblePlatforms[p]                
                    ladder = Ladder(x_pos, fromPlatform.y, endPlatform.y - fromPlatform.y)
                    #print "ladder", "x_pos = ", x_pos, "fromPlatform.y = ", fromPlatform.y, "toPlatform.y = ", toPlatform.y
                    if len(self.ladders) > 0:                    
                        for allLadders in self.ladders:
                            print allLadders.rect
                            if ((ladder.x+LADDER_WIDTH) in range(allLadders.x, allLadders.x + LADDER_WIDTH)) or (ladder.x in range(allLadders.x, allLadders.x + LADDER_WIDTH)):
                                print ladder.x, "found a bad one!"                                
                                continue                            
                            else:
                                self.ladders.append(ladder)
                                print ladder.x, "created a ladder"
                        print "--------"
                    else:
                        self.ladders.append(ladder)
            
    

class Jumpman: #Defines Jumpman the one and only
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vx = 0.0
        self.vy = 0.0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        self.vy -=0.5 #fiddle with actual number, was selected arbitrarily. it felt GOOD
    
    def gravityOn(self):
        self.vy += 0.005 #selected randomly, can change
        
    def gravityOff(self):
        self.vy = 0.0 #selected randomly, can change
        
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
        pressed = pygame.key.get_pressed()
        if self.model.mode == MODE_UNDERLADDER: 
            #should be able to move up, left, or right, jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT]:
                self.model.jumpman.vx = -1.0*MOVESPEED
            if pressed[K_RIGHT]:
                self.model.jumpman.vx = 1.0*MOVESPEED
            if pressed[K_UP]:
                self.model.jumpman.vy = -1.0*MOVESPEED
            if pressed[K_SPACE]:
                self.model.jumpman.jump()
        elif self.model.mode == MODE_ABOVELADDER:
            #should be able to move, down, left, right, jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT]:
                self.model.jumpman.vx = -1.0*MOVESPEED
            if pressed[K_RIGHT]:
                self.model.jumpman.vx = 1.0*MOVESPEED
            if pressed[K_DOWN]:
                self.model.jumpman.vy = 1.0*MOVESPEED
            if pressed[K_SPACE]:
                self.model.jumpman.jump()
        elif self.model.mode == MODE_ONLADDER:        
            #should be able to move up, down
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT]:
                self.model.jumpman.vx = -1.0*MOVESPEED
            if pressed[K_RIGHT]:
                self.model.jumpman.vx = 1.0*MOVESPEED
            if pressed[K_DOWN]:
                self.model.jumpman.vy = 1.0*MOVESPEED
            if pressed[K_UP]:
                self.model.jumpman.vy = -1.0*MOVESPEED
            if pressed[K_SPACE]:
                self.model.jumpman.jump()
        elif self.model.mode == MODE_ONPLATFORM:
            #should be able to move left, right, jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT]:
                self.model.jumpman.vx = -1.0*MOVESPEED
            if pressed[K_RIGHT]:
                self.model.jumpman.vx = 1.0*MOVESPEED
            if pressed[K_SPACE]:
                self.model.jumpman.jump()
        elif self.model.mode == MODE_FALLING:
            #should be able to move left, right
            self.model.jumpman.vx = 0
            if pressed[K_LEFT]:
                self.model.jumpman.vx = -1.0*MOVESPEED
            if pressed[K_RIGHT]:
                self.model.jumpman.vx = 1.0*MOVESPEED
        elif self.model.mode == MODE_UPDOWNLADDER:
            #should be able to move up down left right jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if event.type != KEYDOWN:
                return
            if pressed[K_LEFT]:
                self.model.jumpman.vx = -1.0*MOVESPEED
            if pressed[K_RIGHT]:
                self.model.jumpman.vx = 1.0*MOVESPEED
            if pressed[K_UP]:
                self.model.jumpman.vy = -1.0*MOVESPEED
            if pressed[K_DOWN]:
                self.model.jumpman.vy = 1.0*MOVESPEED
            if pressed[K_SPACE]:
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