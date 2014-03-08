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

import math

MODE_UNDERLADDER = 1
MODE_ABOVELADDER = 2
MODE_ONLADDER = 3
MODE_ONPLATFORM = 4
MODE_FALLING = 5

class Model:
    def __init__(self):
        self.jumpman = Jumpman(x,y,width,height) #need jumpman class
        self.platforms = []
            #put code to generate platforms to fill the screen
        self.ladders = []
            #code to generate ladders b/w platforms and place in array
        self.mode = modeFinder
    
    def update(self):
        self.jumpman.update()
        
    def modeFinder(self):#So not even done yet
        #if jumpman in contact with platform and ladder - mode canclimb
        #if in contact with platform and not ladder - mode walk
        #if in contact with ladder and not platform - mode climb
        #if in contact with nothing - mode fall
        #uses inContact as a helper function
    
    def inContact(self, jumpman, pladder):#Not done yet either
        #determines if jumpman is in contact with a given platform or ladder
    
    def genPlatform(self):
        #Generates platforms depending of windowheight/width    
        numLayers  = math.ceil(WINDOWHEIGHT/(2.0*J_HEIGHT)) #Number of layers of platforms allowed
        for layer in range(numLayers):
            y = (WINDOWHEIGHT/numLayers)*layer
            x = 0
            width = WINDOWWIDTH
            plat = Platform(x,y,width)
            self.platforms.append(plat)
            
    
    def genLadder(self): #Not Dones
        #Generates ladders depending on the location of the platforms

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
        self.height = 10 #Height 10px
        self.rect = pygame.Rect(x, y, width, height)
        
class Ladder: #Defines ladder class
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.width = 30 #Width 30px
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
class View:
    def __init__(self, model, screen): #View contains model and screen
        self.model = Model
        self.screen = screen
        
    def draw(self):
        self.screen.fill(BLACK) #Makes screen bg black
        for platform in self.model.platforms:
            pygame.draw.Rect(self.screen, GREEN, pygame.Rect(platform.x, platform.y, platform.width, platform.height)) #Draws all of the platforms
        for ladder in self.model.ladders:
            pygame.draw.Rect(self.screen, BLUE, pygame.Rect(ladder.x, ladder.y, ladder.width, ladder.height)) #Draws all of the ladders
        pygame.draw.Rect(self.model.jumpman.x, self.model.jumpman.y, self.model.jumpman.width, self.model.jumpman.height) #Draws our jumpman

class Controller:
    def __init__(self,model):
        self.model = model
    
    def handleEvent(self, event): #Defines all scenarios that can happen to jumpman and movements associated with said states
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
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
        elif model.mode == MODE_ONGROUND:
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

            
    