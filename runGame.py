import os, sys
import pygame
from math import sin, cos, radians
from pygame.sprite import Sprite
from pygame.locals import *
from pygame.mixer import *
from Player import *
from Land import *
from Unit import *
from Projectile import *
from Main import *

if __name__  == "__main__":
    kablibelmofib = Main()
    kablibelmofib.mainLoop()
