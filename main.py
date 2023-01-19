import pygame
import time

YELLOW = (255, 255, 0)



##fields for player: x position, y position

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("guy.png").convert()
        self.rect = self.image.get_rect()
        self.movex = 0
        self.movey = 0

    def moveUp(self):
        self.rect.y += -1
        print(player.rect.y)

    def moveDown(self):
        self.rect.y += 1
        print(player.rect.y)


class Bullet:
    def __init__(self, x, y, rad, xvel, yvel):
        print("bullet made")
        self.x = x
        self.y = y
        self.rad = rad
        self.color = YELLOW
        self.xvel = xvel
        self.yvel = yvel


def playerMovement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.moveUp()
    if keys[pygame.K_s]:
        player.moveDown()

    if keys[pygame.K_SPACE]:
        bullets.append(Bullet(player.rect.x, player.rect.y, 5, 20, 0))


def isOffScreen(x, y):
    if x < 0 or x > 1280 or y < 0 or y > 720:
        return True
    else:
        return False


def handleBullets():
    for b in bullets:
        pygame.draw.circle(screen, b.color, (b.x, b.y), b.rad, 0)
        b.x += b.xvel
        b.y += b.yvel
        if isOffScreen(b.x, b.y):
            bullets.remove(b)


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

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    clearScreen()
    screen.blit(backdrop, [i,0])
    screen.blit(backdrop, [worldx+i, 0])
    if i == -worldx:
        screen.blit(backdrop, [worldx + i, 0])
        i = 0
    i -= 1
    screen.blit(player.image, player.rect)
    playerMovement()
    handleBullets()

    pygame.display.flip()
