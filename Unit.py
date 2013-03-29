import os, sys
import pygame
from math import sin, cos, radians
from pygame.sprite import Sprite
from pygame.locals import *
from pygame.mixer import *
#from Projectile.py import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def load_image_alpha(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message

    image = image.convert_alpha()
    return image, image.get_rect()

def path_rejoin(path):
    return os.path.join(*path.split('/'))

def load_image(name, colorkey = None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message

    image = image.convert()
    if colorkey is not None:
        if colorkey == 01:
            colorkey = image.get_it((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannont load Sound:', fullname
        raise SystemExit, messege
    return sound


class Unit(object):

    def __init__(self, positionX, positionY, side):
        self.side = side
        self.mySprite = pygame.image.load(path_rejoin('data/Tank.gif')).convert()
        self.rect = self.mySprite.get_rect()
        self.positionX = positionX
        self.positionY = positionY
        self.rect.bottomleft = (self.positionX, self.positionY)
        if side == 'Soviet':
            self.health = 100
            self.trajectory = 45
            self.mySprite = pygame.transform.flip(self.mySprite, 1, 0)
        elif side == 'Nazi':
            self.health = 120
            self.trajectory = 45
            #self.mySprite = pygame.transform.flip(self.mySprite, 1, 0)
        self.mySound = load_sound('data/TankFiring.wav')

    def fire(self):
        self.mySound.play()

    def update(self, main):
        #self.rect = self.mySprite.get_rect()
        self.rect.bottomleft = (self.positionX, self.positionY)
        #if self.side == 'Nazi':
        #    self.mySprite = pygame.transform.flip(self.mySprite, 1, 0)
        main.screen.blit(self.mySprite, (self.rect.left, self.rect.top))

    def getRect(self):
        return self.rect

    def getHealth(self):
        return self.health

    def getTrajectory(self):
        return self.trajectory

    def setHealth(self, newHealth):
        self.health = newHealth

    def setTrajectory(self, newTrajectory):
        self.trajectory = newTrajectory

    def rotateUp(self):
        self.trajectory = self.trajectory + 1

    def rotateDown(self):
        self.trajectory = self.trajectory - 1

    def getXPos(self):
        return self.rect.left

    def getYPos(self):
        return self.rect.bottom

    def setXPos(self, newX):
        self.positionX = newX

    def setYPos(self, newY):
        self.positionY = newY

    def moveLeft(self, newY):
        self.positionX = self.positionX-1
        self.positionY = newY

    def moveRight(self, newY):
        self.positionX = self.positionX+1
        self.positionY = newY
        
    def takeDamage(self):
        self.health = self.health-20

    def getSide(self):
        if self.side == 'Nazi':
            return 0
        else:
            return 1
