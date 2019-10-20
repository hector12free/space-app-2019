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

# level 1 - basic; level 2 - with collector
level = 1
if isDemoMode:
    level = 2 # TODO change it back

pygame.init()
pygame.display.set_caption("Space Junk Terminator")

# Window width & Height
width = 800
height = 600

# Colors
red = (197, 38, 32) # (255,0,0)
redDark = (154, 30, 25)
blue = (0,0,255)
yellow = (255,255,0)
green = (36, 194, 179) # (0, 200, 0)
greenDark = (28, 151, 139)
background_color = (0,0,0)

# Starship collector
collector_size = 50
collector_pos = [width/3, height-2*collector_size]
collectorImg_filepath = 'images/LogoMakr_0rPhIj.png' 
collectorImg = pygame.image.load(collectorImg_filepath)
collectorImg = pygame.transform.rotozoom(collectorImg, 0, 0.125)

# Satellite
satellite_size = 50
satellite_pos = [width/2, height-2*collector_size]
satelliteImg_filepath = 'images/satellite.png' 
satelliteImg = pygame.image.load(satelliteImg_filepath)
satelliteImg = pygame.transform.rotozoom(satelliteImg, 0, 0.125)

# Enemy - Space Junk
enemy_size = 50
enemy_pos = [random.randint(0,width-enemy_size), 0]
enemy_list=[enemy_pos]
spaceJunkImg_filepath = 'images/spaceJunk1.png'
spaceJunkImg = pygame.image.load(spaceJunkImg_filepath)
spaceJunkImg = pygame.transform.rotozoom(spaceJunkImg, 0, 0.03)

speed = 20
screen = pygame.display.set_mode((width,height))

game_over = False

score = 0

clock = pygame.time.Clock()

myfont = pygame.font.SysFont("monospace", 35)

def initializeStates(collector_pos, satellite_pos, enemy_list):
    collector_pos = [width/3, height-2*collector_size]
    satellite_pos = [width/2, height-2*collector_size]

    enemy_pos = [random.randint(0,width-enemy_size), 0]
    enemy_list=[enemy_pos]

def drawCollector(x,y):
    screen.blit(collectorImg,(x,y))

def drawSpaceJunk(x,y):
    screen.blit(spaceJunkImg,(x,y))

def drawSatellite(x,y):
    screen.blit(satelliteImg,(x,y))

def set_speed(score,speed):
    # if score < 20:
    #     speed = 20
    # elif score < 40:
    #     speed = 25
    # elif score < 60:
    #     speed = 30
    # elif score < 80:
    #     speed = 40
    # else:
    #     speed = speed = score/2+1
    return speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0,width-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        drawSpaceJunk(enemy_pos[0], enemy_pos[1])

# update the position of the enemy
def update_enemey_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >=0 and enemy_pos[1] < height:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def cleanJunk(enemy_list):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, collector_pos, collector_size):
            enemy_list.remove(enemy_pos)
    
def hasCollisionWithSatellite(enemy_list):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, satellite_pos, satellite_size):
            return True
    return False

def detect_collision(object_pos, enemy_pos, object_size):
    p_x = object_pos[0]
    p_y = object_pos[1]

    e_x= enemy_pos[0]
    e_y=enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + object_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + object_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True
    return False

def redrawWindow(continueBtn, quitBtn):
    screen.fill(background_color)
    continueBtn.draw(screen, (0,0,0))
    quitBtn.draw(screen, (0,0,0))

def drawTransitionPage(continueBtnText):
    stayAtThisPage = True
    continueBtn = button(green, width/3, height*2/3, 120, 50, continueBtnText)
    quitBtn = button(red, width*2/3, height*2/3, 120, 50, 'Close')

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
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                x = collector_pos[0]
                y = collector_pos[1]

                if event.key == pygame.K_LEFT and x > speed:
                    x -= collector_size
                elif event.key == pygame.K_RIGHT and x < width - speed - collector_size:
                    x += collector_size
                elif event.key == pygame.K_UP and y > speed:
                    y -= collector_size
                elif event.key == pygame.K_DOWN and y < height - speed - collector_size:
                    y += collector_size

                collector_pos = [x,y] 

        screen.fill(background_color)

        drop_enemies(enemy_list)
        score = update_enemey_positions(enemy_list, score)
        speed = set_speed(score, speed)

        text = "Score:" + str(score)
        label = myfont.render(text, 1, yellow)
        screen.blit(label,(width-200,height-40))

        if level > 1: # only clear junk when level > 1
            cleanJunk(enemy_list)

        if not isDemoMode and hasCollisionWithSatellite(enemy_list):
            game_over=True
            break

        draw_enemies(enemy_list)

        drawSatellite(satellite_pos[0], satellite_pos[1])
        if (level > 1):
            drawCollector(collector_pos[0], collector_pos[1])

        clock.tick(30)

        pygame.display.update()

    # go to game over page with Next & Quit buttons
    drawTransitionPage("Next")

    # when user select Next button, user go to play next level
    game_over = False
    level += 1
    # score = 0
    initializeStates(collector_pos, satellite_pos, enemy_list)
    print("next level: ", level)