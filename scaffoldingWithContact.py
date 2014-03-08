# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 20:01:01 2014

@author: koenigin
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
            if self.Y + self.Height >= walk.Y and self.Y + self.Height < walk.Y + walk.Height:
                if self.X + 0.75 * self.Width >= walk.X and self.X + 0.25*self.Width() <= walk.X + walk.Width():
                    onPlatform = True      
                    break
        for up in self.ladders:
            if self.X + 0.25 * self.Width >= up.X and self.X + 0.75*self.Width <= up.X + up.Width:
                if self.Y + self.Height <= up.Y + up.Height and self.Y+ self.Height >= up.Y and not self.Y < up.Y:
                    withinLadder = True
                elif self.Y + self.Height >= up.Y and self.Y < up.Y:
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

            
    