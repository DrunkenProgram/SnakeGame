import pygame
import sys
import random

# ----- [윈도우창 설정] -----

WINDOW_WIDTH = 540
WINDOW_HEIGHT = 600
GRID = 30
GRID_WIDTH = int(WINDOW_WIDTH/GRID)
GRID_HEIGHT = int(WINDOW_HEIGHT/GRID)

# ===== [색상설정] =====

BLACK = "#000000"
RED = "#FF5555"
BLUE1 = "#03256C"
BLUE2 = "#3066BE"
BLUE3 = "#40BCD8"
GREEN = "#4A7c59"
BEIGE1 = "#D1B7A1"
BEIGE2 = "#E9D3C0"
BLACK = "#222222"
WHITE = "#DDDDDD"

NORTH = (0, -1)
SOUTH = (0,  1)
WEST = (-1,  0)
EAST = (1,  0)

# ----- [스네이크 클래스] -----


class Snake:

    def __init__(self):
        self.length = 1
        self.create_snake()
        self.head_color = BLUE1
        self.color1 = BLUE2
        self.color2 = BLUE3

    def create_snake(self):
        self.length = 3
        self.positions = [(int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))]
        self.direction = random.choice([NORTH, SOUTH, WEST, EAST])

    def move_snake(self, surface):

        head = self.get_head_position()
        x, y = self.direction
        next = ((head[0] + (x*GRID)) % WINDOW_WIDTH,
                (head[1] + (y*GRID)) % WINDOW_HEIGHT)
        if next in self.positions[2:]:
            self.create_snake()
            gameover(surface)
        else:
            self.positions.insert(0, next)
            if len(self.positions) > self.length:
                del self.positions[-1]

    def draw_snake(self, surface):
        for index, pos in enumerate(self.positions):
            if index == 0:
                draw_object(surface, self.head_color, pos)
            elif index % 2 == 0:
                draw_object(surface, self.color1, pos)
            else:
                draw_object(surface, self.color2, pos)

    def game_control(self, arrowkey):
        if (arrowkey[0]*-1, arrowkey[1]*-1) == self.direction:
            return
        else:
            self.direction = arrowkey

    def get_head_position(self):
        return self.positions[0]

# ----- [ 먹이 클래스 ] -----


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_food()

    def randomize_food(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRID,
                         random.randint(0, GRID_HEIGHT-1) * GRID)

    def draw_food(self, surface):
        draw_object(surface, self.color, self.position)


# ----- [ 전역 ] -----

def draw_background(surface):
    background = pygame.Rect((0, 0), (WINDOW_WIDTH, WINDOW_HEIGHT))
    draw_grid(surface)


def draw_grid(surface):
    for row in range(0, int(GRID_HEIGHT)):
        for col in range(0, int(GRID_WIDTH)):
            if (row+col) % 2 == 0:
                rect = pygame.Rect((col*GRID, row*GRID), (GRID, GRID))
                pygame.draw.rect(surface, BEIGE1, rect)
            else:
                rect = pygame.Rect((col*GRID, row*GRID), (GRID, GRID))
                pygame.draw.rect(surface, BEIGE2, rect)


def draw_object(surface, color, pos):
    rect = pygame.Rect((pos[0], pos[1]), (GRID, GRID))
    pygame.draw.rect(surface, color, rect)


def position_check(snake, food_group):
    for food in food_group:
        if snake.get_head_position() == food.position:
            global game_score
            game_score += 1
            eating = pygame.mixer.Sound("sound effect/eating.wav")
            eating.play()
            snake.length += 1
            food.randomize_food()


def show_info(surface, snake, speed):
    font = pygame.font.SysFont('Roboto', 40)
    image = font.render(
        f' score: {game_score}  length: {snake.length}  level: {int(player.length//10)} ', True, GREEN)
    pos = image.get_rect()
    pos.move_ip(63, 3)
    surface.blit(image, pos)


def gameover(surface):
    global game_score
    font = pygame.font.SysFont('Roboto', 50)
    image = font.render("GAME OVER", True, BLACK)
    image2 = font.render("press spacebar to restart", True, BLACK)
    image3 = font.render(f' Final score: {game_score}', True, BLACK)
    gameOver = pygame.mixer.Sound("sound effect/gameOver.wav")
    gameOver.play()
    pos = image.get_rect()
    pos2 = image2.get_rect()
    pos3 = image3.get_rect()
    pos.move_ip(165, 240)
    pos2.move_ip(70, 295)
    pos3.move_ip(140, 350)
    surface.blit(image, pos)
    surface.blit(image2, pos2)
    surface.blit(image3, pos3)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    game_score = 0
                    break


def game_start_screen(surface):
    font = pygame.font.SysFont('Roboto', 50)
    image = font.render("SNAKE GAME", True, BLACK)
    image2 = font.render("press spacebar to start", True, BLACK)
    pos = image.get_rect()
    pos2 = image2.get_rect()
    pos.center = ((WINDOW_WIDTH//2), (WINDOW_HEIGHT//2)-30)
    pos2.center = ((WINDOW_WIDTH//2), (WINDOW_HEIGHT//2)+10)

    surface.blit(image, pos)
    surface.blit(image2, pos2)


def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


player = Snake()
run = True
game_score = 0

# ----- [ 먹이 그룹 ] -----


def draw_food_group(food_group, surface):
    for food in food_group:
        food.draw_food(surface)


food = Food()
food_group = []

for i in range(5):
    food = Food()
    food_group.append(food)


# ----- [ game loop ] -----

pygame.init()
pygame.display.set_caption('SNAKE GAME')
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
background = pygame.mixer.Sound("sound effect/background.wav")
background.play(-1)
screen.fill(WHITE)  # or whatever your background color is
game_start_screen(screen)
pygame.display.update()

wait_for_key()  # wait for the user to press space

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            if event.key == pygame.K_UP:
                player.game_control(NORTH)
            if event.key == pygame.K_w:
                player.game_control(NORTH)
            if event.key == pygame.K_LEFT:
                player.game_control(WEST)
            if event.key == pygame.K_a:
                player.game_control(WEST)
            if event.key == pygame.K_DOWN:
                player.game_control(SOUTH)
            if event.key == pygame.K_s:
                player.game_control(SOUTH)
            if event.key == pygame.K_RIGHT:
                player.game_control(EAST)
            if event.key == pygame.K_d:
                player.game_control(EAST)

    draw_background(screen)
    player.move_snake(screen)
    position_check(player, food_group)
    player.draw_snake(screen)
    draw_food_group(food_group, screen)
    speed = player.length/3
    show_info(screen, player, speed)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(5+speed)

# ----- [ 파이게임 종료 ] -----

print('pygame closed')
pygame.quit()
sys.exit()
