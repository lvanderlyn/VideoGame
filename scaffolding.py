# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 16:12:53 2014

@author: anneubuntu
"""

"""
Scaffolding -
Implementing the model-view-controller structure
Leaving some functions undefined - we can work on them later once we know what they
need to contain
THIS IS GOOD AND IMPORTANT
"""

class Model:
    def __init__(self):
        self.jumpman = Jumpman(x,y,width,height)
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
    
    def inContact(jumpman, pladder, self):#Not done yet either
        #determines if jumpman is in contact with a given platform or ladder
    
        
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
    