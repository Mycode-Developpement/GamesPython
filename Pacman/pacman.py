"""
JEU Pacman 
DEBUT : 27/07
FIN : 29/07
DUREE : 6H-7H
"""

import pygame, sys, os
from block import Block
from player import Player
from ghost import Ghost
from coin import Coin
from random import shuffle
import button

pygame.init()

class Game():
    def __init__(self):
        self.best_score = 0
        self.start()
        
    def start(self):
        self.color_spawn = ["blueGhost", "greenGhost", "orangeGhost", "redGhost", "yellowGhost"]
        shuffle(self.color_spawn)

        self.player = Player(self)
        self.all_coins = pygame.sprite.Group()
        self.all_player = pygame.sprite.Group(self.player)
        self.all_block = pygame.sprite.Group()
        self.all_ghost = pygame.sprite.Group(Ghost(self, self.color_spawn[0], self.player))
        
        self.color_spawn.pop(0)
        self.spawn = 0
        self.max_bar = pygame.Rect(10, HEIGHT-40, WIDTH-20, 20)
        self.bar = pygame.Rect(10, HEIGHT-30, (WIDTH//20)*self.spawn, 18)
        self.build_terrain()
 
    def build_terrain(self):
        for y, row in enumerate(MAP):
            for x, letter in enumerate(row):
                if letter == "M":  # Block
                    self.all_block.add(Block(x+1, y+1))
                elif letter == "C": #coin
                    self.all_coins.add(Coin(self,x+1, y+1))
        

    
    def spawn_ghost(self):
        self.spawn += 1
        if self.spawn == 20:
            if len(self.color_spawn) != 0:
                self.all_ghost.add(Ghost(self, self.color_spawn[0], self.player))
                self.color_spawn.pop(0)

            self.spawn = 0
        self.bar = pygame.Rect(15, HEIGHT-35, ((WIDTH-10)//20)*self.spawn, 10)
        
        
    
    def check_collision_block(self):
        return pygame.sprite.spritecollideany(self.player, self.all_block)
    
    def check_collision_block2(self, sprite):
        return pygame.sprite.spritecollideany(sprite, self.all_block)

    
    def check_collision_coin(self):
        return pygame.sprite.spritecollideany(self.player, self.all_coins)
    
    def check_collision_ghost(self):
        return pygame.sprite.spritecollideany(self.player, self.all_ghost)
    
    def check_collision_player(self,sprite):
        return pygame.sprite.spritecollideany(sprite,self.all_player)
    
    def restart(self):
        global state_menu
        state_menu = True
        if self.player.score > self.best_score:
            self.best_score = self.player.score
        self.start()


#Constante :
WIDTH, HEIGHT = 920, 650
FPS = 60
SIZE_CELL = 30
BG_YELLOW = (255,242,0)

# M -> Wall
# O -> empty
# C -> Coin
MAP = [
    ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'],
    ['M', 'O', 'C', 'O', 'C', 'C', 'C', 'O', 'M', 'O', 'C', 'C', 'C', 'O', 'C', 'C', 'M', 'C', 'O', 'C', 'C', 'C', 'O', 'C', 'O', 'M'],
    ['M', 'C', 'M', 'M', 'M', 'M', 'C', 'C', 'M', 'C', 'M', 'M', 'M', 'M', 'C', 'O', 'M', 'C', 'M', 'M', 'M', 'M', 'C', 'M', 'O', 'M'],
    ['M', 'C', 'C', 'O', 'C', 'M', 'C', 'C', 'M', 'C', 'M', 'O', 'O', 'O', 'C', 'O', 'M', 'C', 'M', 'O', 'C', 'O', 'O', 'M', 'C', 'M'],
    ['M', 'C', 'M', 'C', 'M', 'M', 'C', 'C', 'M', 'C', 'M', 'O', 'M', 'O', 'C', 'O', 'M', 'C', 'M', 'O', 'M', 'C', 'C', 'M', 'O', 'M'],
    ['M', 'O', 'C', 'C', 'O', 'C', 'C', 'O', 'M', 'O', 'M', 'C', 'C', 'C', 'C', 'O', 'M', 'C', 'M', 'O', 'C', 'O', 'C', 'O', 'C', 'M'],
    ['M', 'C', 'M', 'M', 'C', 'M', 'M', 'O', 'M', 'O', 'M', 'M', 'M', 'O', 'M', 'M', 'M', 'O', 'M', 'M', 'C', 'M', 'M', 'M', 'C', 'M'],
    ['M', 'C', 'O', 'O', 'C', 'M', 'C', 'C', 'M', 'C', 'O', 'O', 'C', 'O', 'C', 'C', 'M', 'C', 'C', 'C', 'O', 'M', 'O', 'O', 'C', 'M'],
    ['M', 'M', 'M', 'M', 'O', 'M', 'M', 'M', 'M', 'O', 'M', 'M', 'M', 'M', 'C', 'M', 'M', 'O', 'M', 'O', 'M', 'M', 'M', 'M', 'M', 'M'],
    ['M', 'O', 'C', 'O', 'C', 'O', 'C', 'C', 'C', 'C', 'C', 'O', 'C', 'C', 'O', 'O', 'O', 'C', 'O', 'C', 'O', 'O', 'C', 'C', 'O', 'M'],
    ['M', 'C', 'M', 'M', 'C', 'M', 'M', 'O', 'M', 'M', 'C', 'M', 'M', 'O', 'M', 'M', 'C', 'M', 'M', 'O', 'M', 'M', 'C', 'M', 'M', 'M'],
    ['M', 'C', 'O', 'O', 'O', 'O', 'O', 'C', 'O', 'O', 'C', 'C', 'C', 'C', 'O', 'C', 'O', 'O', 'C', 'O', 'C', 'O', 'O', 'C', 'O', 'M'],
    ['M', 'C', 'M', 'M', 'M', 'M', 'M', 'O', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'O', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'O', 'M'],
    ['M', 'C', 'C', 'C', 'O', 'C', 'C', 'C', 'O', 'O', 'O', 'O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'C', 'O', 'M'],
    ['M', 'O', 'M', 'M', 'M', 'M', 'O', 'C', 'M', 'M', 'O', 'O', 'C', 'C', 'M', 'M', 'M', 'M', 'O', 'O', 'M', 'M', 'M', 'M', 'O', 'M'],
    ['M', 'C', 'C', 'O', 'O', 'M', 'C', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'O', 'C', 'C', 'C', 'C', 'C', 'O', 'M', 'C', 'C', 'O', 'M'],
    ['M', 'M', 'M', 'M', 'C', 'M', 'M', 'M', 'M', 'C', 'M', 'M', 'M', 'M', 'C', 'M', 'M', 'M', 'M', 'C', 'M', 'M', 'M', 'M', 'M', 'M'],
    ['M', 'C', 'O', 'C', 'O', 'O', 'C', 'C', 'C', 'O', 'C', 'C', 'O', 'O', 'C', 'O', 'C', 'C', 'C', 'O', 'C', 'C', 'O', 'O', 'O', 'M'],
    ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
]

#page
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pacman")

#time
timer = pygame.time.Clock()
EVENT_SPAWN = pygame.USEREVENT
pygame.time.set_timer(EVENT_SPAWN,1000)

#texte 
font = pygame.font.SysFont("Comic Sans", 55)
font2 = pygame.font.SysFont("Comic Sans", 18)
title = font.render("PACMAN", True, pygame.Color("black"))


#chemin relatif :
current_dir = os.path.dirname(__file__)  # Répertoire du script pong.py
image_path_resume = os.path.join(current_dir, 'assets', 'play.png')
image_path_quit = os.path.join(current_dir, 'assets', 'quit.png')

#image bouton 
resume_img = pygame.image.load(image_path_resume).convert_alpha()
quit_img = pygame.image.load(image_path_quit).convert_alpha()
resume_button = button.Button(WIDTH // 2 - 175, HEIGHT // 2 - 100, resume_img, 1)
quit_button = button.Button(WIDTH // 2 - 175, HEIGHT // 2 + 50, quit_img, 1)

#loop game
state_menu = True
running = True

game = Game()

text = font2.render(f"Score : {game.player.score}", True, (0,0,0))
text_mycode = font2.render('Jeu crée par Mycode Developpement', True, pygame.Color("black"))


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        if not state_menu:

            if event.type == EVENT_SPAWN:
                game.spawn_ghost()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.player.change_direction("UP")
                
                if event.key == pygame.K_DOWN:
                    game.player.change_direction("DOWN")

                if event.key == pygame.K_LEFT:
                    game.player.change_direction("LEFT")
                
                if event.key == pygame.K_RIGHT:
                    game.player.change_direction("RIGHT")

    
    if state_menu: #si le menu est activée 
        screen.fill(BG_YELLOW)
        #texte 
        text_best = font2.render(f"Meilleur Score : {game.best_score}", True, (0,0,0))
        #affichage 
        
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
        screen.blit(text_best, (WIDTH//2-text_best.get_width()//2,110))
        screen.blit(text, (WIDTH//2-text.get_width()//2,150))
        screen.blit(text_mycode, (WIDTH//2-text_mycode.get_width()//2,HEIGHT-50))

        if resume_button.draw(screen): #bouton play appuyé 
            state_menu = False
        
        if quit_button.draw(screen): #bouton exit cliqué
            running = False
            pygame.quit()
            sys.exit()
    
    else:
        screen.fill((255,255,255))
        #texte 
        text = font2.render(f"Score : {game.player.score}", True, (0,0,0))
        #affichage texte    
        screen.blit(text, (WIDTH-100,HEIGHT//2))
        #dessiner élément rect du jeu 
        pygame.draw.rect(screen, (0,0,0), game.max_bar, width=5)
        pygame.draw.rect(screen, BG_YELLOW, game.bar)
        
        game.all_block.draw(screen) #dessiner le terrain 
        game.all_coins.draw(screen) #dessiner les pièces
        game.all_ghost.draw(screen) #dessiner les fantomes
        game.all_player.draw(screen) #dessiner le joueur 
        #mouvement du joueur
        game.player.move()
        game.player.animations()

        for ghost in game.all_ghost:
            ghost.move()
            ghost.animations()
        
        for coin in game.all_coins:
            coin.detect_coll()
            coin.animations()

    pygame.display.update()
    timer.tick(FPS)


