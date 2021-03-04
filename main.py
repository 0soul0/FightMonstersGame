import random
import math

import pygame as pg
from pygame import mixer

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Intialize the pg
pg.init()

# create the screen
screen = pg.display.set_mode((800, 600))

# Title and Icon
pg.display.set_caption("monster")
icon = pg.image.load('image/monster.png')
pg.display.set_icon(icon)

# Background
background = pg.image.load('image/space.png')
background = pg.transform.scale(background, (800, 600))
# Background sound
mixer.music.load('sound/background.wav')
# mixer.music.play(1)

# Player
playerImg = pg.image.load('image/player.png')
# set image size
playerImg = pg.transform.scale(playerImg, (60, 60))
playerX = 370
playerY = 480
playerX_change = 0
playerX_speed = 0.5

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    # set image size
    enemyImg.append(pg.transform.scale(pg.image.load('image/monster.png'), (60, 60)))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pg.image.load('image/bullet.png')
# set image size
bulletImg = pg.transform.scale(bulletImg, (40, 20))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"

# Score
score_value = 0
font = pg.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pg.font.Font('freesansbold.ttf', 64)
game_state = "start"

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (300, 300))


# built player
def player(x, y):
    screen.blit(playerImg, (x, y))


# built enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# built bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 10, y))


# collision detection
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 30:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # set background RGB
    screen.fill((0, 255, 0))
    # Background Image
    screen.blit(background, (0, 0))

    # listen event
    for event in pg.event.get():
        # close screen
        if event.type == pg.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = -playerX_speed
            if event.key == pg.K_RIGHT:
                playerX_change = playerX_speed
            if event.key == pg.K_SPACE and bullet_state is "ready":
                # Get the current x coordinate of the spaceship
                bullet_Sound = mixer.Sound('sound/laser.wav')
                # bullet_Sound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0

    if game_state is "gameover":
        game_over_text()
    else:
        # player movement
        playerX += playerX_change
        # setting border of player moving
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):

            # Game Over
            game_over = isCollision(enemyX[i], enemyY[i], playerX, playerY)
            if game_over:
                game_state = "gameover"
                game_over_text()
                for j in range(num_of_enemies):
                    enemyY[i] = 2000
                break

            # enemy movement
            enemyX[i] += enemyX_change[i]
            # setting border of enemy moving
            if enemyX[i] <= 0:
                enemyX_change[i] = -enemyX_change[i]
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -enemyX_change[i]
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_Sound = mixer.Sound('sound/explosion.wav')
                # explosion_Sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                # print(score)
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

    player(playerX, playerY)

    show_score(textX, textY)
    # update screen
    pg.display.update()
