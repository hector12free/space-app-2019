import pygame
import random
import sys
from button import button

level = 1 # level 1 - basic; level 2 - with collector

pygame.init()

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

# Starship
player_size = 50
player_pos = [width/2, height-2*player_size]
collectorImg_filepath = 'images/LogoMakr_0rPhIj.png' 
collectorImg = pygame.image.load(collectorImg_filepath)
collectorImg = pygame.transform.rotozoom(collectorImg, 0, 0.125)

# Satellite
satellite_size = 50
satellite_pos = [width/3, height-2*player_size]
satelliteImg_filepath = 'images/satellite.png' 
satelliteImg = pygame.image.load(satelliteImg_filepath)
satelliteImg = pygame.transform.rotozoom(satelliteImg, 0, 0.125)

# Enemy
enemy_size = 50
enemy_pos = [random.randint(0,width-enemy_size), 0]
enemy_list=[enemy_pos]

# Space Junk
spaceJunkImg_filepath = 'images/spaceJunk1.png'
spaceJunkImg = pygame.image.load(spaceJunkImg_filepath)
spaceJunkImg = pygame.transform.rotozoom(spaceJunkImg, 0, 0.125)

speed = 20
screen = pygame.display.set_mode((width,height))

game_over = False

score = 0

clock = pygame.time.Clock()

myfont = pygame.font.SysFont("monospace", 35)

def collector(x,y):
    screen.blit(collectorImg,(x,y))

def spaceJunk(x,y):
    screen.blit(spaceJunkImg,(x,y))

def satellite(x,y):
    screen.blit(satelliteImg,(x,y))

def set_speed(score,speed):
    if score < 20:
        speed = 20
    elif score < 40:
        speed = 25
    elif score < 60:
        speed = 30
    elif score < 80:
        speed = 40
    else:
        speed = speed = score/2+1
    return speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0,width-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        spaceJunk(enemy_pos[0], enemy_pos[1])
#        pygame.draw.rect(screen,blue, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

# update the position of the enemy
def update_enemey_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >=0 and enemy_pos[1] < height:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score
            # enemy_pos[0]= random.randint(0,width-enemy_size)
            # enemy_pos[1] = 0

def collision_check(enemy_list, player_pos, satellite_pos, level):
    if level == 1:
        for enemy_pos in enemy_list:
            if detect_collision(enemy_pos, player_pos):
                return True
            return False
    elif level == 2:
        for enemy_pos in enemy_list:
            if detect_collision(enemy_pos, satellite_pos):
                return True
            return False
            

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x= enemy_pos[0]
    e_y=enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True
    return False

def redrawWindow():
    screen.fill((255,255,255))
    startBtn.draw(screen, (0,0,0))
    quitBtn.draw(screen, (0,0,0))

stayAtHomePage = True
startBtn = button(green, width/3, height*2/3, 120, 50, 'Start')
quitBtn = button(red, width*2/3, height*2/3, 120, 50, 'Close')

while stayAtHomePage:
    redrawWindow()
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            stayAtHomePage = False
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if startBtn.isOver(pos):
                print("clicked the Button")
                stayAtHomePage = False
            elif quitBtn.isOver(pos):
                print("user decided to quit the game")
                stayAtHomePage = False
                pygame.quit()
                quit()
        if event.type == pygame.MOUSEMOTION:
            if startBtn.isOver(pos):
                startBtn.color = greenDark
            else:
                startBtn.color = green
            if quitBtn.isOver(pos):
                quitBtn.color = redDark
            else:
                quitBtn.color = red

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_pos = [x,y] 

    screen.fill(background_color)

    drop_enemies(enemy_list)
    score = update_enemey_positions(enemy_list, score)
    speed = set_speed(score, speed)

    text = "Score:" + str(score)
    label = myfont.render(text, 1, yellow)
    screen.blit(label,(width-200,height-40))

    if collision_check(enemy_list, player_pos, satellite_pos, level):
        game_over=True
        break

    draw_enemies(enemy_list)


    #rect(surface, color, rect, width=0) -> Rect
    # pygame.draw.rect(screen, red, (player_pos[0], player_pos[1], player_size, player_size))
    collector(player_pos[0], player_pos[1])
    if (level == 2):
        satellite(satellite_pos[0], satellite_pos[1])

    clock.tick(30)

    pygame.display.update()
