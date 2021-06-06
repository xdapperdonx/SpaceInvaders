import pygame
import random
import math

#used to access pygame module
pygame.init()

#screen
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load("background.png")

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

#enemy
    #blank list to store multiple enemies
enemyImg = []
enemyX = []
enemyX_change = []
enemyY = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))

    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))

    enemyX_change.append(4)
    enemyY_change.append(40)

#missile
missileImg = pygame.image.load("missile.png")
missileX = 0
missileX_change = 0
missileY = 480
missileY_change = 10
#ready: cant see bullet in screen
#fire: bullet is moving
missile_state = "ready"

#score
score_value = 0
#parameteres = type of font and size
font = pygame.font.Font("freesansbold.ttf", 32)

#where to display score
textX = 10
textY = 10

#gameover text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    #render text on screen, parameters(nameOfText, score, appear on screen, (color))
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))


def player(x, y):
    #img and coordinate to draw
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    #img and coordinate to draw
    screen.blit(enemyImg[i], (x, y))

def fire_missile(x,y):
    global missile_state
    missile_state = "fire"
    #debugging
    screen.blit(missileImg,(x + 16, y + 10))

def isCollision(enemyX, enemyY, missileX, missileY):
    #distance formula
    distance = math.sqrt((math.pow(enemyX - missileX,2)) + (math.pow(enemyY - missileY,2)))
    if distance < 27:
        return True
    else:
        return False

running = True

#main game loop
while running:
    #RGB code
    screen.fill((128,0,128))

    #background image
    screen.blit(background, (0,0))

    #loop through all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #if keystroke pressed event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if missile_state is "ready":
                    #save current player x coordinate
                    missileX = playerX
                    fire_missile(missileX, missileY)

        #if released event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0
    
    #updates position if key pressed
    playerX += playerX_change
    #set a boundary for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #enemy movement
    #in for loop to have multiple enemies
    for i in range(num_of_enemies):
        #gameover
        if enemyY[i] > 440:
            #remove enemies
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                #display gameover text
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        #set a boundary for enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        #collision
        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            #reset missle and print score
            missileY = 480
            missile_state = "ready"
            score_value += 1

            #respawn enemy
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

            #draws enemy
        enemy(enemyX[i], enemyY[i], i)

    #multiple missiles
    if missileY <= 0:
        missileY = 480
        missile_state = "ready"

    #bullet movement
    if missile_state is "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change

   

    #screen layer drawn first then player
    player(playerX, playerY)

    #show score call
    show_score(textX, textY)

    #update the screen
    pygame.display.update()