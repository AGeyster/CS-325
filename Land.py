import os, sys
import pygame
import random
import math
from math import sin, cos, radians
from pygame.sprite import Sprite
from pygame.locals import *
from pygame.mixer import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


def initialize():
    groundColumns = {}
    i = 0
    while i < 824:
        landValue = random.randrange(0, 412)
        if i == 0:
            pass
        elif (landValue < (groundColumns[(i-1)] - 5)):
            landValue = groundColumns[(i-1)] - 5
        elif (landValue > (groundColumns[(i-1)] + 5)):
            landValue = groundColumns[(i-1)] + 5
        if landValue >= 412:
            landValue = 412
        if landValue <= 0:
            landValue = 0
	groundColumns[i] = landValue
        i += 1
    return groundColumns
	   
def drawGround(Main):
    surface = Main.screen
    ground = Main.ground
    for i in range(0, 824):
	pygame.draw.line(surface, (0, 255, 0), (i+200, 768), (i+200, 768-ground[i]))
        
                            
