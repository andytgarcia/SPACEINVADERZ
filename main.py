import pygame



##fields for player: x position, y position,

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

    def simGrav(self):
        self.rect.y += grav
        if self.rect.y > worldy:
            self.rect.y = worldy





def playerMovement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.moveUp()
    if keys[pygame.K_s]:
        player.moveDown()








def clearScreen():
    pygame.draw.rect(screen, pygame.Color(0, 0, 0), (0,0, 1280, 720))


# start of program
pygame.init()  # start engine
FPS = 60  # 60 frames per second
fpsClock = pygame.time.Clock
worldx = 1280
worldy = 720
screen = pygame.display.set_mode((worldx, worldy))
gameOver = False
grav = 1


player = Player()
player.rect.x = 50
player.rect.y = 320

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
    pygame.display.flip()

    clearScreen()
    screen.blit(player.image, player.rect)
    playerMovement()
    player.simGrav()

