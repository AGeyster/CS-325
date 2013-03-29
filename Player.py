import os, sys
import pygame
from math import sin, cos, radians
from pygame.sprite import Sprite
from pygame.locals import *
from pygame.mixer import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Player(Sprite):

    #units

    def __init__(side):
        units = {}
        unit1;
        unit2;
        unit3;
        unit4;
        if(side == 'Nazi'):
            unit1 = Unit('Nazi')
            unit2 = Unit('Nazi')
            unit3 = Unit('Nazi')
            unit4 = Unit('Nazi')
            units.append(unit1)
            units.append(unit2)
            units.append(unit3)
            units.append(unit4)
        elif(side == 'Soviet'):
            unit1 = Unit('Soviet')
            unit2 = Unit('Soviet')
            unit3 = Unit('Soviet')
            unit4 = Unit('Soviet')
            units.append(unit1)
            units.append(unit2)
            units.append(unit3)
            units.append(unit4)
        
