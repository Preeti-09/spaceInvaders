import pygame
import random 
import os.path
import math
from pygame import mixer

#initialise pygame
pygame.init()

#set screen
screen = pygame.display.set_mode((800,600))

#loading
filepath = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(filepath,'background.png'))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join(filepath,'space-shuttle.png'))
pygame.display.set_icon(icon)
mixer.music.load(os.path.join(filepath,'background.wav'))
mixer.music.play(-1)

#score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#gameover
overFont = pygame.font.Font('freesansbold.ttf',64)

#player
playerImg = pygame.image.load(os.path.join(filepath,'spaceship.png'))
playerX = 450
playerY = 480
playerX_change = 0 

#enemy 
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
noOfEnemies = 5

for i in range(noOfEnemies):
    enemyImg.append(pygame.image.load(os.path.join(filepath,'enemy.png')))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(30,100))
    enemyX_change.append(6)
    enemyY_change.append(40)

#bullet
bulletImg = pygame.image.load(os.path.join(filepath,'bullet.png'))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bulletState = "ready"

#define functions
def gameOverText():
    overText = overFont.render("Score : " + str(scoreValue),True,(255,255,255))
    screen.blit(overText,(250,250))

def showScore(x,y):
    score = font.render("Score : " + str(scoreValue),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x,y ):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i ):
    screen.blit(enemyImg[i],(x,y))

def fireBullet(x,y):
    global bulletState
    if bulletState is "dead":
        return
    bulletState = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

#pygame driver
running = True
while running:
    
    screen.fill((0,0,0))    
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #if keystroke is pressed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            #print('Left arrow pressed')
            playerX_change -= 1
        if event.key == pygame.K_RIGHT:
            #print('Right arrow pressed')
            playerX_change += 1
        if event.key == pygame.K_SPACE:
            if bulletState is "ready":
                bulletSound = mixer.Sound(os.path.join(filepath,'laser.wav'))
                bulletSound.play()
                bulletX = playerX
                fireBullet(bulletX,bulletY)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #print('key lifted')
            playerX_change = 0 

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    
    for i in range(noOfEnemies):
        
        #game over
        if enemyY[i] > 440:
            for j in range(noOfEnemies):
                enemyY[j] = 2000
            bulletState = "dead"
            gameOverText()
            break
    
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] *= -1
        if enemyX[i] > 736:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] *= -1
        
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosionSound = mixer.Sound(os.path.join(filepath,'explosion.wav'))
            explosionSound.play()
            bulletY = 480
            bulletState = "ready"
            scoreValue += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(30,100)
        
        enemy(enemyX[i],enemyY[i],i)
    
    
    if bulletY <= 0 :
        bulletY = 480
        bulletState = "ready"
     
    if bulletState is "fire":
        fireBullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
    player(playerX,playerY)
    showScore(textX,textY)
    
    pygame.display.update()
