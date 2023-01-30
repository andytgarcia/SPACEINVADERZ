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
        self.spreadPower = False
        self.rapidPower = False
        self.triplePower = False

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
        self.rect = pygame.Rect(x - rad, y - rad, rad * 2, rad * 2)

class Event(pygame.sprite.Sprite):
    def __init__(self, spreadShot, rapidFire, tripleBurst):
        super(Event, self).__init__()
        self.image = pygame.image.load("mysteryBox2.jpg").convert()
        self.spreadShot = spreadShot
        self.rapidFire = rapidFire
        self.tripleBurst = tripleBurst
        self.rect = self.image.get_rect(center = (1279, random.randint(1, 670)))

    def isSpreadPower(self):
        return self.spreadShot

    def isRapid(self):
        return self.rapidFire

    def isTriple(self):
        return self.tripleBurst


def createEvent():
    randNum = random.randint(1, 100)
    if randNum < 20:
        if randNum % 3 == 0:
            events.append(Event(True, False, False))
            print("spreadshot created")
            return True

        elif randNum % 2 == 0:
            events.append(Event(False, False, True))
            print("event created")
            return True

        else:
            events.append(Event(False, True, False))
            print("event created")
            return True
    return False


def playerMovement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.moveUp()
    if keys[pygame.K_s]:
        player.moveDown()

    if keys[pygame.K_SPACE] and player.nextShot < time.time_ns():
        bullets.append(Bullet(player.rect.x + 51, player.rect.y + 25, 5, 10))
        if not player.rapidPower:
            player.nextShot = time.time_ns() + 1000000000 / 2








def isOffScreen(x, y):
    if x < 0 or x > 1280 or y < 0 or y > 720:
        return True
    else:
        return False


def drawEvents():
    for e in events:
        screen.blit(e.image, e.rect)
        print("event drawn")
        e.rect.x += -1
        if e.rect.colliderect(player.rect):
            if e.isSpreadPower:
                player.spreadPower = True
                player.rapidPower = False
                player.triplePower = False
            elif e.isRapid:
                player.rapidPower = True
                player.spreadPower = False
                player.triplePower = False
            else:
                player.triplePower = True
                player.rapidPower = False
                player.spreadPower = False
            print("powered up!")
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
fpsClock = pygame.time.Clock
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
            nextTimeEvent = time.time() + 10
    drawEvents()

    pygame.display.flip()
