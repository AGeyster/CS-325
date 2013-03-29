import os, sys
import pygame, math
from pygame.sprite import Sprite
from pygame.locals import *
from pygame.mixer import *

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

class Projectile(Sprite):
    #angle = 180 #degrees
    #self.firingSound = load_sound('data/TankFiring.wav')
    image = None

    def __init__(self, tank, ground, target):
        self.speedX = 0.0
        self.speedY = 0.0
        self.posX = 0
        self.posY = 0
        self.firingTank = tank
        self.targetTank = target
        self.mySprite = pygame.image.load(path_rejoin('data/tankShell.gif')).convert()
        self.rect = self.mySprite.get_rect()
        if Projectile.image is None:
            Projectile.image = self.mySprite
        if self.firingTank.getSide() == 0: #Nazi Firing
            print self.firingTank.getTrajectory()
            self.rect.center = self.firingTank.getRect().topright
            self.speedX = math.sin(math.radians(90-self.firingTank.getTrajectory())) * (float(10))#will be later replaced with adjustable power
            self.speedY = (0-math.cos(math.radians(90-self.firingTank.getTrajectory()))) * (float(5))#will be replaced with adjstable power
        elif self.firingTank.getSide() == 1: #Soviet firing
            print self.firingTank.getTrajectory()
            self.rect.center = self.firingTank.getRect().topleft
            self.speedX = (0-math.sin(math.radians(90-self.firingTank.getTrajectory()))) * float(10)#will be replaced with adjustable power
            self.speedY = (0-math.cos(math.radians(90-self.firingTank.getTrajectory()))) * float(5)#will be replaced with adjustable power
        self.posX = self.rect.centerx
        self.posY = self.rect.centery
        print "end of projectile init"

    def update(self, Main):
        self.posX = self.posX + self.speedX
        self.posY = self.posY + self.speedY
        if self.posX > 1024 or self.posX < 200:
            Main.endShot()
        elif self.posY > 768:
            Main.endShot()
        elif self.posY == 0:
            Main.endShot()
        self.rect.centerx = int(self.posX)
        self.rect.centery = int(self.posY)
        self.speedY = self.speedY + (.2)
        if self.speedY > 7.0:
            self.speedY = 7
        if int(self.posY) >= (768-Main.ground[int(self.posX)-200]):
            print "bullet in ground"
            Main.endShot()
            Main.destroyTerrain(self.posX)
        if  self.firingTank.getRect().collidepoint(int(self.posX), int(self.posY)):
            Main.endShot()
            Main.destroyTerrain(self.posX)
            Main.damageTank(self.posX)
        elif self.targetTank.getRect().collidepoint(int(self.posX), int(self.posY)):
            Main.endShot()
            Main.destroyTerrain(self.posX)
            Main.damageTank(self.posX)
        Main.screen.blit(self.mySprite, (self.posX, self.posY))
        #print "updating bullet"
    
        
            
        
    
