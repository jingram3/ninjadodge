import pygame, sys, time, random
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
starAddRate = 25
windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Ninja Dodge')

BLACK = (0,0,0)

player = pygame.Rect(300, 400, 40, 40)
playerImg = pygame.image.load('img/ninja.png')
playerStretchedImg = pygame.transform.scale(playerImg, (40, 40))
platformImg = pygame.image.load('img/star.png')
background = pygame.image.load('img/bg.png')
backgroundRect = pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT)

moveLeft = False
moveRight = False
MOVESPEED = 10
jumpSpeed = 20

isJumping = False
noJumps = 2
GRAVITY = 2
jumpPoint = 300
starAddCount = 0
right = []
top = []
fromRight = [400, 350, 300, 250]
fromTop = [50, 150, 250, 450, 350, 550, 650, 750]

speedCounter = 1
starSpeed= 15

def newRight():
    right.append(pygame.Rect(WINDOWWIDTH, fromRight[random.randint(0, len(fromRight)-1)], 50, 50))

def newTop():
    top.append(pygame.Rect(fromTop[random.randint(0, len(fromTop)-1)], 0, 50, 50))

newRight()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_SPACE and noJumps>0:
                if noJumps == 2:
                    jumpPoint = player.top
                else:
                    jumpSpeed = 15
                noJumps -= 1
                isJumping = True
                
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
    starAddCount += 1
    if starAddCount == starAddRate:
        starAddCount = 0
        platSize = 40
        newRight()
        newTop()

    for p in right:
        if p.right < 0:
           right.remove(p)
           p.left=WINDOWWIDTH
           speedCounter+=1
           if(speedCounter==3):
               starSpeed+=1
               speedCounter=1
        elif p.colliderect(player):
            print('Game Over')
            pygame.quit()
            sys.exit()
        p.left -= starSpeed

    for p in top:
        if p.bottom > WINDOWHEIGHT:
           top.remove(p)
           p.bottom=0
        elif p.colliderect(player):
            print('Game Over')
            pygame.quit()
            sys.exit()
        p.bottom += starSpeed

    windowSurface.fill(BLACK)
    windowSurface.blit(background, backgroundRect)
    for p in top:
        windowSurface.blit(platformImg, p)

    for p in right:
        windowSurface.blit(platformImg, p)
        
    if moveLeft and player.left > 0:
        player.left -= MOVESPEED
    if moveRight and player.right < WINDOWWIDTH:
        player.right += MOVESPEED
    if isJumping and player.top > 0:
        player.top -= jumpSpeed
        jumpSpeed -= GRAVITY
    if isJumping and player.top >= jumpPoint:
        player.top = jumpPoint
        jumpSpeed = 20
        noJumps = 2
        isJumping = False

    windowSurface.blit(playerStretchedImg, player)
    pygame.display.update()
    mainClock.tick(40)
    
        

