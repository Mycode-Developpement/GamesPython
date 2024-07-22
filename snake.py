"""
- Jeu du Snake crée par Arnaud Grandchamp
- Début : 20/07/2024
- Fin : 20/07/2024
- Durée : 3H-4H
"""

import pygame 
from random import randint

pygame.init()

screen = pygame.display.set_mode((640,560))
pygame.display.set_caption("SNAKE")

NB_COL = 11
NB_ROW = 14
SIZE_CELL = 40

COLOR1 = (35, 155, 86)
COLOR2 = (59, 65, 60)
COLOR_SNAKE = (0, 141, 213)
COLOR_SNAKE2 = (0, 135, 208)
COLOR_APPLE = (204, 41, 54)

surface = pygame.Surface((440,560))

timer = pygame.time.Clock()
USER_EVENT = pygame.USEREVENT
pygame.time.set_timer(USER_EVENT,400)
running = True

class Apple():
    def __init__(self):
        self.x = randint(0, NB_COL-1)
        self.y = randint(0,NB_ROW-1)
  
    def draw_apple(self):
        self.apple = pygame.Rect((self.x*SIZE_CELL)+50, self.y*SIZE_CELL, SIZE_CELL,SIZE_CELL)
        pygame.draw.rect(screen, COLOR_APPLE,self.apple, border_radius=10)
    
    def randomPosition(self):
        while (self.x,self.y) in game.snake.block: 
            self.x = randint(0, NB_COL-1)
            self.y = randint(0,NB_ROW-1)


class Snake():
    def __init__(self):
        self.block = [(4,7), (5,7), (6,7)]
        self.size = len(self.block)
        self.direction = "RIGHT"
        self.new = (0,0)

    def draw_snake(self):
        for i in self.block[:-1]:
            self.case = pygame.Rect(i[0]*SIZE_CELL+50, i[1]*SIZE_CELL, SIZE_CELL, SIZE_CELL)
            pygame.draw.rect(screen, COLOR_SNAKE, self.case, border_radius=5)
        
        self.case = pygame.Rect(self.block[-1][0]*SIZE_CELL+50, self.block[-1][1]*SIZE_CELL, SIZE_CELL, SIZE_CELL)
        pygame.draw.rect(screen, COLOR_SNAKE2, self.case, border_radius=5)

    def moove(self, appleCo):
        self.new = self.block[-1]

        if self.direction == "RIGHT":
            self.block.append((self.new[0]+1, self.new[1]))
        
        elif self.direction == "LEFT":
            self.block.append((self.new[0]-1, self.new[1]))

        elif self.direction == "UP":
            self.block.append((self.new[0], self.new[1]-1))
        
        elif self.direction == "DOWN":
            self.block.append((self.new[0], self.new[1]+1))
        
        if not self.block[-1][0] in range(0,NB_COL) or not self.block[-1][1] in range(0,NB_ROW):
            game.restart()
        
        for block in self.block[:-1]:
            if block == self.block[-1]:
                game.restart()
        
        if self.block[-1] != appleCo:
            self.block.pop(0)
            return True
        self.size = len(self.block)
        return False


class Game():
    def __init__(self):
        self.score_nb = 0
        
        self.snake = Snake()
        self.apple = Apple()

        self.font = pygame.font.Font(None, 30)
        self.text = f"Score : {self.score_nb}"
        self.text_score = self.font.render(self.text, True, pygame.Color("black"))
        self.texte_rect = self.text_score.get_rect()
        
    def update(self):
        self.apple.draw_apple()
        self.snake.draw_snake()
        screen.blit(self.text_score, (510,150), self.texte_rect)

    def mooveSnake(self):
        if not self.snake.moove((self.apple.x,self.apple.y)):
            self.apple.randomPosition()
            self.score()

    def restart(self):
        self.snake = Snake()
        self.apple = Apple()
        self.score_nb = 0

    def score(self):
        self.score_nb = self.snake.size - 3
        self.text = f"Score : {self.score_nb}"
        self.text_score = self.font.render(self.text, True, pygame.Color("black"))
        self.texte_rect = self.text_score.get_rect()

def grille():
    """fonction qui permet de tracer le cadrillage"""
    for i in range(NB_COL):
        for j in range(NB_ROW):
            case = pygame.Rect(i*SIZE_CELL+50, j*SIZE_CELL, SIZE_CELL, SIZE_CELL)
            pygame.draw.rect(screen, COLOR2, case, width=1)
        

game = Game()

while running: 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            screen.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction != "DOWN":
                    game.snake.direction = "UP"
            if event.key == pygame.K_DOWN:
                if game.snake.direction != "UP":
                    game.snake.direction = "DOWN"
            if event.key == pygame.K_LEFT:
                if game.snake.direction != "RIGHT":
                    game.snake.direction = "LEFT"
            if event.key == pygame.K_RIGHT:
                if game.snake.direction != "LEFT":
                    game.snake.direction = "RIGHT"

        if event.type == USER_EVENT:
            game.mooveSnake()

    
    screen.fill(pygame.Color("white"))
    surface.fill(COLOR1)
    screen.blit(surface, (50,0))
    
    #grille()
    game.update()
    pygame.display.update()

    timer.tick(60)