# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 15:24:50 2014

@author: ragspiano
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 13:29:57 2014

@author: koenigin
"""

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


#Import necessary modules
import pygame
import math
from pygame.locals import *
import random
import time

#Set up game mode constants
MODE_UNDERLADDER = 1
MODE_ABOVELADDER = 2
MODE_ONLADDER = 3
MODE_ONPLATFORM = 4
MODE_FALLING = 5
MODE_UPDOWNLADDER = 6

#set window constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 800


# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

#set size constants
J_HEIGHT = 40
J_WIDTH = 20
J_LIVES = 6
PLATFORM_HEIGHT = 10
LADDER_WIDTH = 30
BULLET_WIDTH = 10
BULLET_HEIGHT = 10

#these need to be divisible by 3
GEM_WIDTH = 15
GEM_HEIGHT = 15

#more constants
NUM_GEMS = 10
MOVESPEED = 0.9
BULLET_SPEED = 2

class Model:
    """Set up all model objects"""
    def __init__(self, jumpmanLives, level):
        '''set up things all model objects need, including level so lives 
        can be maintained between levels'''
        self.jumpman = Jumpman(WINDOWWIDTH/2.0, WINDOWHEIGHT-PLATFORM_HEIGHT - J_HEIGHT, J_WIDTH, J_HEIGHT, jumpmanLives)
        self.platforms = []
        self.genPlatforms()
        self.ladders = []
        self.genLadders()
        self.gems = []
        self.levelGems = NUM_GEMS+(level*2)
        self.genGems()
        self.mode = self.modeFinder()
        self.bullets = []
        self.level = level
    
    def update(self):
        '''updates model to reflect changes in things like jumpman position 
        and gravity as well as gem count and lives'''
        self.jumpman.update()
        pastMode = self.mode
        self.mode = self.modeFinder()
        if self.mode == MODE_FALLING:
            self.jumpman.gravityOn()
        if pastMode == MODE_FALLING and self.mode != MODE_FALLING:
            if self.jumpman.vy > 1.2: #chosen so that you die if you fall off a platform but not if you jump
                self.jumpman.die()
                fall.play()
            self.jumpman.gravityOff()
            
        #check if jumpman picked up any gems
        for gem in self.gems:
            if self.inContact(self.jumpman, gem):
                gemNoise.play()
                self.gems.remove(gem)
                self.jumpman.gemCount += 1
                
        #try to generate some bullets to be fired
        if random.randint(0,200-(level*15))==0:
            self.bullets.append(self.makeBullet())
        
        #check if any bullets hit jumpman
        if len(self.bullets)>0:
            for bullet in self.bullets:
                bullet.update()
                if self.inContact(self.jumpman, bullet):
                    bulletNoise.play()
                    self.bullets.remove(bullet)
                    self.jumpman.die()
        
        #check if any bullets exited the screen
        if len(self.bullets)>0:
            for bullet in self.bullets:
                if bullet.x > WINDOWWIDTH or bullet.x < 0 or bullet.y > WINDOWHEIGHT or bullet.y < 0:
                    self.bullets.remove(bullet)
    
    def checkIfCollectedAllGems(self):
        '''checks if all gems are collected so that the game can move on to
        the next level'''
        if self.jumpman.gemCount == self.levelGems + 1:
            return False
        else:
            return True
                
    def modeFinder(self):
        '''checks what objects the jumpman is in contact with to determine
        what mode the game is in and thus what movement/gravity is allowed
        
        #1 - UNDERLADDER         
        #bottom in platform and top in ladder and sideInLadder and not bottom in ladder
        
        #2 - ABOVELADDER
        #bottom in platform and bottom in ladder and not top in ladder and side in ladder
        
        #3 - ONLADDER
        #bottom in ladder and bottom not in platform
    
        #4 -  ONPLATFROM
        #bottom in platform and not bottom in ladder
        
        #5 - FALLING
        #not any of above
        
        #6 - UPDOWNLADDER
        #bottom in ladder and top in ladder and bottom in platform
                    
        '''
        bottomInPlatform = False #includes top edge of platform
        topInLadder = False 
        bottomInLadder = False #needs to be inclusive - if bottom edge of man touching bottom edge of ladder, tru
        #or bottom of jumpman touching top edge of ladder        
        sideInLadder = False #needs to be 50% in  ladder
        
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
        #Based on the above comment these seperate contact into modes
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
        
    
    def inContact(self, jumpman, other):
        '''function that checks if objects collide to determine bullet kill 
        or gem collection'''
        return jumpman.rect.colliderect(other.rect)
    
    def genPlatforms(self):
        '''function for randomly generating platforms for the model'''
        numLayers  = int(math.ceil(WINDOWHEIGHT/(2.0*J_HEIGHT))) #Number of layers of platforms allowed
        h = WINDOWHEIGHT/numLayers
        initPlat = Platform(0, WINDOWHEIGHT-PLATFORM_HEIGHT, WINDOWWIDTH)
        self.platforms.append(initPlat)
        for i in range(0,10):
            y = random.randint(1, numLayers)*h
            width = 200 #change this to make variable widths
            x = random.randint(0,WINDOWWIDTH-width)#Picks a random starting x position           
            plat = Platform(x,y,width)
            self.platforms.append(plat)
              
    def genLadders(self): 
        '''Uses the location of platforms to psuedo-randomly generate ladders'''
        numLayers = math.ceil(WINDOWHEIGHT/(2.0*J_HEIGHT))
        h = WINDOWHEIGHT/numLayers
        height = 0
        x_pos = 0
        y_coor = 0
        numLadders = 5
        i = 0
        #runs through all the platforms on the screen
        for fromPlatform in self.platforms:
            for chance in range (0,100): #Gives each platform 15 tries to find possible ladders         
                possiblePlatforms = []    
                x_pos = random.randint(fromPlatform.x, fromPlatform.x+fromPlatform.width) #defines a starting x position          
                #Checks for platforms that we could potentially build ladders to                
                for toPlatform in self.platforms:
                        if toPlatform.y>fromPlatform.y:
                            if x_pos in range(toPlatform.x, toPlatform.x+toPlatform.width-LADDER_WIDTH):
                                possiblePlatforms.append(toPlatform)
                                goodXPos = x_pos+0
                if len(possiblePlatforms) != 0:
                    break#We don't need more chances

            if len(possiblePlatforms) != 0:
                p = random.randint(0,len(possiblePlatforms)-1)#picks a random end platform
                endPlatform = possiblePlatforms[p]
                ladder = Ladder(goodXPos, fromPlatform.y, endPlatform.y - fromPlatform.y)#Generates a ladder


                if len(self.ladders) > 0:#Checks the other ladders in existence for overlaps
                    goodLadder = False                
                    for j in range (len(self.ladders)):
                        lad = self.ladders[j]
                        if (ladder.y > lad.y+lad.height):
                            goodLadder = True
                        if (ladder.x >= lad.x) and (ladder.x < (lad.x + LADDER_WIDTH)):
                            goodLadder = False
                            break
                        if (ladder.x <= lad.x) and (ladder.x+LADDER_WIDTH in range (lad.x, lad.x+LADDER_WIDTH)):
                            goodLadder = False
                            break
                        else:
                            goodLadder = True
                    if goodLadder == True:
                        self.ladders.append(ladder)#Puts the ladder in

                else:
                    self.ladders.append(ladder)#Creates the first ladder
        
    def genGems(self):
        '''using similar logic to the above, randomly generates gems, trying
        to prevent overlapping'''
        i = self.levelGems
        while i>=0:
            p = random.randint(0,len(self.platforms)-1)#Picks a random platform
            platform = self.platforms[p]
            x_pos = random.randint(platform.x, (platform.x + platform.width - (GEM_WIDTH/3)))#Picks a random starting x position
            gem = Gem(x_pos-GEM_WIDTH, platform.y-GEM_HEIGHT, GEM_WIDTH, GEM_HEIGHT)#Creates a possible gem at that position
            
            if len(self.gems) ==0:
                self.gems.append(gem)#Creates the first gem
                i = i-1

            else:
                goodGem = False
                for allGems in self.gems:#Checks the rest of the gems for overlaps
                    if (gem.y > allGems.y+allGems.height):
                        goodGem = True
                    if (gem.x >= allGems.x) and (gem.x < (allGems.x + GEM_WIDTH)):
                        goodGem = False
                        break
                    if (gem.x <= allGems.x) and (gem.x+GEM_WIDTH in range (allGems.x, allGems.x+GEM_WIDTH)):
                        goodGem = False
                        break
                    else:
                        goodGem = True                        
                if goodGem == True:
                    self.gems.append(gem)#Creates the next gem
                    i = i-1
    
    def makeBullet(self):
        '''generates a bullet with an arbitrary start/ horizontal/vertical
        direction'''
        xOrY = random.randint(0,1) #0 = False = traveling vertical, 1=True=traveling horizontal
        x=0
        y=0
        direction = 0
        if xOrY:
            leftOrRight = random.randint(0,1) #decides whether bullet comes from left side of screen or right
            if leftOrRight:
                x = 0
                direction = 1
            else:
                x = WINDOWWIDTH
                direction = -1
            y = random.randint(0, WINDOWHEIGHT)
        else:
            topOrBottom = random.randint(0,1) #decides whether bullet comes from top of screen or bottom
            if topOrBottom:
                y = 0
                direction = 1
            else:
                y = WINDOWHEIGHT
                direction = -1
            x = random.randint(0,WINDOWWIDTH)
        return Bullet(x,y,BULLET_WIDTH,BULLET_HEIGHT,xOrY,direction)

class Actor:
    '''moving objects within the model
        gems, jumpman, and bullets are actors
    '''
    def __init__(self,x,y,width, height):
        '''initializes position and dimension attributes shared by all actors'''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vx = 0.0
        self.vy = 0.0
    
    def update(self):
        '''updates the actor's position and updates the rectangle object of the
        actor'''
        self.x += self.vx
        self.y += self.vy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
class Jumpman(Actor):
    '''
    Defines jumpman the one and only
    '''
    def __init__(self,x,y,width,height, lives):
        '''
        all attributes of actor plus the number of lives he has left
        '''
        Actor.__init__(self,x,y,width, height)
        self.gemCount = 0 #jumpman keeps track of collected gems
        self.lives = lives #also keeps track of lives
        self.image = pygame.image.load("Jumpman.png") #jumpman graphic
        transcolor = BLACK
        self.image.set_colorkey(transcolor)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.lostLife = False
    
    def update(self):
        '''updates position if the jumpman is still within the play window'''
        if self.rect.left + self.vx >= 0 and self.rect.right + self.vx <= WINDOWWIDTH and self.rect.bottom + self.vy <= WINDOWHEIGHT-5:
            Actor.update(self)

    def jump(self):
        '''causes the jumpman to jump up'''
        self.vy -=0.85 #fiddle with actual number, was selected arbitrarily. it felt GOOD
    
    def gravityOn(self):
        '''a constant increase on velocity to simulate gravity'''
        self.vy += 0.01 #selected randomly, can change
        
    def gravityOff(self):
        '''turns gravity off because should not affect jumpman on a ladder/platform'''
        self.vy = 0.0 #selected randomly, can change
    
    def die(self):
        '''causes jumpman to lose a life'''
        self.lostLife = True
        self.lives -=1
    
    def respawn(self):
        '''moves jumpman to bottom of screen to re-spawn'''
        self.lostLife = False
        #i want to put in some kind of death effect so he doesn't just jump to a new spot
        self.x = WINDOWWIDTH/2
        self.y = WINDOWHEIGHT - PLATFORM_HEIGHT - J_HEIGHT
        self.vx = 0
        self.vy = 0
        
        
class Platform: 
    '''Defines platform class'''
    def __init__(self, x, y, width):
        '''initializes all platform attributes
        doesn't need a height because defined by constant'''
        self.x = x
        self.y = y
        self.width = width
        self.height = PLATFORM_HEIGHT #Height 10px
        image = pygame.image.load("Platformsprite.png")
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.transform.scale(image, (self.width, self.height))
        
class Ladder: 
    '''Defines ladder class'''
    def __init__(self, x, y, height):
        ''' doesn't need width because defined by comment'''
        self.x = x
        self.y = y
        self.width = LADDER_WIDTH #Width 30px
        self.height = height
        image = pygame.image.load("Laddersprite.png")
        transcolor = BLACK
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.transform.scale(image, (self.width, self.height))
        
class Gem(Actor):
    '''defining a subclass for gems'''
    def __init__(self,x,y,width,height):
        '''initialising with a size and position'''
        Actor.__init__(self,x,y,width, height)
        
    def update(self):
        '''doesn't do anything but every actor has one'''
        Actor.update(self)
        
    
class Bullet(Actor):
    '''defines bullet subclass'''
    def __init__(self,x,y,width,height, xOrY, posOrNeg):
        '''initializes bullets with things like size and speed'''
        #xOrY is true if in x direction, false if negative direction
        #posOrNeg is 1 if traveling in increasing x or y, negative if decreasing
        Actor.__init__(self,x,y,width,height)
        if xOrY:
            self.vx = BULLET_SPEED*posOrNeg
            self.vy = 0.0
        else:
            self.vx = 0.0
            self.vy = BULLET_SPEED*posOrNeg
    
    def update(self):
        '''updates position of bullet based on Actor update'''
        Actor.update(self)
            
    
class View:
    '''veiw class controls window display'''
    def __init__(self, model, screen): 
        '''View contains model and screen'''
        self.model = model
        self.screen = screen
        
    def draw(self):
        '''draws all the model objects so they appear in the window'''
        self.screen.fill(BLACK) #Makes screen bg black
        for platform in self.model.platforms:
            screen.blit(platform.image, (platform.x, platform.y)) #Draws all of the platforms
        for ladder in self.model.ladders:
            screen.blit(ladder.image, (ladder.x, ladder.y)) #Draws all of the ladders
        screen.blit(self.model.jumpman.image.convert_alpha(), self.model.jumpman.rect)#Draws our jumpman
        for gem in self.model.gems: #draws gems as our fancy 4-square arrangement
            pygame.draw.rect(self.screen, WHITE, (gem.x+GEM_WIDTH/3, gem.y, GEM_WIDTH/3, GEM_HEIGHT/3))
            pygame.draw.rect(self.screen, WHITE, (gem.x, gem.y+GEM_HEIGHT/3, GEM_WIDTH/3, GEM_HEIGHT/3))
            pygame.draw.rect(self.screen, WHITE, (gem.x+(2*GEM_WIDTH/3), gem.y+GEM_HEIGHT/3, GEM_WIDTH/3, GEM_HEIGHT/3))
            pygame.draw.rect(self.screen, WHITE, (gem.x+GEM_WIDTH/3, gem.y+(2*GEM_HEIGHT/3), GEM_WIDTH/3, GEM_HEIGHT/3))
        for bullet in self.model.bullets: #draws bullets
            pygame.draw.rect(self.screen, WHITE, bullet.rect)
            
    def animateDeathtoWhite(self):
        '''flashes jumpman to original appearence'''
        screen.blit(self.model.jumpman.image.convert_alpha(), self.model.jumpman.rect)
        pygame.time.wait(100)
        
    def animateDeathtoBlack(self):
        '''flashes jumpman black in death'''
        pygame.draw.rect(self.screen, BLACK, self.model.jumpman.rect)
        pygame.time.wait(100)
        
    def drawInfo(self, font):
        '''Displays lives and gem count information at top of screen'''
        pygame.draw.rect(self.screen, BLACK, (0,0,WINDOWWIDTH,30))
        label = font.render("LIVES REMAINING: ", 1, WHITE)
        self.screen.blit(label, (10, 10))
        for i in range(self.model.jumpman.lives):
            pygame.draw.rect(self.screen, WHITE, (210+(15*i),16,10,10))
        label2 = font.render("GEMS COLLECTED: "+str(self.model.jumpman.gemCount)+ " / "+str(self.model.levelGems+1),1,WHITE)
        self.screen.blit(label2, (WINDOWWIDTH - 270,10))
        
    def newLevel(self,font,level):
        '''displays level screen between levels'''
        self.screen.fill(BLACK)
        label = font.render("Level: "+str(level), 1, (255,255,255))
        self.screen.blit(label,(WINDOWWIDTH/2,WINDOWHEIGHT/2))

    def gameOver(self, font, level):
        '''displays game over screen when all lives are spent'''
        self.screen.fill(BLACK)
        label = font.render("GAME OVER!", 1, WHITE)
        label2 = font.render("Level: "+str(level), 1, WHITE)
        self.screen.blit(label, (WINDOWWIDTH/2, WINDOWHEIGHT/2))
        self.screen.blit(label2, (WINDOWWIDTH/2, WINDOWHEIGHT/2+70))  

class Controller:
    '''controls the jumpman's motion'''
    def __init__(self,model):
        '''initializes the model'''
        self.model = model
    
    def handleEvent(self, event):
        '''Defines all scenarios that can happen to jumpman and movements associated with said states
            Takes in arrow keys and WASD input, and spacebar to jump'''
        if event.type == QUIT:
            pygame.quit()
        pressed = pygame.key.get_pressed() #finds keys pressed so multiple input can be taken
        if self.model.mode == MODE_UNDERLADDER: 
            #should be able to move up, left, or right, jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
            if pressed[K_UP] or pressed[ord('w')]:
                self.model.jumpman.vy = -1.0*MOVESPEED
                walk.play()
            if pressed[K_SPACE]:
                jumpNoise.play()
                self.model.jumpman.jump()
        elif self.model.mode == MODE_ABOVELADDER:
            #should be able to move, down, left, right, jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
            if pressed[K_DOWN] or pressed[ord('s')]:
                self.model.jumpman.vy = 1.0*MOVESPEED
                walk.play()
            if pressed[K_SPACE]:
                jumpNoise.play()
                self.model.jumpman.jump()
        elif self.model.mode == MODE_ONLADDER:        
            #should be able to move up, down
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
            if pressed[K_DOWN] or pressed[ord('s')]:
                self.model.jumpman.vy = 1.0*MOVESPEED
                walk.play()
            if pressed[K_UP] or pressed[ord('w')]:
                self.model.jumpman.vy = -1.0*MOVESPEED
                walk.play()
            if pressed[K_SPACE]:
                jumpNoise.play()
                self.model.jumpman.jump()
        elif self.model.mode == MODE_ONPLATFORM:
            #should be able to move left, right, jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
            if pressed[K_SPACE]:
                jumpNoise.play()
                self.model.jumpman.jump()
        elif self.model.mode == MODE_FALLING:
            #should be able to move left, right
            self.model.jumpman.vx = 0
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
        elif self.model.mode == MODE_UPDOWNLADDER:
            #should be able to move up down left right jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if event.type != KEYDOWN:
                return
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
            if pressed[K_UP] or pressed[ord('w')]:
                self.model.jumpman.vy = -1.0*MOVESPEED
                walk.play()
            if pressed[K_DOWN] or pressed[ord('s')]:
                self.model.jumpman.vy = 1.0*MOVESPEED
                walk.play()
            if pressed[K_SPACE]:
                self.model.jumpman.jump()
                jumpNoise.play()
            
if __name__ == '__main__':
    '''THE MAIN GAME STUFF!'''
    
    #initializes sound effect things
    pygame.mixer.pre_init(44100,-16,2,2048)
    pygame.init()
    background = pygame.mixer.Sound('back.wav')
    jumpNoise = pygame.mixer.Sound('jump.wav')
    bulletNoise = pygame.mixer.Sound('bullet.wav')
    walk = pygame.mixer.Sound('walk.wav')
    fall = pygame.mixer.Sound('fall.wav')
    gemNoise = pygame.mixer.Sound('gem.wav')
    background.play() #intro music

    size = (WINDOWWIDTH,WINDOWHEIGHT)
    screen = pygame.display.set_mode(size, 0, 32)
    pygame.display.set_caption('Jumpman')
    
    #initial level and lives
    level = 0
    lives = J_LIVES
    
    #two font sizes
    font = pygame.font.SysFont("monospace", 50)
    font2 = pygame.font.SysFont("monospace",20)
    
    label = font.render("JUMPMAN", 1, WHITE)
    screen.blit(label, (WINDOWWIDTH/2, WINDOWHEIGHT/2))
    pygame.display.update()
    pygame.time.wait(9000)

    #this loop controls the game/gameover state.  runs while jumpman has lives left  
    while(lives>=0):
        #makes new level
        model = Model(lives,level)
        view = View(model,screen)
        controller = Controller(model)
        view.newLevel(font,level)
        pygame.display.update()
        pygame.time.wait(2500)
        running = True
        #this loop is the running loop within a single game level
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                controller.handleEvent(event)
            model.update()
            gameNotYetWon = model.checkIfCollectedAllGems() #checks if all gems collected
            if gameNotYetWon:
                view.draw() #draws all the things on screen
                view.drawInfo(font2) #draws the info bar
                if model.jumpman.lostLife: 
                    for i in range(5): #this animates the flashing effect when jumpman dies
                        view.animateDeathtoBlack()
                        pygame.display.update()
                        view.animateDeathtoWhite()
                        pygame.display.update()
                    model.jumpman.lostLife = False
                    model.jumpman.respawn()
                    screen.blit(model.jumpman.image.convert_alpha(), model.jumpman.rect)#Draws our jumpman
            else: #if all gems collected
                pygame.time.wait(500)
                level +=1
                running = False
                lives = model.jumpman.lives
                break
                
            pygame.display.update()
            time.sleep(.001)
            if model.jumpman.lives == 0: #kills game loop if no more lives
                lives = -1
                running = False
    #display gameover and quit
    view.gameOver(font, level)
    pygame.display.update()
    time.sleep(5)
    pygame.quit()