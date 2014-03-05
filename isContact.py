# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 14:32:50 2014

@author: koenigin
"""
import pygame, sys, random
from pygame.locals import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 1600
WINDOWHEIGHT = 850
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

MOVESPEED = 6

player = [pygame.draw.rect(windowSurface, WHITE, (100,0,100,100))]

ladder = [pygame.draw.rect(windowSurface, BLUE, (50, 100, 150, 850))]

plat = [pygame.draw.rect(windowSurface, GREEN, (0, 800, 300, 100))]


def isContact(actor, other):
    '''takes in the jumpmann actor and an object and determines if there is contact between the two'''
    if (actor.right - 0.5* actor.width <= other.right) and (actor.right - 0.5*actor.width >= other.left):
        if actor.bottom <= other.top:
            return True
    else:
        return False


def modeSelect(actor, climb, walk):
    '''take in a list of climable object called 'climb', and list of platforms
    called 'walk' and determines the mode (controls allowed) based on what
    the jumperman is in contact with'''
    for up in climb:
        if isContact(actor, up):
            Climb = True
            break
    for platform in walk:
        if isContact(actor, platform):
            Walk = True
            break
    if Walk and Climb:
        return 'both'
    elif Walk and not Climb:
        return 'walk'
    elif Climb and not Walk:
        return 'climb'
    else:
        return 'non-interactive'
 
       #Code below currently does not work!!!
       #was attempting to use case selector for mode
#while True:
#    for event in pygame.event.get():
#        mode = modeSelect(player, ladder, plat)
#        if event.type == QUIT:
#            running = False
#            pygame.quit()
#            sys.exit()
#        if mode == 'both':
#            if event.type == KEYDOWN:                   #denotes that one or more keys are pushed down
#                # change the keyboard variables
#                if event.key == K_LEFT or event.key == ord('a'):
#                    moveRight = False
#                    moveLeft = True
#                if event.key == K_RIGHT or event.key == ord('d'):
#                    moveLeft = False
#                    moveRight = True
#                if event.key == K_UP or event.key == ord('w'):
#                    moveDown = False
#                    moveUp = True
#                if event.key == K_DOWN or event.key == ord('s'):
#                    moveUp = False
#                    moveDown = True
#            if event.type == KEYUP:                     #denotes that no keys are pushed down
#                if event.key == K_ESCAPE:
#                    pygame.quit()
#                    sys.exit()
#                if event.key == K_LEFT or event.key == ord('a'):
#                    moveLeft = False
#                if event.key == K_RIGHT or event.key == ord('d'):
#                    moveRight = False
#                if event.key == K_UP or event.key == ord('w'):
#                    moveUp = False
#                if event.key == K_DOWN or event.key == ord('s'):
#                    moveDown = False
#                if event.key == ord('x'):
#                    player.top = random.randint(0, WINDOWHEIGHT - player.height)
#                    player.left = random.randint(0, WINDOWWIDTH - player.width)
#        elif mode == 'climb':
#            if event.type == KEYDOWN:                   #denotes that one or more keys are pushed down
#            # change the keyboard variables
#                if event.key == K_LEFT or event.key == ord('a'):
#                    moveRight = False
#                    moveLeft = False
#                if event.key == K_RIGHT or event.key == ord('d'):
#                    moveLeft = False
#                    moveRight = False
#                if event.key == K_UP or event.key == ord('w'):
#                    moveDown = False
#                    moveUp = True
#                if event.key == K_DOWN or event.key == ord('s'):
#                    moveUp = False
#                    moveDown = True
#            if event.type == KEYUP:                     #denotes that no keys are pushed down
#                if event.key == K_ESCAPE:
#                    pygame.quit()
#                    sys.exit()
#                if event.key == K_LEFT or event.key == ord('a'):
#                    moveLeft = False
#                if event.key == K_RIGHT or event.key == ord('d'):
#                    moveRight = False
#                if event.key == K_UP or event.key == ord('w'):
#                    moveUp = False
#                if event.key == K_DOWN or event.key == ord('s'):
#                    moveDown = False
#                if event.key == ord('x'):
#                    player.top = random.randint(0, WINDOWHEIGHT - player.height)
#                    player.left = random.randint(0, WINDOWWIDTH - player.width)
#        elif mode == 'walk':
#            if event.type == KEYDOWN:                   #denotes that one or more keys are pushed down
#            # change the keyboard variables
#                if event.key == K_LEFT or event.key == ord('a'):
#                    moveRight = False
#                    moveLeft = True
#                if event.key == K_RIGHT or event.key == ord('d'):
#                    moveLeft = False
#                    moveRight = True
#                if event.key == K_UP or event.key == ord('w'):
#                    moveDown = False
#                    moveUp = False
#                if event.key == K_DOWN or event.key == ord('s'):
#                    moveUp = False
#                    moveDown = False
#            if event.type == KEYUP:                     #denotes that no keys are pushed down
#                if event.key == K_ESCAPE:
#                    pygame.quit()
#                    sys.exit()
#                if event.key == K_LEFT or event.key == ord('a'):
#                    moveLeft = False
#                if event.key == K_RIGHT or event.key == ord('d'):
#                    moveRight = False
#                if event.key == K_UP or event.key == ord('w'):
#                    moveUp = False
#                if event.key == K_DOWN or event.key == ord('s'):
#                    moveDown = False
#                if event.key == ord('x'):
#                    player.top = random.randint(0, WINDOWHEIGHT - player.height)
#                    player.left = random.randint(0, WINDOWWIDTH - player.width)
#        else:
#            moveRight = False
#            moveLeft = False
#            moveUp = False
#            moveDown = False    
#      
#    # draw the black background onto the surface
#    windowSurface.fill(BLACK)
#    # move the player
#    if moveDown and player.bottom < WINDOWHEIGHT:
#        player.top += MOVESPEED
#    if moveUp and player.top > 0:
#        player.top -= MOVESPEED
#    if moveLeft and player.left > 0:
#        player.left -= MOVESPEED
#    if moveRight and player.right < WINDOWWIDTH:
#        player.right += MOVESPEED
#
#    # draw the player onto the surface
#    pygame.draw.rect(windowSurface, BLUE, ladder)    
#    pygame.draw.rect(windowSurface, WHITE, player)
# 
#
#    # draw the window onto the screen
#    pygame.display.update()
#    mainClock.tick(40)
#pygame.quit()
#
#        
#            
#            
#        
#        