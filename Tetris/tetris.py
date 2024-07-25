"""
JEU TETRIS 
DEBUT : 23/07
FIN : 24/07
DUREE : 5H-6H 
"""


import pygame, sys, os
from random import randint
import copy
import button 

pygame.init()

# Constants
WIDTH, HEIGHT = 920, 650
FPS = 60
NB_COL = 10
NB_ROW = 18
SIZE_CELL = 33

# Colors
COLOR_BG = (44, 62, 80)
COLOR_GAME = (52, 73, 94)
COLOR_LINE = (23, 32, 42)

LIST_COLOR_BLOCK = [(179, 182, 183), (247, 220, 111), (236, 112, 99), (93, 173, 226), (88, 214, 141), (155, 89, 182)]

# Block definitions
BLOCKS = [
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],        # O
    [[1, 1, 1, 1]],          # I
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

class Game:
    def __init__(self, screen):
        self.list_block = BLOCKS
        self.list_color = LIST_COLOR_BLOCK
        self.screen = screen
        self.win_point = [0, 40, 100, 300, 1200]
        self.font = pygame.font.SysFont("Calibri", 45)
        self.start()

    def start(self):
        self.grid = [[0 for _ in range(NB_COL)] for _ in range(NB_ROW)]
        self.score = 0
        self.block_suit = []
        self.color_suit = []
        
        for i in range(4):
            self.block_suit.append(copy.deepcopy(self.list_block[randint(0, len(self.list_block) - 1)]))
            self.color_suit.append(copy.deepcopy(self.list_color[randint(0, len(self.list_color) - 1)]))
    
        self.block = copy.deepcopy(self.block_suit[0])
        self.color = copy.deepcopy(self.color_suit[0])
        self.block_position = [0, NB_COL // 2 - len(self.block[0]) // 2]
        
        self.page_game_init()

    def page_game_init(self):
        self.surface_game = pygame.Surface((NB_COL * SIZE_CELL, NB_ROW * SIZE_CELL))
        self.surface_game.fill(COLOR_GAME)
        self.surface_spawn = pygame.Surface((6 * SIZE_CELL, 12 * SIZE_CELL))
        self.surface_spawn.fill(COLOR_GAME)

    def draw(self):
        screen.fill(COLOR_BG)
        self.screen.blit(self.surface_game, ((WIDTH // 4, 10)))  # surface of the game
        self.screen.blit(self.surface_spawn, ((WIDTH//2+200, 10)))  # surface of the spawn piece
        self.surface_game.fill(COLOR_GAME)
        self.surface_spawn.fill(COLOR_GAME)

        #score 
        self.text_score = self.font.render(f"Score : {self.score}", True, (255, 255, 255))
        self.screen.blit(self.text_score, (WIDTH//2+230, HEIGHT-150))

        #grid of spawn piece 
        self.draw_grid(1, COLOR_LINE, 12, 6, self.surface_spawn)

        # Draw blocks already placed
        for index, value in enumerate(self.grid):
            for index2, value2 in enumerate(value):
                if value2 != 0:
                    square = pygame.Rect(index2 * SIZE_CELL + 1, index * SIZE_CELL + 1, SIZE_CELL - 2, SIZE_CELL - 2)
                    pygame.draw.rect(self.surface_game, value2, square)

        # Draw current block
        for y, row in enumerate(self.block):
            for x, cell in enumerate(row):
                if cell:
                    square = pygame.Rect((self.block_position[1] + x) * SIZE_CELL + 1, (self.block_position[0] + y) * SIZE_CELL + 1, SIZE_CELL - 2, SIZE_CELL - 2)
                    pygame.draw.rect(self.surface_game, self.color, square)

        # Draw piece in spawn surface
        for piece in self.block_suit[1]:
            square = pygame.Rect((piece[1] - 2) * SIZE_CELL + 1, piece[0] * SIZE_CELL + 1 + SIZE_CELL, SIZE_CELL - 2, SIZE_CELL - 2)
            pygame.draw.rect(self.surface_spawn, self.color_suit[1], square)

        for piece in self.block_suit[2]:
            square = pygame.Rect((piece[1] - 2) * SIZE_CELL + 1, piece[0] * SIZE_CELL + 1 + SIZE_CELL * 5, SIZE_CELL - 2, SIZE_CELL - 2)
            pygame.draw.rect(self.surface_spawn, self.color_suit[2], square)
        
        for piece in self.block_suit[3]:
            square = pygame.Rect((piece[1] - 2) * SIZE_CELL + 1, piece[0] * SIZE_CELL + 1 + SIZE_CELL * 9, SIZE_CELL - 2, SIZE_CELL - 2)
            pygame.draw.rect(self.surface_spawn, self.color_suit[3], square)
        
        # Draw grid
        self.draw_grid(1, COLOR_LINE, NB_ROW, NB_COL, self.surface_game)

    def draw_grid(self, widthValue, color, nb_row, nb_col, surface):
        for i in range(nb_row):
            for j in range(nb_col):
                square = pygame.Rect(j * SIZE_CELL, i * SIZE_CELL, SIZE_CELL, SIZE_CELL)
                pygame.draw.rect(surface, color, square, width=widthValue)

    def move_fall(self):
        global state_menu
        self.block_position[0] += 1
        if self.check_collision():
            self.block_position[0] -= 1
            self.merge_block()
            self.new_block()
            self.detect_line()
            if self.check_collision():
                state_menu = True
                self.start()

    def move_right(self):
        self.block_position[1] += 1
        if self.check_collision():
            self.block_position[1] -= 1

    def move_left(self):
        self.block_position[1] -= 1
        if self.check_collision():
            self.block_position[1] += 1

    def rotate_right(self):
        self.block = [list(row) for row in zip(*self.block[::-1])]
        if self.check_collision():
            self.block = [list(row) for row in zip(*self.block)][::-1]

    def rotate_left(self):
        self.block = [list(row) for row in zip(*self.block)][::-1]
        if self.check_collision():
            self.block = [list(row) for row in zip(*self.block[::-1])]

    def check_collision(self):
        for y, row in enumerate(self.block):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.block_position[1] + x
                    new_y = self.block_position[0] + y
                    if new_x < 0 or new_x >= NB_COL or new_y >= NB_ROW or self.grid[new_y][new_x]:
                        return True
        return False

    def merge_block(self):
        for y, row in enumerate(self.block):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.block_position[0] + y][self.block_position[1] + x] = self.color

    def new_block(self):
        self.block_suit.pop(0)
        self.color_suit.pop(0)
        self.block_suit.append(copy.deepcopy(self.list_block[randint(0, len(self.list_block) - 1)]))
        self.color_suit.append(copy.deepcopy(self.list_color[randint(0, len(self.list_color) - 1)]))
        self.block = copy.deepcopy(self.block_suit[0])
        self.color = copy.deepcopy(self.color_suit[0])
        self.block_position = [0, NB_COL // 2 - len(self.block[0]) // 2]

    def detect_line(self):
        line_delete = 0
        for index, row in enumerate(self.grid):
            if all(row):
                self.grid.pop(index)
                self.grid.insert(0, [0] * NB_COL)
                line_delete += 1
        self.score += self.win_point[line_delete]


# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TETRIS")


#chemin relatif :
current_dir = os.path.dirname(__file__)  # Répertoire du script pong.py
image_path_resume = os.path.join(current_dir, 'img', 'button_resume.png')
image_path_quit = os.path.join(current_dir, 'img', 'button_quit.png')

#image bouton 
resume_img = pygame.image.load(image_path_resume).convert_alpha()
quit_img = pygame.image.load(image_path_quit).convert_alpha()
resume_button = button.Button(WIDTH // 2 - 100, HEIGHT // 2 - 100, resume_img, 1)
quit_button = button.Button(WIDTH // 2 - 75, HEIGHT // 2 + 50, quit_img, 1)

# Timer setup
timer = pygame.time.Clock()
fall_event = pygame.USEREVENT
pygame.time.set_timer(fall_event, 400)  # adjust the fall speed as needed

# Game loop
running = True
state_menu = True
game = Game(screen)

screen.fill(COLOR_BG)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if not state_menu:
            if event.type == fall_event:
                game.move_fall()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    game.move_right()
                if event.key == pygame.K_LEFT:
                    game.move_left()
                if event.key == pygame.K_DOWN:
                    game.move_fall()
                if event.key == pygame.K_UP:  # ROTATE RIGHT
                    game.rotate_right()
                if event.key == pygame.K_c:  # ROTATE LEFT
                    game.rotate_left()

    if state_menu:
        if resume_button.draw(screen):
            state_menu = False
        if quit_button.draw(screen):
            running = False
            pygame.quit()
            sys.exit()
    else:
        game.draw()

    pygame.display.flip()
    timer.tick(FPS)
