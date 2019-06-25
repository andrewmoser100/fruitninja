#########################################
# Programmer: Mr. G
# Date: 07/01/2016
# File Name: sprite_platforms.py
# Description: Demonstrates how to use Sprite platforms to support a Sprite object under gravity
#########################################
import pygame
from random import *
pygame.init()

HEIGHT = 600
WIDTH  = 800
screen=pygame.display.set_mode((WIDTH,HEIGHT))

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
apple=pygame.image.load("apple1.png")
coconut=pygame.image.load("coconut1.png")
lemon=pygame.image.load("lemon1.png")
watermelon=pygame.image.load("watermelon1.png")
bomb_image=pygame.image.load("bomba.png")
live=pygame.image.load("lives.png")
live=pygame.transform.scale(live,(50,50))
totalLives = 3
Test=["apple1.png","coconut1.png","lemon1.png","watermelon1.png"]
FRUITS=[apple,coconut,lemon,watermelon]
FRUIT_names =['APPLE','COCONUT','LEMON','WATERMELON']

GROUND = HEIGHT
GRAVITY = 2
HORI_SPEED = 10
VERT_SPEED = -30
background=pygame.image.load("background.png")
background=pygame.transform.scale(background,(800,600))
intro=pygame.image.load("intro.jpg")
intro=pygame.transform.scale(intro,(800,600))

#---------------------------------------#
#   classes                             #
#---------------------------------------#
class Fruit(pygame.sprite.Sprite):
    """ (fileName)
        Visible game object.
        Inherits Sprite to use its Rect property.
        See Sprite documentation here: 
        http://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
    """
    def __init__(self, picture=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.vx = 10
        self.vy = -30
        self.visible = False
        self.image = pygame.image.load(picture)
        self.image = pygame.transform.scale(self.image, (70,70))
        self.rect = self.image.get_rect()
        self.update()

    def spawn(self, x, y):
        """ Assign coordinates to the center of the object and make it visible.
        """
        self.x = x-self.rect.width/2
        self.y = y-self.rect.height/2
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)
        self.visible = True
        self.update()

    def draw(self, surface):
  #      FRT=FRUITS[self.frt]
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect = pygame.Rect(self.x,self.y,self.rect.width,self.rect.height)
                    
    def move(self, GRAVITY=2):
        self.x = self.x + self.vx
        self.vy = self.vy + GRAVITY
        self.y = self.y + self.vy
        self.update()
        
    def reset(self, GROUND=600):
        self.y = GROUND - self.rect.height
        self.vy= randint (-50,-30)
        self.x = randint (-200,900)       
        self.vx= randint (10,30)
        if self.x>400:
            self.vx*=-1
        self.update()

class Bomb(pygame.sprite.Sprite):

    def __init__(self,bimage="bomba.png"):
        pygame.sprite.Sprite.__init__(self)
        self.bx=0
        self.by=0
        self.bvx=10
        self.bvy=-30
        self.bvisible=False
        self.bimage=pygame.image.load(bimage)
        self.bimage=pygame.transform.scale(self.bimage, (70,70))
        self.bradius=self.bimage.get_rect()
        self.brect = self.bimage.get_rect()

    def spawn(self,bx,by,):
        self.bx=bx-self.brect.width/2
        self.by=by-self.brect.height/2
        self.brect=pygame.Rect(self.bx,self.by,self.brect.width,self.brect.height)
        self.visible=True
        self.bomb_update()

    def draw(self,surface):
        surface.blit(self.bimage,self.brect)

    def bomb_update(self):
        self.brect=pygame.Rect(self.bx,self.by,self.brect.width,self.brect.height)

    def bomb_reset(self, GROUND=600):
        self.by=GROUND-self.brect.height
        self.bvy=randint(-50,-30)
        self.bx=randint(-200,900)
        self.bvx=randint(10,30)
        if self.bx>400:
            self.bvx*=-1
        self.bomb_update()

    def bomb_move(self, bomb_GRAVITY=2):
        self.bx = self.bx + self.bvx
        self.bvy = self.bvy + bomb_GRAVITY
        self.by = self.by + self.bvy
        self.bomb_update()
        
        


#---------------------------------------#
# functions                             #
#---------------------------------------#
def redraw_screen():
    screen.blit(background,(0,0))
    if totalLives == 3:
        screen.blit(live,(600,15))
        screen.blit(live,(650,15))
        screen.blit(live,(700,15))
    elif totalLives == 2:
        screen.blit(live,(650,15))
        screen.blit(live,(700,15))
    elif totalLives == 1:
        screen.blit(live,(700,15))
    fruit.draw(screen)
    bomb.draw(screen)
    pygame.display.update()

def distance(x1,y1,x2,y2): 
    return sqrt((x1-x2)**2+(y1-y2)**2)

def intro_screen():
    screen.blit(intro,(0,0))
    pygame.display.update()
    
                
#---------------------------------------#
# main program starts here              #
#---------------------------------------#
num=randint(1,6)
i = randint(0,3)

fruit=Fruit(Test[i])
bomb=Bomb()
fruit.spawn(randint (50,350),GROUND-fruit.rect.height)
bomb.spawn(randint(50,350),GROUND-bomb.brect.height)
lives=3

#---------------------------------------#
inPlay = 1

while inPlay==1:
    intro_screen()
    for event in pygame.event.get(): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: #If spacebar is pressed start the main game
            inPlay=2

while inPlay == 2:

     
        
    
    
    position=pygame.mouse.get_pos()
    pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        inPlay = False
    bomb.bomb_move()
    fruit.move()

    (mouseX,mouseY)=pygame.mouse.get_pos()
 #   if distance(mouseX,mouseY,self.bx,self.by)<=
    
    if bomb.by<-100 or bomb.by>700:
        bomb=Bomb()
        bomb.spawn(randint (50,350),GROUND-fruit.rect.height)
        bomb.bomb_reset()

    if fruit.y<-100 or fruit.y>700:
        for i in range(3):
            i = randint(0,3)
            fruit=Fruit(Test[i])
            fruit.spawn(randint (50,350),GROUND-fruit.rect.height)
        fruit.reset()

    


    redraw_screen()
    pygame.time.delay(20)
#---------------------------------------# 
pygame.quit()
