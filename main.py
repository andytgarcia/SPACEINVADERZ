import pygame
import time
import random

YELLOW = (255, 255, 0)

##fields for player: x position, y position

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("shipFinal.png").convert()
        self.rect = self.image.get_rect()
        self.movey = 1
        self.nextShot = 0

    def moveUp(self):
        if self.rect.y == 0:
            self.rect.y -= 0
        else:
            self.rect.y -= self.movey

    def moveDown(self):
        if self.rect.y == (720 - 50):
            self.rect.y += 0
        else:
            self.rect.y += self.movey
            print(self.rect.y)


class Bullet:
    def __init__(self, x, y, rad, xvel):
        print("bullet made")
        self.x = x
        self.y = y
        self.rad = rad
        self.color = YELLOW
        self.xvel = xvel


class Event(pygame.sprite.Sprite):
    def __init__(self, spreadShot, rapidFire, tripleBurst):
        super(Event, self).__init__()
        self.image = pygame.image.load("mystery.png").convert()
        self.spreadShot = spreadShot
        self.rapidFire = rapidFire
        self.tripleBurst = tripleBurst
        self.rect = self.image.get_rect()



def createEvent():
    randNum = random.randrange(0, 100, 1)
    if randNum < 20:
        if randNum % 3 == 0:
            events.append(Event(True, False, False))
        elif randNum % 2 == 0:
            events.append(Event(False, False, True))
        else:
            events.append(Event(False, True, False))


def playerMovement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.moveUp()
    if keys[pygame.K_s]:
        player.moveDown()

    if keys[pygame.K_SPACE] and player.nextShot < time.time_ns():
        bullets.append(Bullet(player.rect.x + 51, player.rect.y + 25, 5, 10))
        player.nextShot = time.time_ns() + 1000000000/2


def isOffScreen(x, y):
    if x < 0 or x > 1280 or y < 0 or y > 720:
        return True
    else:
        return False


def handleBullets():
    for b in bullets:
        pygame.draw.circle(screen, b.color, (b.x, b.y), b.rad, 0)
        b.x += b.xvel
        if isOffScreen(b.x, b.y):
            bullets.remove(b)
            print("bullet removed")


def clearScreen():
    pygame.draw.rect(screen, pygame.Color(0, 0, 0), (0, 0, 1280, 720))


# start of program
pygame.init()  # start engine
FPS = 60  # 60 frames per second
fpsClock = pygame.time.Clock
worldx = 1280
worldy = 720
screen = pygame.display.set_mode((worldx, worldy))
gameOver = False
grav = 1
backdrop = pygame.image.load("spaceFinal.jpg").convert()

player = Player()
player.rect.x = 50
player.rect.y = 320
i = 0
bullets = []
events = []

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    clearScreen()
    screen.blit(backdrop, [i, 0])
    screen.blit(backdrop, [worldx + i, 0])
    if i == -worldx:
        screen.blit(backdrop, [worldx + i, 0])
        i = 0
    i -= 1
    screen.blit(player.image, player.rect)
    playerMovement()
    handleBullets()

    pygame.display.flip()
