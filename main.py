import threading

import pygame
import time
import random

YELLOW = (255, 255, 0)
currentTime = time.time()


##fields for player: x position, y position

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("shipFinal.png").convert()
        self.rect = self.image.get_rect()
        self.movey = 1
        self.nextShot = 0
        self.normalFire = True
        self.spreadPower = False
        self.rapidPower = False

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
    def __init__(self, x, y, rad, xvel, damage):
        print("bullet made")
        self.x = x
        self.y = y
        self.rad = rad
        self.color = YELLOW
        self.xvel = xvel
        self.rect = pygame.Rect(x - rad, y - rad, rad * 2, rad * 2)
        self.damage = damage





class Event(pygame.sprite.Sprite):
    def __init__(self, spreadShot, rapidFire):
        super(Event, self).__init__()
        self.image = pygame.image.load("mysteryBox2.jpg").convert()
        self.spreadShot = spreadShot
        self.rapidFire = rapidFire
        self.rect = self.image.get_rect(center=(1279, random.randint(1, 670)))

    def isSpreadPower(self):
        return self.spreadShot

    def isRapid(self):
        return self.rapidFire


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nextShot = 100000000000
        self.health = 100
        self.image = pygame.image.load("alien1.jpg").convert()
        self.rect = self.image.get_rect(center = (1279, random.randint(1, 670)))





def createEnemies(index):
    randNum = random.randint(1, 100)
    if randNum < index:
        enemies.append(Enemy(1279, random.randint(1, 670)))


def drawEnemies():
    for en in enemies:
        screen.blit(en.image, (en.x, en.y))



def createEvent():
    randNum = random.randint(1, 100)
    if randNum < 10:
        if randNum % 2 == 1:
            events.append(Event(True, False))
            print("spreadshot created")
            return True
        else:
            events.append(Event(False, True))
            print("rapid created")
            return True
    return False


def playerMovement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.moveUp()
    if keys[pygame.K_s]:
        player.moveDown()

    if keys[pygame.K_SPACE] and player.nextShot < time.time_ns():
        if player.spreadPower:
            bullets.append(Bullet(player.rect.x + 51, player.rect.y + 25, 20, 10, 50))
        else:
            bullets.append(Bullet(player.rect.x + 51, player.rect.y + 25, 5, 10, 25))
        if not player.rapidPower:
            player.nextShot = time.time_ns() + 1000000000 / 2
        else:
            player.nextShot = time.time_ns() + 10000000


def isOffScreen(x, y):
    if x < 0 or x > 1280 or y < 0 or y > 720:
        return True
    else:
        return False


def drawEvents(events):
    for e in events:
        screen.blit(e.image, e.rect)
        print("event drawing")
        e.rect.x += -1
        if e.rect.colliderect(player.rect):
            if e.spreadShot:
                if not player.spreadPower:
                    player.spreadPower = True
                    player.rapidPower = False
                else:
                    player.spreadPower = False
                    player.rapidPower = False
            elif e.rapidFire:
                if not player.rapidPower:
                    player.spreadPower = False
                    player.rapidPower = True
                else:
                    player.rapidPower = False
                    player.spreadPower = False
            events.remove(e)
        if isOffScreen(e.rect.x, e.rect.y):
            events.remove(e)
            print("event removed")


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
fpsClock = pygame.time.Clock()
worldx = 1280
worldy = 720
screen = pygame.display.set_mode((worldx, worldy))
gameOver = False
grav = 1
backdrop = pygame.image.load("spaceFinal.jpg").convert()
nextTimeEvent = 0

player = Player()
player.rect.x = 50
player.rect.y = 320
i = 0
bullets = []
events = []
enemies = []
enemyBullet = []

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
    if nextTimeEvent < time.time():
        if createEvent():
            nextTimeEvent = time.time() + 20
    drawEvents(events)
    createEnemies(5)


    pygame.display.flip()