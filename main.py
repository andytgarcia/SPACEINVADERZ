import threading

import pygame
import time
import random
import os

YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
currentTime = time.time()
gameState = "start"
s = 'sound'


##fields for player: x position, y position

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("shipFinal.png").convert()
        self.rect = self.image.get_rect()
        self.movey = 8
        self.nextShot = 0
        self.normalFire = True
        self.spreadPower = False
        self.rapidPower = False
        self.health = 90
        self.score = 0

    def moveUp(self):
        if self.rect.y == 0:
            self.rect.y -= 0
        else:
            self.rect.y -= self.movey

    def moveDown(self):
        if self.rect.y >= 660:
            #print("border!!!")
            self.rect.y += 0
        else:
            self.rect.y += self.movey
            # print(self.rect.y)


class Bullet:
    def __init__(self, x, y, rad, xvel, color, damage, owner):
        # print("bullet made")
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.xvel = xvel
        self.rect = pygame.Rect(self.x - self.rad, self.y - self.rad, self.rad * 2, self.rad * 2)
        self.damage = damage
        self.owner = owner

    def drawBulletHurtBox(self):
        pygame.draw.rect(screen, self.color, self.rect, 0)


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
    def __init__(self):
        self.x = 1279
        self.y = random.randrange(10, 671, 50)
        self.nextShot = 0
        self.health = 100
        self.image = pygame.image.load("invader.png").convert()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # center=(1279, random.randint(1, 670))
        self.isAlive = True
        self.bulletList = []
        self.type = random.randrange(1, 4)

    def updateEnemyBullets(self):
        global gameState
        for b in self.bulletList:
            if b.rect.colliderect(player.rect) and b.owner == self:
                # print("collision")
                self.bulletList.remove(b)
                player.health -= b.damage
                if player.health <= 0:
                    gameState = "end"

    def getRect(self):
        return self.rect

    def setHealth(self, health):
        self.health = health

    def getHealth(self):
        return self.health

    def setStatus(self, status):
        self.isAlive = status


def handleEnemy():
    for en in enemies:
        if en.nextShot < time.time_ns():
            en.bulletList.append(Bullet(en.rect.x + 51, en.rect.y + 25, 5, enemyBulletVelocity, RED, 30, en))
            en.nextShot = time.time_ns() + (enemyFireRate / 2)

        if not en.isAlive:
            enemies.remove(en)
        drawBullets(en.bulletList)
        en.updateEnemyBullets()


def createEnemies(index):
    randNum = random.randint(1, 100)
    if randNum < index:
        enemies.append(Enemy())
        # print("enemy created")
        return True


def drawEnemies():
    for en in enemies:
        screen.blit(en.image, en.rect)
        if en.type == 1:
            while en.rect.x != 1149:
                en.rect.x -= 1
        elif en.type == 2:
            while en.rect.x != 1200:
                en.rect.x -= 1
        else:
            while en.rect.x != 1050:
                en.rect.x -= 1


def createEvent():
    randNum = random.randint(1, 100)
    if randNum < 10:
        if randNum % 2 == 1:
            events.append(Event(True, False))
            # print("spreadshot created")
            return True
        else:
            events.append(Event(False, True))
            # print("rapid created")
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
            bullets.append(Bullet(player.rect.x + 51, player.rect.y + 25, 20, 15, YELLOW, 50, player))
        else:
            bullets.append(Bullet(player.rect.x + 51, player.rect.y + 25, 5, 10, YELLOW, 25, player))
        if not player.rapidPower:
            player.nextShot = time.time_ns() + 1000000000 / 2
        else:
            player.nextShot = time.time_ns() + 100000000 / 2
        pygame.mixer.Sound.play(fire)


def isOffScreen(x, y):
    if x < 0 or x > 1280 or y < 0 or y > 720:
        return True
    else:
        return False


def drawEvents(events):
    for e in events:
        screen.blit(e.image, e.rect)
        e.rect.x += -7
        if e.rect.colliderect(player.rect):
            if e.spreadShot:
                if not player.spreadPower:
                    player.spreadPower = True
                    player.rapidPower = False
                    pygame.mixer.Sound.play(eventAcquire)
                else:
                    player.spreadPower = False
                    player.rapidPower = False
                    player.health = 90
                    pygame.mixer.Sound.play(healthBoost)
            elif e.rapidFire:
                if not player.rapidPower:
                    player.spreadPower = False
                    player.rapidPower = True
                    pygame.mixer.Sound.play(eventAcquire)
                else:
                    player.rapidPower = False
                    player.spreadPower = False
                    player.health = 90
                    pygame.mixer.Sound.play(healthBoost)
            events.remove(e)
        if isOffScreen(e.rect.x, e.rect.y):
            events.remove(e)
            # print("event removed")


def drawBullets(bulletList):
    for b in bulletList:
        pygame.draw.circle(screen, b.color, (b.x, b.y), b.rad, 0)
        b.x += b.xvel
        b.rect.x += b.xvel
        if isOffScreen(b.x, b.y):
            bulletList.remove(b)
            # print("bullet removed")


def updatePlayerBullets():
    for b in bullets:
        for en in enemies:
            if en.rect.colliderect(b.rect):
                try:
                    bullets.remove(b)
                except ValueError:
                    print("")
                en.health = en.health - b.damage
                if en.health <= 0:
                    en.isAlive = False
                    player.score += 100


def startScreen():
    clearScreen()
    screen.blit(backdrop, (0, 0))
    textSurface = bigFont.render("SPACE INVADERZ", True, WHITE)
    screen.blit(textSurface, (400, 200))
    textSurface = littleFont.render("Press Enter to Start Game!", True, WHITE)
    screen.blit(textSurface, (500, 450))


def checkStartScreenKeyPresses():
    global gameState
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        gameState = "playing"


def drawScoreAndHealth():
    textSurface = littleFont.render("Score: " + str(player.score), True, WHITE)
    screen.blit(textSurface, (20, 10))
    if player.health == 90:
        textSurface = littleFont.render("Health: " + str(player.health), True, GREEN)
        screen.blit(textSurface, (20, 50))
    if player.health == 60:
        textSurface = littleFont.render("Health: " + str(player.health), True, YELLOW)
        screen.blit(textSurface, (20, 50))
    if player.health == 30:
        textSurface = littleFont.render("Health: " + str(player.health), True, RED)
        screen.blit(textSurface, (20, 50))


def endScreen():
    global gameState
    textSurface = bigFont.render("GAME OVER!", True, WHITE)
    screen.blit(textSurface, (475, 200))
    textSurface = littleFont.render("Your Score: " + str(player.score), True, WHITE)
    screen.blit(textSurface, (550, 450))
    textSurface = littleFont.render("Press Enter to Play Again", True, WHITE)
    screen.blit(textSurface, (500, 500))


def checkEndScreenPresses():
    global gameState
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        reset()
        gameState = "playing"


def reset():
    player.rect.x = 50
    player.rect.y = 320
    player.normalFire = True
    player.spreadPower = False
    player.rapidPower = False
    player.health = 90
    player.score = 0
    bullets.clear()
    enemies.clear()
    events.clear()
    index = 50
    difficultyTime = 10.0
    counter = 5
    decTime = 2
    enemyBulletVelocity = -10


def clearScreen():
    pygame.draw.rect(screen, pygame.Color(0, 0, 0), (0, 0, 1280, 720))


# start of program
pygame.init()  # start engine
pygame.font.init()  # start font
pygame.mixer.init()  # start sound


#sounds
fire = pygame.mixer.Sound(os.path.join('8d82b5_Galaga_Firing_Sound_Effect.mp3'))
eventAcquire = pygame.mixer.Sound(os.path.join('4.mp3'))
healthBoost = pygame.mixer.Sound(os.path.join('5.mp3'))


bigFont = pygame.font.SysFont('Times New Roman', 50)
littleFont = pygame.font.SysFont('Arial', 18)
FPS = 60  # 60 frames per second
fpsClock = pygame.time.Clock()
worldx = 1280
worldy = 720
screen = pygame.display.set_mode((worldx, worldy))
pygame.display.set_caption("SPACE INVADERS")
gameOver = False
grav = 1
backdrop = pygame.image.load("spaceFinal.jpg").convert()
nextTimeEvent = time.time()
nextEnemyCreate = time.time()

player = Player()
player.rect.x = 50
player.rect.y = 320
i = 0
bullets = []
events = []
enemies = []
index = 50
difficultyTime = 10.0
counter = 5
decTime = 2
enemyBulletVelocity = -10
enemyFireRate = 10_000_000_000

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    if gameState == "start":
        checkStartScreenKeyPresses()
        startScreen()

    if gameState == "end":
        endScreen()
        checkEndScreenPresses()

    if gameState == "playing":

        # main game commands
        clearScreen()
        screen.blit(backdrop, [i, 0])
        screen.blit(backdrop, [worldx + i, 0])
        if i == -worldx:
            screen.blit(backdrop, [worldx + i, 0])
            i = 0
        i -= 2  # 1

        # playerhandling
        screen.blit(player.image, player.rect)
        playerMovement()
        drawBullets(bullets)
        updatePlayerBullets()
        drawScoreAndHealth()

        # event handling
        if nextTimeEvent < time.time():
            if createEvent():
                nextTimeEvent = time.time() + 20
        drawEvents(events)

        # enemy handling
        if nextEnemyCreate < time.time():
            if createEnemies(index):
                nextEnemyCreate = time.time() + difficultyTime
        if player.score % 500 == 0:
            index += counter
            difficultyTime -= decTime
        if player.score >= 10000 and player.score > 0:
            enemyBulletVelocity = -20
        if player.score >= 20000:
            enemyFireRate = 1_000_000_000
        if index <= 75:
            counter = 0
        if difficultyTime == 2:
            decTime = 0

        drawEnemies()
        handleEnemy()

    pygame.display.flip()
    fpsClock.tick(FPS)
