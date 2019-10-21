import pygame
import random
import sys
from button import button

# TODO add sound effects
# TODO add transation page between levels

# TODO enhancements:
# TODO show buttons directly in play pages
# TODO display different satellites/collectors/junks
# TODO 

# Set isDemoMode flag to True to only play with level 2, which is more interesting
isDemoMode = True

# level 1 - basic; level 2 - with collector to clean space junk
level = 2 if isDemoMode else 1

pygame.init()
pygame.display.set_caption("Space Junk Terminator")

# Window width & Height
width = 800
height = 600

# Colors
red = (197, 38, 32) # (255, 0, 0)
redDark = (154, 30, 25)
blue = (0, 0, 255)
yellow = (255, 255, 0)
green = (36, 194, 179) # (0, 200, 0)
greenDark = (28, 151, 139)
backgroundColor = (0, 0, 0)

# Starship collector
collectorSize = 50
collectorPos = [width / 3, height - 2 * collectorSize]
collectorImgFilePath = 'images/LogoMakr_0rPhIj.png' 
collectorImg = pygame.image.load(collectorImgFilePath)
collectorImg = pygame.transform.rotozoom(collectorImg, 0, 0.125)

# Satellite
satelliteSize = 50
satellitePos = [width / 2 - collectorSize / 2, height / 2 - collectorSize / 2]
satelliteImgFilePath = 'images/satellite.png' 
satelliteImg = pygame.image.load(satelliteImgFilePath)
satelliteImg = pygame.transform.rotozoom(satelliteImg, 0, 0.125)

# Enemy - Space Junk
enemySize = 50
enemyPos = [random.randint(0, width - enemySize), 0]
enemyList = [enemyPos]
spaceJunkImgFilePath = 'images/spaceJunk1.png'
spaceJunkImg = pygame.image.load(spaceJunkImgFilePath)
spaceJunkImg = pygame.transform.rotozoom(spaceJunkImg, 0, 0.03)

speed = 20
screen = pygame.display.set_mode((width, height))

gameOver = False

score = 0

clock = pygame.time.Clock()

myfont = pygame.font.SysFont("monospace", 35)

def initializeStates(collectorPos, satellitePos, enemyList):
    collectorPos = [width / 3, height - 2 * collectorSize]
    satellitePos = [width / 2, height - 2 * collectorSize]

    enemyPos = [random.randint(0, width - enemySize), 0]
    enemyList = [enemyPos]

def drawCollector(x, y):
    screen.blit(collectorImg, (x, y))

def drawSpaceJunk(x, y):
    screen.blit(spaceJunkImg, (x, y))

def drawSatellite(x, y):
    screen.blit(satelliteImg, (x, y))

def setSpeed(score, speed):
    # if score < 20:
    #     speed = 20
    # elif score < 40:
    #     speed = 25
    # elif score < 60:
    #     speed = 30
    # elif score < 80:
    #     speed = 40
    # else:
    #     speed = speed = score / 2 + 1
    return speed

def dropEnemies(enemyList):
    delay = random.random()
    if len(enemyList) < 10 and delay < 0.1:
        posX = random.randint(0, width - enemySize)
        posY = 0
        enemyList.append([posX, posY])

def drawEnemies(enemyList):
    for enemyPos in enemyList:
        drawSpaceJunk(enemyPos[0], enemyPos[1])

# update the position of the enemy
def updateEnemeyPositions(enemyList, score):
    for idx, enemyPos in enumerate(enemyList):
        if enemyPos[1] >=0 and enemyPos[1] < height:
            enemyPos[1] += speed
        else:
            enemyList.pop(idx)
            score += 1
    return score

def cleanJunk(enemyList):
    for enemyPos in enemyList:
        if detectCollision(enemyPos, collectorPos, collectorSize):
            enemyList.remove(enemyPos)
    
def hasCollisionWithSatellite(enemyList):
    for enemyPos in enemyList:
        if detectCollision(enemyPos, satellitePos, satelliteSize):
            return True
    return False

def detectCollision(objectPos, enemyPos, objectSize):
    p_x = objectPos[0]
    p_y = objectPos[1]

    e_x= enemyPos[0]
    e_y=enemyPos[1]

    if (e_x >= p_x and e_x < (p_x + objectSize)) or (p_x >= e_x and p_x < (e_x + enemySize)):
        if (e_y >= p_y and e_y < (p_y + objectSize)) or (p_y >= e_y and p_y < (e_y + enemySize)):
            return True
    return False

def redrawWindow(continueBtn, quitBtn):
    screen.fill(backgroundColor)
    continueBtn.draw(screen, (0, 0, 0))
    quitBtn.draw(screen, (0, 0, 0))

def drawTransitionPage(continueBtnText):
    stayAtThisPage = True
    continueBtn = button(green, width / 3, height * 2 / 3, 120, 50, continueBtnText)
    quitBtn = button(red, width * 2 / 3, height * 2 / 3, 120, 50, 'Close')

    while stayAtThisPage:
        redrawWindow(continueBtn, quitBtn)
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                stayAtThisPage = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continueBtn.isOver(pos):
                    print("clicked the Button", continueBtnText)
                    stayAtThisPage = False
                elif quitBtn.isOver(pos):
                    print("user decided to quit the game")
                    stayAtThisPage = False
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEMOTION:
                if continueBtn.isOver(pos):
                    continueBtn.color = greenDark
                else:
                    continueBtn.color = green
                if quitBtn.isOver(pos):
                    quitBtn.color = redDark
                else:
                    quitBtn.color = red

drawTransitionPage("Start")

while True:
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                x = collectorPos[0]
                y = collectorPos[1]

                if event.key == pygame.K_LEFT and x > speed:
                    x -= collectorSize
                elif event.key == pygame.K_RIGHT and x < width - speed - collectorSize:
                    x += collectorSize
                elif event.key == pygame.K_UP and y > speed:
                    y -= collectorSize
                elif event.key == pygame.K_DOWN and y < height - speed - collectorSize:
                    y += collectorSize

                collectorPos = [x,y] 

        screen.fill(backgroundColor)

        dropEnemies(enemyList)
        score = updateEnemeyPositions(enemyList, score)
        speed = setSpeed(score, speed)

        text = "Score: " + str(score)
        label = myfont.render(text, 1, yellow)
        screen.blit(label, (width - 200, height - 40))

        if level > 1: # only clear junk when level > 1
            cleanJunk(enemyList)

        if not isDemoMode and hasCollisionWithSatellite(enemyList):
            gameOver=True
            break

        drawEnemies(enemyList)

        drawSatellite(satellitePos[0], satellitePos[1])
        if (level > 1):
            drawCollector(collectorPos[0], collectorPos[1])

        clock.tick(30)

        pygame.display.update()

    # go to game over page with Next & Quit buttons
    drawTransitionPage("Next")

    # when user select Next button, user go to play next level
    gameOver = False
    level += 1
    # score = 0
    initializeStates(collectorPos, satellitePos, enemyList)
    print("next level: ", level)