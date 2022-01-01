import pygame
from pygame import mixer
import random
import math


pygame.init()  # initialize the game

# meh
screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()
# background
bg = icon = pygame.image.load('space.jpg')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


# Title-Display Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):

    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(20)

# Bullet     # Ready - cant see bullet // #fire- bullet moving
BulletImg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 4
Bullet_state = "ready"


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))
    

def isCollision(enemyX, enemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(enemyX-BulletX, 2)) +
                         (math.pow(enemyY-BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game-loop
running = True

################################################################
while running:

    screen.fill((0, 0, 0))  # rgb
    # background image
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed check whether its right/left`
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if Bullet_state == "ready":

                    BulletX = playerX
                    fire_bullet(BulletX, BulletY)
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking spaceship bounadries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            BulletY = 480
            Bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_state = "ready"

    if Bullet_state == "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    clock.tick(60)
    # print(clock.get_fps())

    pygame.display.update()
