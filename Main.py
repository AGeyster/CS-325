import os, sys
import pygame
from math import sin, cos, radians
from pygame.sprite import Sprite
from pygame.locals import *
from pygame.mixer import *
from pygame.font import *
from Player import *
from Land import *
from Unit import *
from Projectile import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

#screen = pygame.display.set_mode((1424,768))

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

class Main(object):
    
    def __init__(self):
        self.screen = pygame.display.set_mode((1224, 768), pygame.FULLSCREEN)
        pygame.init()
        #self.screen = pygame.display.set_mode((1424, 768))
        pygame.display.set_caption('Scorched Europa')
        pygame.mouse.set_visible(0)
        self.currentTurn = 0
        self.timeRemaining = 30
        self.clockCounter = 0
        self.isFiring = 0
        self.myFont = pygame.font.SysFont("monospace", 15)
        self.labelNazi = self.myFont.render("Current Turn: Nazi", 1, (255, 255, 0))
        self.labelSoviet = self.myFont.render("Current Turn: Soviet", 1, (255, 255, 0))
        #self.labelTimer = self.myFont.render(('Time Remaining: %d', self.timeRemaining), 1, (255,255,0))
        self.infoLabel = self.myFont.render("Time per Turn: 30 seconds", 1, (255, 255, 0))
        self.clock = pygame.time.Clock()
        self.ground = initialize()
        self.leftFlag = pygame.image.load(path_rejoin('data/NaziFlag.gif')).convert()
        self.rightFlag = pygame.image.load(path_rejoin('data/SovietFlag.gif')).convert()
        self.background = pygame.image.load(path_rejoin('data/Mountains.gif')).convert()
        self.myUnit = Unit(247,768-self.ground[47], 'Nazi')
        self.myUnitTwo = Unit(950, 768-self.ground[750], 'Soviet')
        self.projectileHolder = Projectile(self.myUnit, self.ground, self.myUnitTwo)
        self.screen.blit(self.background, (200,0))
        self.screen.blit(self.leftFlag, (0,0))
        self.screen.blit(self.rightFlag, (1024, 0))
        if self.currentTurn == 0:
            self.screen.blit(self.labelNazi, (200, 0))
        elif self.currentTurn == 1:
            self.screen.blit(self.labelSoviet, (200, 0))
        self.screen.blit(self.infoLabel, (200, 20))
        drawGround(self)
        pygame.display.flip()
        self.state = 'IN_GAME'

    def updateBackground(self):
        self.screen.blit(self.background, (200,0))
        self.screen.blit(self.leftFlag, (0,0))
        self.screen.blit(self.rightFlag, (1224, 0))
        drawGround(self)
        if self.currentTurn == 0:
            self.screen.blit(self.labelNazi, (200, 0))
        elif self.currentTurn == 1:
            self.screen.blit(self.labelSoviet, (200, 0))
        self.screen.blit(self.infoLabel, (200, 20))
        self.myUnit.update(self)
        self.myUnitTwo.update(self)
        pygame.display.flip()

    def endShot(self):
        self.isFiring = 0

    def destroyTerrain(self, hitPositionUnadjusted):
        adjustedPosition = int(hitPositionUnadjusted-200)
        counter = 1
        while counter <=14:
            if adjustedPosition-counter >= 0 and adjustedPosition-counter <= 823:
                self.ground[adjustedPosition-counter] = self.ground[adjustedPosition-counter]-15+counter
            counter = counter + 1
        counter = 1
        while counter <=14:
            if adjustedPosition+counter >= 0 and adjustedPosition+counter <= 823:
                self.ground[adjustedPosition+counter] = self.ground[adjustedPosition+counter]-15+counter
            counter = counter + 1
        if adjustedPosition >= 0 and adjustedPosition <= 823:
            self.ground[adjustedPosition] = self.ground[adjustedPosition]-15
        print "destroying terain"

    def damageTank(self, hitPosition):
        if self.myUnit.getXPos()+self.myUnit.getRect().width > hitPosition and self.myUnit.getXPos()-self.myUnit.getRect().width < hitPosition:
            self.myUnit.takeDamage()
            print "Nazi was hit"
        elif self.myUnitTwo.getXPos()+self.myUnitTwo.getRect().width > hitPosition and self.myUnitTwo.getXPos()-self.myUnitTwo.getRect().width < hitPosition:
            self.myUnitTwo.takeDamage()
            print "Soviet was hit"

    def mainLoop(self):
        keepGoing = True
        while keepGoing:
            self.clock.tick(60)
            if self.state == 'IN_GAME':
                self.checkInput()
                #self.updateBackground()
                #pygame.display.flip()
                
    def checkInput(self):
        #currentTurn = 0
        #clockCounter = 0
        tempHolder = 0
        #isFiring = False
        for event in pygame.event.get():
            #self.myUnit.update(self)
            #self.myUnitTwo.update(self)
            #pygame.display.flip()
            if self.myUnit.getHealth() == 0:
                winLabel = self.myFont.render("Winner: Soviets's!", 1, (255, 255, 0))
                self.updateBackground()
                self.myUnit.update(self)
                self.myUnitTwo.update(self)
                self.screen.blit(winLabel, (612, 0))
                pygame.display.flip()
                pygame.time.delay(5000)
                exit(0)
            elif self.myUnitTwo.getHealth() == 1:
                winLabel = self.myFont.render("Winner: Nazi's!", 1, (255, 255, 0))
                self.updateBackground()
                self.myUnit.update(self)
                self.myUnitTwo.update(self)
                self.screen.blit(winLabel, (612, 0))
                pygame.display.flip()
                pygame.time.delay(5000)
                exit(0)
            elif self.isFiring == 1:
                self.timeRemaining = 30
                self.clockCounter = 0
            elif event.type == QUIT:
                exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                exit(0)
            elif event.type == KEYDOWN and event.key == K_t:
                #pygame.display.toggle_fullscreen()
                self.myUnit.setHealth(0)
            elif event.type == KEYDOWN and event.key == K_RETURN and self.currentTurn == 0:
                self.myUnit.fire()#Nazi Fire Event
                self.currentTurn = 1
                self.timeRemaining = 30
                #self.label = self.myFont.render("Current Turn: Soviet", 1, (255, 255, 0))
                print "Turnover"
                self.clockCounter = 0
                self.isFiring = 1
                self.projectileHolder = Projectile(self.myUnit, self.ground, self.myUnitTwo)
            elif event.type == KEYDOWN and event.key == K_RETURN and self.currentTurn == 1:
                self.myUnitTwo.fire()#soviet fire event
                self.currentTurn = 0
                self.timeRemaining = 30
                #self.label = self.myFont.render("Current Turn: Nazi", 1, (255, 255, 0))
                print "Turnover"
                self.clockCounter = 0
                self.isFiring = 1
                self.projectileHolder = Projectile(self.myUnitTwo, self.ground, self.myUnit)
            elif event.type == KEYDOWN and event.key == K_UP and self.currentTurn == 0:
                self.myUnit.rotateUp()
                print "rotating"
            elif event.type == KEYDOWN and event.key == K_DOWN and self.currentTurn == 0:
                self.myUnit.rotateDown()
                print "rotating"
            elif event.type == KEYDOWN and event.key == K_UP and self.currentTurn == 1:
                self.myUnitTwo.rotateUp()
                print "rotating"
            elif event.type == KEYDOWN and event.key == K_DOWN and self.currentTurn == 1:
                self.myUnitTwo.rotateDown()
                print "rotating"
            elif event.type == KEYDOWN and event.key == K_LEFT and self.currentTurn == 0:
                if self.myUnit.getXPos()-200 == 0:
                    pass
                else:
                    tempHolder = 768-self.ground[(self.myUnit.getXPos()-201)]
                    self.myUnit.moveLeft(tempHolder)
            elif event.type == KEYDOWN and event.key == K_RIGHT and self.currentTurn == 0:
                if self.myUnit.getXPos()-200 == 823:
                    pass
                else:
                    tempHolder = 768-self.ground[(self.myUnit.getXPos()-199)]
                    self.myUnit.moveRight(tempHolder)
            elif event.type == KEYDOWN and event.key == K_LEFT and self.currentTurn == 1:
                if self.myUnitTwo.getXPos()-200 == 0:
                    pass
                else:
                    tempHolder = 768-self.ground[(self.myUnitTwo.getXPos()-201)]
                    self.myUnitTwo.moveLeft(tempHolder)
            elif event.type == KEYDOWN and event.key == K_RIGHT and self.currentTurn == 1:
                if self.myUnitTwo.getXPos()-200 == 823:
                    pass
                else:
                    tempHolder = 768-self.ground[(self.myUnitTwo.getXPos()-199)]
                    self.myUnitTwo.moveRight(tempHolder)

            self.updateBackground()
            self.myUnit.update(self)
            self.myUnitTwo.update(self)
            #print "isFiring"
            #print self.isFiring
            if self.isFiring == 1:
                self.projectileHolder.update(self)
            pygame.display.flip()
            self.clock.tick(47)
            if ((self.clockCounter+1) > 1410):
                self.clockCounter = 0
                if self.currentTurn == 0:
                    self.currentTurn = 1
                    self.timeRemaining = 30
                    #self.label = self.myFont.render("Current Turn: Soviet", 1, (255, 255, 0))
                    print "Turnover"
                elif True:
                    self.currentTurn = 0
                    self.timeRemaining = 30
                    #self.label = self.myFont.render("Current Turn: Nazi", 1, (255, 255, 0))
                    print "Turnover"
            elif (self.clockCounter < 1410):
                self.clockCounter = self.clockCounter + 1
            if (math.fmod(self.clockCounter, 47) == 0) & (self.clockCounter != 0 & self.clockCounter != 1410):
                self.timeRemaining = self.timeRemaining - 1
            print self.clockCounter
            print self.timeRemaining
            

            
    
