import pygame
import random
from sys import exit

WIDTH = 840
HEIGHT = 600 
BLOCKSIZE = 40
ARRAYWIDTH = WIDTH // BLOCKSIZE
ARRAYHEIGHT = HEIGHT // BLOCKSIZE
RECTCOLOR = (100,100,100)
FOODCOLOR = (255,0,0)
SNAKEHEADCOLOR = (0,200,0)
SNAKETAILCOLOR = (0,150,0)


# Initialize Game
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake')
# Icon attributed to <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
icon = pygame.image.load('C:/Users/derek/OneDrive/Documents/Python Projects/Snake/snake.png') 
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
score = 0


# Background
def draw_Grid():
    for x in range(0,WIDTH,BLOCKSIZE):
        for y in range(0,HEIGHT,BLOCKSIZE):
            rect = pygame.Rect(x,y,BLOCKSIZE,BLOCKSIZE)
            pygame.draw.rect(screen,RECTCOLOR,rect,1)

# Music
pygame.mixer.music.load('C:/Users/derek/OneDrive/Documents/Python Projects/Snake/background.mp3')
pygame.mixer.music.play(-1)

# Sounds
lose_sound = pygame.mixer.Sound('C:/Users/derek/OneDrive/Documents/Python Projects/Snake/explosion.wav')
eat_sound = pygame.mixer.Sound('C:/Users/derek/OneDrive/Documents/Python Projects/Snake/eatfood.wav')
change_direction_sound = pygame.mixer.Sound('C:/Users/derek/OneDrive/Documents/Python Projects/Snake/change_direction.wav')

play_lose_sound = True

# Food
class Food:
    def __init__(self):        
        self.foodX = random.randint(0,(WIDTH//BLOCKSIZE)-1)
        self.foodY = random.randint(0,(HEIGHT//BLOCKSIZE)-1)
        self.recto = pygame.Rect(self.foodX*BLOCKSIZE,self.foodY*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE)
food = Food()

def eatFood():
    foodt = (food.foodX,food.foodY)
    if snake.body[0] == foodt:
        global score
        score += 1
        eat_sound.play()

        # Move food to new spot that is not in snake body
        food.foodX = random.randint(0,(WIDTH//BLOCKSIZE)-1)
        food.foodY = random.randint(0,(HEIGHT//BLOCKSIZE)-1)
        while (food.foodX,food.foodY) in snake.body:
            food.foodX = random.randint(0,(WIDTH//BLOCKSIZE)-1)
            food.foodY = random.randint(0,(HEIGHT//BLOCKSIZE)-1)
        food.recto = pygame.Rect(food.foodX*BLOCKSIZE,food.foodY*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE)

        # Grow snake
        snaketailx = snake.body[-1][0]
        snaketaily = snake.body[-1][1]
        if snake.facing == "L":
            snake.body.append((snaketailx+1,snaketaily))
        elif snake.facing == "R":
            snake.body.append((snaketailx-1,snaketaily))
        elif snake.facing == "U":
            snake.body.append((snaketailx,snaketaily+1))
        elif snake.facing == "D":
            snake.body.append((snaketailx,snaketaily-1))

# Snake (List of coordinates)
class Snake:
    def __init__(self):
                
        self.body = [( (ARRAYWIDTH)//2, (ARRAYHEIGHT)//2 ), ( (ARRAYWIDTH)//2 + 1, (ARRAYHEIGHT)//2 )]
        self.snake_L = False
        self.snake_R = False
        self.snake_U = False
        self.snake_D = False
        self.alive = True
        self.hasmoved = False
        self.facing = "Null"
snake = Snake()

def draw_Snake():
    # Draw head
    x, y = snake.body[0]
    snakeheadrect = pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
    pygame.draw.rect(screen, SNAKEHEADCOLOR, snakeheadrect)

    # Draw tail
    for x,y in snake.body[1:]:
        snaketailrect = pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(screen, SNAKETAILCOLOR, snaketailrect)

def left_Snake():
    newsnakex = snake.body[0][0] - 1
    if outofBounds(newsnakex,'X'):
        return
    if (newsnakex,snake.body[0][1]) in snake.body:
        snake.alive = False
        return

    snake.body.insert(0,(newsnakex,snake.body[0][1]))
    snaketail = snake.body.pop()
    rect = pygame.Rect((snaketail[0])*BLOCKSIZE,(snaketail[1])*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE) # Rect of tail of snake
    pygame.draw.rect(screen,(0,0,0),rect) # Turn that rect into black rect
    pygame.draw.rect(screen,RECTCOLOR,rect,1) # Give that black rect a gray outline
    
def right_Snake():
    newsnakex = snake.body[0][0] + 1
    if outofBounds(newsnakex,'X'):
        return
    if (newsnakex,snake.body[0][1]) in snake.body:
        snake.alive = False
        return

    snake.body.insert(0,(newsnakex, snake.body[0][1]))
    snaketail = snake.body.pop()
    rect = pygame.Rect((snaketail[0])*BLOCKSIZE,(snaketail[1])*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE) # Rect of tail of snake
    pygame.draw.rect(screen,(0,0,0),rect) # Turn that rect into black rect
    pygame.draw.rect(screen,RECTCOLOR,rect,1) # Give that black rect a gray outline

def up_Snake():
    newsnakey = snake.body[0][1] - 1
    if outofBounds(newsnakey,'Y'):
        return
    if (snake.body[0][0],newsnakey) in snake.body:
        snake.alive = False
        return

    snake.body.insert(0,(snake.body[0][0], newsnakey))
    snaketail = snake.body.pop()
    rect = pygame.Rect((snaketail[0])*BLOCKSIZE,(snaketail[1])*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE) # Rect of tail of snake
    pygame.draw.rect(screen,(0,0,0),rect) # Turn that rect into black rect
    pygame.draw.rect(screen,RECTCOLOR,rect,1) # Give that black rect a gray outline

def down_Snake():
    newsnakey = snake.body[0][1] + 1
    if outofBounds(newsnakey,'Y'):
        return
    if (snake.body[0][0],newsnakey) in snake.body:
        snake.alive = False
        return

    snake.body.insert(0,(snake.body[0][0], newsnakey))
    snaketail = snake.body.pop()
    rect = pygame.Rect((snaketail[0])*BLOCKSIZE,(snaketail[1])*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE) # Rect of tail of snake
    pygame.draw.rect(screen,(0,0,0),rect) # Turn that rect into black rect
    pygame.draw.rect(screen,RECTCOLOR,rect,1) # Give that black rect a gray outline

# Game Over Font and Text Display
game_over_font = pygame.font.Font("freesansbold.ttf", 64)
score_font = pygame.font.Font("freesansbold.ttf", 64)

def gameover_text():
    game_over = game_over_font.render("GAMEOVER", True, (255,255,255))
    score_show = score_font.render("SCORE: " + str(score), True, (255,255,255))
    screen.blit(game_over,(220,250))
    screen.blit(score_show,(260,320))

def outofBounds(val, xory):
    if xory == 'X':
        if val < 0 or val > 20:
            snake.alive = False
            return True
    elif xory == 'Y':
        if val < 0 or val > 14:
            snake.alive = False
            return True
    return False

# Creates event for snake movement and controls the speed
MOVE_SNAKE = pygame.USEREVENT
pygame.time.set_timer(MOVE_SNAKE,110)

cooldown = 0
# Game loop
while True:
    draw_Grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.snake_R == False and snake.snake_L == False and cooldown == 0:
                change_direction_sound.play()
                snake.snake_L = True
                snake.snake_R = False
                snake.snake_U = False
                snake.snake_D = False
                snake.hasmoved = True
                snake.facing = "L"
                cooldown = 4
                
            elif event.key == pygame.K_RIGHT and snake.snake_L == False and snake.snake_R == False and snake.hasmoved == True and cooldown == 0:
                change_direction_sound.play()
                snake.snake_L = False
                snake.snake_R = True
                snake.snake_U = False
                snake.snake_D = False
                snake.hasmoved = True
                snake.facing = "R"
                cooldown = 4
                
            elif event.key == pygame.K_UP and snake.snake_D == False and snake.snake_U == False and cooldown == 0:
                change_direction_sound.play()
                snake.snake_L = False
                snake.snake_R = False
                snake.snake_U = True
                snake.snake_D = False
                snake.hasmoved = True
                snake.facing = "U"
                cooldown = 4
                 
            elif event.key == pygame.K_DOWN and snake.snake_U == False and snake.snake_D == False and cooldown == 0:
                change_direction_sound.play()
                snake.snake_L = False
                snake.snake_R = False
                snake.snake_U = False
                snake.snake_D = True
                snake.hasmoved = True
                snake.facing = "D"
                cooldown = 4
        
        elif event.type == MOVE_SNAKE and snake.alive == True:
            if snake.snake_L == True:
                left_Snake()
            elif snake.snake_R == True:
                right_Snake()
            elif snake.snake_U == True:
                up_Snake()
            elif snake.snake_D == True:
                down_Snake()            

    # Draw Food   
    pygame.draw.rect(screen,FOODCOLOR,food.recto)

    # If snake is alive it can eat food and is drawn on screen
    if snake.alive:
        eatFood()
        draw_Snake()
    
    # Otherwise, game ends
    else:
        if play_lose_sound:
            pygame.mixer.music.fadeout(5)
            lose_sound.play()
            play_lose_sound = False
        draw_Snake()
        gameover_text()

    # Update display and control FPS
    if cooldown > 0: cooldown -= 1
    pygame.display.flip()
    clock.tick(60)