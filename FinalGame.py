'''
-------------------------------------------------------------------------------
Name:		UNFAIR_FRUIT_NINJA.py
Purpose:	MAKE FRUIT NINJA
Author:		Moser.A

Created:	1/06/2019
------------------------------------------------------------------------------
'''

import pygame
from random import *

pygame.init()

HEIGHT = 600
WIDTH = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

apple = pygame.image.load("apple1.png")
apple2 = pygame.image.load("apple2.png")
apple2 = pygame.transform.scale(apple2, (70, 70))

coconut = pygame.image.load("coconut1.png")
coconut2 = pygame.image.load("coconut2.png")
coconut2 = pygame.transform.scale(coconut2, (70, 70))

lemon = pygame.image.load("lemon1.png")
lemon2 = pygame.image.load("lemon2.png")
lemon2 = pygame.transform.scale(lemon2, (70, 70))

watermelon = pygame.image.load("watermelon1.png")
watermelon2 = pygame.image.load("watermelon2.png")
watermelon2 = pygame.transform.scale(watermelon2, (70, 70))

bomb_image = pygame.image.load("bomba.png")
live = pygame.image.load("lives.png")
live = pygame.transform.scale(live, (50, 50))
diamond = pygame.image.load("MouseIcon.png")
diamond = pygame.transform.scale(diamond, (25, 25))
ximage = pygame.image.load("X.png")
ximage = pygame.transform.scale(ximage, (50, 50))
explosion = pygame.image.load("Explosion/exp1.png")

# Loads sprites for the explosion
for i in range(1, 16):
    explosion = []
    image = 'explosion/exp' + str(i) + '.png'
    explosion.append(pygame.image.load(image))

# scale all the sprites to a specific size
for i in range(len(explosion)):
    explosion[i] = pygame.transform.scale(explosion[i], (75, 75))

totalLives = 3
score = 0
# Spawning Bombs when true
bombing = False
# Spawning another fruit
levelUp = False

# Fonts
font = pygame.font.Font("Never Surrender.ttf", 30)
font2 = pygame.font.Font("arcade.ttf", 30)
font3 = pygame.font.Font("Cooper Black.ttf", 25)
font4 = pygame.font.Font("arcade.ttf", 35)

Test = ["apple1.png", "coconut1.png", "lemon1.png", "watermelon1.png"]
FRUITS = [apple, coconut, lemon, watermelon]
FRUIT_names = ['APPLE', 'COCONUT', 'LEMON', 'WATERMELON']
# Sound effect that goes off when you swipe through a fruit
swipe = pygame.mixer.Sound("swipe.wav")

GROUND = HEIGHT
GRAVITY = 2
# Speed that Fruit will move
HORI_SPEED = 10
VERT_SPEED = -30

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (800, 600))
intro = pygame.image.load("intro.jpg")
intro = pygame.transform.scale(intro, (800, 600))
outro = pygame.image.load("outro.jpg")
outro = pygame.transform.scale(outro, (800, 600))


# ---------------------------------------#
#  classes                               #
# ---------------------------------------#
class Fruit(pygame.sprite.Sprite):
    """
    Class that draws the fruit
    Visible game object.
    """

    def __init__(self, picture=None):
        """
        :param picture: None
        """
        pygame.sprite.Sprite.__init__(self)

        # Fruits coordinates
        self.x = 0
        self.y = 0
        # Velocities of fruit
        self.vx = 10
        self.vy = -30

        self.visible = False
        self.picture = picture
        self.image = pygame.image.load(picture)
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.update()

    def spawn(self, x, y):
        """
         Function used to spawn the fruit
        :param x: x coordinates for the fruit
        :param y: y coordinates for the fruit
        :return: None
        """

        # Starting coordinates then fruit is drawn
        self.x = x - self.rect.width / 2
        self.y = y - self.rect.height / 2
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)
        self.visible = True
        self.update()

    def draw(self, surface):
        """
        Function to draw the fruit
        :param surface:
        :return: None
        """
        surface.blit(self.image, self.rect)

    def update(self):
        """
        Function redraws the fruit based on its coordinates
        :return: None
        """
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)


    def move(self, GRAVITY=2):
        """
        Function that moves the fruit based on Gravity
        :param GRAVITY: = 2
        :return: None
        """
        self.x = self.x + self.vx
        self.vy = self.vy + GRAVITY
        self.y = self.y + self.vy
        self.update()

    def reset(self, GROUND=600):
        """
        Resets the fruit when it goes out of the screen
        :param GROUND: 600
        :return: None
        """
        self.y = GROUND - self.rect.height
        self.vy = randint(-50, -30)
        self.x = randint(-200, 900)
        self.vx = randint(10, 30)
        if self.x > 400:
            self.vx *= -1
        self.update()

    def mouse_strike(self, x, y):
        """
        Checks if the mouse goes over the fruit
        :param x: x coordinate of fruit subtract screens x cooridnate
        :param y: y coordinate of fruit subtract screens y cooridnate
        :return: Sliced Fruit
        """
        return (0 <= (x - self.x) <= 70 and 0 <= (y - self.y) <= 70)


class Bomb(pygame.sprite.Sprite):
    """
       Class that draws the bomb
       Visible game object.
    """

    def __init__(self, bimage="bomba.png"):
        """
        :param bimage: Load Bomb image
        """
        pygame.sprite.Sprite.__init__(self)

        self.bx = 0
        self.by = 0
        self.bvx = 10
        self.bvy = -30
        self.bvisible = False
        self.bimage = pygame.image.load(bimage)
        self.bimage = pygame.transform.scale(self.bimage, (70, 70))
        self.bradius = self.bimage.get_rect()
        self.brect = self.bimage.get_rect()

    def spawn(self, bx, by, ):
        """
        Function used to spawn the bomb
        :param bx: bx coordinates for the bomb
        :param by: by coordinates for the bomb
        :return: None
        """
        self.bx = bx - self.brect.width / 2
        self.by = by - self.brect.height / 2
        self.brect = pygame.Rect(self.bx, self.by, self.brect.width, self.brect.height)
        self.bvisible = True
        self.bomb_update()

    def draw(self, surface):
        """
        Showing bomb on screen
        :param surface: screen
        :return: None
        """
        surface.blit(self.bimage, self.brect)

    def bomb_update(self):
        """
        Sets bomb into rectangle image on screen
        :return: None
        """
        self.brect = pygame.Rect(self.bx, self.by, self.brect.width, self.brect.height)

    def bomb_explode(self, screen, explosions):
        """
        Function to make the bomb "explode" adds the sprite
        :param screen: Whats being updated
        :param explosions: Sprite from i list
        :return: None
        """
        for i in range(len(explosions)):
            screen.blit(explosions[i], (bomb.bx, bomb.by))
            pygame.display.update()
            pygame.time.delay(10)

    def bomb_reset(self, GROUND=600):
        """
        Bomb resets
        :param GROUND: 600
        :return: None
        """
        self.by = GROUND - self.brect.height
        self.bvy = randint(-50, -30)
        self.bx = randint(-200, 900)
        self.bvx = randint(10, 30)
        if self.bx > 400:
            self.bvx *= -1
        self.bomb_update()

    def mouse_strike(self, x, y):
        """
        Checks if the mouse goes over the bomb
        :param x: x coordinate of fruit subtract screens x cooridnate
        :param y: y coordinate of fruit subtract screens y cooridnate
        :return: Sliced Bomb
        """
        return (0 <= (x - self.bx) <= 70 and 0 <= (y - self.by) <= 70)

    def bomb_move(self, bomb_GRAVITY=2):
        """
        Function that moves bomb
        :param bomb_GRAVITY: 2
        :return: None
        """
        self.bx = self.bx + self.bvx
        self.bvy = self.bvy + bomb_GRAVITY
        self.by = self.by + self.bvy
        self.bomb_update()


# ---------------------------------------#
# functions                             #
# ---------------------------------------#
def redraw_screen():
    """
    Sets background and removes lives
    :return: None
    """
    screen.blit(background, (0, 0))
    if totalLives == 3:
        screen.blit(live, (600, 15))
        screen.blit(live, (650, 15))
        screen.blit(live, (700, 15))
    elif totalLives == 2:
        screen.blit(ximage, (600, 15))
        screen.blit(live, (650, 15))
        screen.blit(live, (700, 15))
    elif totalLives == 1:
        screen.blit(ximage, (600, 15))
        screen.blit(ximage, (650, 15))
        screen.blit(live, (700, 15))

    pygame.mouse.set_visible(False)
    (diamondX, diamondY) = pygame.mouse.get_pos()
    screen.blit(diamond, (diamondX - 10, diamondY - 5))

    # Score
    score_text = font.render("Score:" + str(score), 1, WHITE)
    screen.blit(score_text, (50, 15))
    fruit.draw(screen)
    # Draws bombs on screen
    if bombing:
        bomb.draw(screen)
    if levelUp:
        secondFruit.draw(screen)
    pygame.display.update()

def intro_screen(font_clr=False, font2_clr=False, font3_clr=False):
    """
    # Function for the intro screen, font clr is used to change the text color from white to black
    :param font_clr: PLAY
    :param font2_clr: HELP
    :param font3_clr: QUIT
    :return: None
    """
    (IMouseX, IMouseY) = pygame.mouse.get_pos()
    screen.blit(intro, (0, 0))
    (clickX, clickY) = pygame.mouse.get_pos()
    if not font_clr:
        play_text = font2.render("PLAY", 1, WHITE)
    else:
        play_text = font2.render("PLAY", 1, BLACK)
    if not font2_clr:
        instructions_text = font2.render("HELP", 1, WHITE)
    else:
        instructions_text = font2.render("HELP", 1, BLACK)
    if not font3_clr:
        quit_text = font2.render("QUIT", 1, WHITE)
    else:
        quit_text = font2.render("QUIT", 1, BLACK)

    screen.blit(play_text, (420, 20))
    screen.blit(instructions_text, (550, 20))
    screen.blit(quit_text, (680, 20))
    pygame.display.update()


def help_screen(font4_clr=False):
    """
    Function for within help screen
    :param font4_clr: Shows text within help
    :return: None
    """
    (HMouseX, HMouseY) = pygame.mouse.get_pos()
    screen.blit(background, (0, 0))
    help1 = font4.render("HELP", 1, WHITE)
    help2 = font3.render("1. Use your mouse to swipe through the fruits", 1, WHITE)
    help3 = font3.render("2. Avoid bombs or you will lose a life", 1, WHITE)
    help4 = font3.render("3. If you do not swipe the fruit and it leaves the screen", 1, WHITE)
    help5 = font3.render("    you will lose a life", 1, WHITE)
    if not font4_clr:
        playgame = font2.render("PLAY", 1, WHITE)
    else:
        playgame = font2.render("PLAY", 1, BLACK)

    screen.blit(playgame, (600, 550))
    screen.blit(help2, (50, 150))
    screen.blit(help1, (340, 10))
    screen.blit(help3, (50, 200))
    screen.blit(help4, (50, 250))
    screen.blit(help5, (50, 275))
    pygame.display.update()


def outro_screen():
    """
    Outro screen
    :return: None
    """
    screen.blit(outro, (0, 0))
    pygame.display.update()
    pygame.time.delay(20)
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            pygame.display.update()
            pygame.quit()


# ---------------------------------------#
# main program starts here              #
# ---------------------------------------#

# Randomize Fruit Spawn
num = randint(1, 6)
i = randint(0, 3)
j = randint(0, 3)
bomb = Bomb()
fruit = Fruit(Test[i])
fruit.spawn(randint(50, 350), GROUND - fruit.rect.height)
secondFruit = Fruit(Test[j])
secondFruit.spawn(randint(50, 350), GROUND - secondFruit.rect.height)


inPlay = 1

# While inPlay=1 intro screen is played
while inPlay == 1:

    # Finds mouse position and changes inPlay value if clicked
    (mx, my) = pygame.mouse.get_pos()
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 420 < mx < 530 and 20 < my < 50:
                inPlay = 3
            if 550 < mx < 640 and 20 < my < 50:
                inPlay = 2
            if 680 < mx < 790 and 20 < my < 50:
                inPlay = 4

    #  If mouse over these coordinates text color changes
    if 420 < mx < 530 and 20 < my < 50:
        msg_clr = True
    else:
        msg_clr = False
    if 550 < mx < 665 and 20 < my < 50:
        msg2_clr = True
    else:
        msg2_clr = False
    if 680 < mx < 790 and 20 < my < 50:
        msg3_clr = True
    else:
        msg3_clr = False

    # Runs into screen
    intro_screen(msg_clr, msg2_clr,msg3_clr)

# Within help screen Inplay = 2 and gets mouse position
while inPlay == 2:
    (hx, hy) = pygame.mouse.get_pos()
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 600 < hx < 720 and 550 < hy < 580:
                inPlay = 3

    # If clicked inPlay value changes
    if 600 < hx < 720 and 550 < hy < 580:
        msg4_clr = True
    else:
        msg4_clr = False
    help_screen(msg4_clr)

# The inPlay = 3 in the actual game
while inPlay == 3:
    position = pygame.mouse.get_pos()
    pygame.event.get()
    keys = pygame.key.get_pressed()

    # Moves fruit and bomb
    if keys[pygame.K_ESCAPE]:
        inPlay = False
    fruit.move()
    bomb.bomb_move()

    # If bomb hit life lost, explosion or bomb goes off screen
    (mouseX, mouseY) = pygame.mouse.get_pos()
    if bomb.mouse_strike(mouseX, mouseY):
        totalLives -= 1
        bomb.bomb_explode(screen, explosion)
        bomb.by = 2000

    # Uses the fruit strike function to see if mouseX and mouseY go over the fruit and changes score
    if fruit.mouse_strike(mouseX, mouseY) and fruit.visible == True:
        score += 100

        # Checks if any of the fruits are the following
        if fruit.picture == 'apple1.png':
            fruit.image = apple2
        elif fruit.picture == 'watermelon1.png':
            fruit.image = watermelon2
        elif fruit.picture == 'lemon1.png':
            fruit.image = lemon2
        elif fruit.picture == 'coconut1.png':
            fruit.image = coconut2

        # Plays the swipe sound effect and changes score
        swipe.play()
        fruit.visible = False

    # If score equals 400 then bombs spawn
    if score > 400:
        bombing = True

        # If the bombs y coordinate is between these two numbers the bomb will spawn and will reset
        if bomb.by < -100 or bomb.by > 700:
            bomb.spawn(randint(50, 350), GROUND - fruit.rect.height)
            bomb.bomb_reset()

    # If the fruits y coordinate is between these two points
    if fruit.y < -100 or fruit.y > 700:
        i = randint(0, 3)
        j = randint(0, 3)

        # Calling on fruit class changing the fruits that spawn
        secondFruit = Fruit(Test[j])
        fruit = Fruit(Test[i])

        # Spawns and resets fruits
        secondFruit.spawn(randint(50, 350), GROUND - secondFruit.rect.height)
        fruit.spawn(randint(50, 350), GROUND - fruit.rect.height)
        fruit.reset()
        secondFruit.reset()

        # Checks to see if the fruit goes off the screen without being sliced and removes life
    if (fruit.x < -10 or fruit.x > 810 or fruit.y > 600) and fruit.visible and fruit.vy > 0:
        totalLives -= 1

        # Resets fruits as long as lives dont equal zero
        if totalLives != 0:
            fruit.reset()

    # Score greater than 600 level up activated and second fruit spawns
    if score > 600:
        levelUp = True
        secondFruit.move()

        # Checks to see if the mouse goes through the fruit and increases score
        if secondFruit.mouse_strike(mouseX, mouseY) and secondFruit.visible == True:
            score += 100

            # Checks if any of the fruits are the following
            if secondFruit.picture == 'apple1.png':
                secondFruit.image = apple2
            elif secondFruit.picture == 'watermelon1.png':
                secondFruit.image = watermelon2
            elif secondFruit.picture == 'lemon1.png':
                secondFruit.image = lemon2
            elif secondFruit.picture == 'coconut1.png':
                secondFruit.image = coconut2

            # Plays the swipe sound effect and changes score
            swipe.play()
            secondFruit.visible = False

        # If the fruits y coordinate is between these two positions
        if secondFruit.y < -100 or secondFruit.y > 700:
            j = randint(0, 3)
            secondFruit = Fruit(Test[j])

            # Spawns and resets the second fruit
            secondFruit.spawn(randint(50, 350), GROUND - secondFruit.rect.height)
            secondFruit.reset()

        # Checks  if the second fruit goes off the screen without being sliced and life lost
        if (secondFruit.x < -10 or secondFruit.x > 810 or secondFruit.y > 600)\
                and secondFruit.visible and secondFruit.vy > 0:
            totalLives -= 1
            if totalLives != 0:
                secondFruit.reset()

    # Checks if lives equals zero
    if totalLives == 0:
        inPlay = 4
    redraw_screen()
    pygame.time.delay(25)

# While inPlay equals to four it will display the outro screen
while inPlay == 4:
    outro_screen()

pygame.quit()

