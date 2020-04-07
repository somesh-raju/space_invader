import pygame, random, math
from pygame import mixer

# initializing pygame
pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 600))

# Change title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# background
background_img = pygame.image.load("background.png")

# Player
coord_change = 0
space_ship = pygame.image.load("space-ship.png")
playerX = 370
playerY = 480
def player(x, y):
    screen.blit(space_ship, (x, y))

# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemy_coord_changeX = []
enemy_count = 6
for _ in range(enemy_count):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(5, 720))
    enemyY.append(random.randint(5, 200))
    enemy_coord_changeX.append(5)
enemy_coord_changeY = 30

def enemy(x,y,i):
    screen.blit(enemy_img[i], (x, y))

# Bullet
bullet_img = pygame.image.load("bullet.png")
bulletX = 370
bulletY = 480
bulletY_coord_change = 10
bullet_state = "ready"
def bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))

# Collision
def collision(enemyX, enemyY, bulletX, bulletY):
    distance_bw_coord = math.sqrt(math.pow((enemyX-bulletX),2)+math.pow((enemyY-bulletY),2))
    if distance_bw_coord < 27:
        return True
    return False

# Score
score_value = 0
font = pygame.font.Font('Revamped.otf', 35)
scoreX = 10
scoreY = 10
def score_func(x,y, score_value):
    txt = f"SCORE : {score_value}"
    s = font.render(txt,True, (255,255,255))
    screen.blit(s,(x,y))

# Game Over
game = ""
def game_over():
    global enemy_img
    global enemyX
    global enemyY
    global enemy_coord_changeX
    global enemy_count
    global game
    enemy_img = []
    enemyX = []
    enemyY = []
    enemy_coord_changeX = []
    enemy_count = 0
    game = "over"

# Sounds
mixer.music.load("background.wav")
mixer.music.play(-1)

# Game loop - like infinite loop until X is not pressed, to catch events
running = True
while running:
    # fill screen with RGB values
    # screen.fill((0, 0, 0))
    screen.blit(background_img, (0, 0))

    # Catch events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                coord_change = 4
            if event.key == pygame.K_LEFT:
                coord_change = -4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                coord_change = 0

    playerX += coord_change

    # player boundary
    if playerX >= 730:
        playerX = 730
    elif playerX <= 5:
        playerX = 5

    # Enemy boundary, movement
    for i in range(enemy_count):
        # Game Over block
        if (enemyX[i] in range((playerX-45),(playerX-40)) or enemyX[i] in range((playerX+40),(playerX+45))) and enemyY[i] > (playerY-70):
            game_over()
            break

        enemyX[i] += enemy_coord_changeX[i]
        if enemyX[i] >= 730:
            enemy_coord_changeX[i] = -3
            enemyY[i] += enemy_coord_changeY
        elif enemyX[i] <= 5:
            enemy_coord_changeX[i] = 3
            enemyY[i] += enemy_coord_changeY
        # Collision
        if collision(enemyX[i], enemyY[i], bulletX, bulletY):
            # collision sound
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            score_value += 1
            bulletX = 370
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(5, 720)
            enemyY[i] = random.randint(5, 200)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_coord_change
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # display GAME OVER if game == over
    if game == "over":
        font_game_over = pygame.font.Font("Revamped.otf", 80)
        s1 = font_game_over.render("GAME OVER", True, (255, 0, 0))
        screen.blit(s1, (120, 270))

    player(playerX, playerY)
    score_func(scoreX,scoreY,score_value)
    pygame.display.update()
