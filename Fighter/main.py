"""
Jeu de combat 1 contre 1
Début : 04/08
FIN : 09/08
DUREE : 12 Heures
"""

import pygame, sys
import os
from fighter import Fighter

pygame.init()
pygame.mixer.init()
# Initialiser le module joystick
pygame.joystick.init()

class Game():
    def __init__(self):
        # Initialiser les manettes
        self.joystick1 = None
        self.joystick2 = None
        self.icon1 = icon_clavier
        self.icon2= icon_clavier
        self.init_joysticks()

        #load player
        self.fighter1 = Fighter(150,300, sprite_fighters, sprite_by_lines, data_sprite, True, self, shurigen, KEYS_PLAYER1, 1)
        self.fighter2 = Fighter(800,300, sprite_fighters, sprite_by_lines, data_sprite, True, self, shurigen, KEYS_PLAYER2, 2)
        self.all_fighters = pygame.sprite.Group(self.fighter1,self.fighter2)

        #health bar 
        self.health_bar_rect = pygame.Rect(100, 25, 254, 74)
        self.health_bar_rect2 = pygame.Rect(WIDTH-354, 25, 254, 74)
        self.health_bar_color = pygame.Rect(102, 27, 250, 70)
        self.health_bar_color2 = pygame.Rect(WIDTH-352, 27, 250, 70)

        #energy bar 
        self.energy_bar_rect = pygame.Rect(100, 110, 204, 34)
        self.energy_bar_rect2 = pygame.Rect(WIDTH-354, 110, 204, 34)

        #font / text 
        self.font = pygame.font.SysFont('Calibri', 33)
        self.fontTitle = pygame.font.SysFont(PATH_FONT, 100)
        self.text_restart = self.font.render("Press SPACE to PLAY", True, WHITE)
        self.text_mycode = self.font.render("Made by @Mycode-Developpement", True, WHITE)
        self.text_player1 = self.font.render("J1", True, BLUE)
        self.text_player2 = self.font.render("J2", True, YELLOW)

        #point
        self.score = [0,0] #player1 / player2
        
        #const
        self.state_menu = True
        self.is_lunch = False

        self.all_text = ["", "3", "2", "1", "FIGHT"]

        #anim start
        self.animation_time = 1000  # Temps en millisecondes pour changer de frame
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def init_joysticks(self):
        # Vérifier combien de manettes sont connectées
        joystick_count = pygame.joystick.get_count()

        if joystick_count > 0:
            # Initialiser la première manette si disponible
            self.joystick2= pygame.joystick.Joystick(0)
            self.joystick2.init()
            self.icon2 = icon_manette
        
        if joystick_count > 1:
            # Initialiser la deuxième manette si disponible
            self.joystick1 = pygame.joystick.Joystick(1)
            self.joystick1.init()
            self.icon1 = icon_manette


    def start(self):
        self.state_menu = False
        self.fighter1.start()
        self.fighter2.start()
    
    def move_func(self):
        # Récupérer l'état de toutes les touches
        keys = pygame.key.get_pressed()

        self.fighter1.move(self.fighter2, screen, keys, self.joystick1)
        self.fighter2.move(self.fighter1, screen, keys, self.joystick2)
        #self.fighter2.animations()
    
    def get_color(self, fighter):
        if fighter.hyper:
            return PURPLE
        elif fighter.is_hyper:
            return PURPLE2
        else:
            return RED

    def draw(self): 
        color1 = self.get_color(self.fighter1)
        color2 = self.get_color(self.fighter2)

        self.health_bar = pygame.Rect(102, 27, (250/100)*self.fighter1.health, 70)
        self.health_bar2 = pygame.Rect(WIDTH-352, 27, (250/100)*self.fighter2.health, 70)

        self.energy_bar = pygame.Rect(102, 112, self.fighter1.energy*2, 30)
        self.energy_bar2 = pygame.Rect(WIDTH-352, 112, self.fighter2.energy*2, 30)

       
       #health bar
        pygame.draw.rect(screen, WHITE, self.health_bar_rect, width=2, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.health_bar_rect2, width=2, border_radius=10)
        pygame.draw.rect(screen, YELLOW, self.health_bar_color, border_radius=10)
        pygame.draw.rect(screen, YELLOW, self.health_bar_color2, border_radius=10)
        pygame.draw.rect(screen, color1, self.health_bar, border_radius=10)
        pygame.draw.rect(screen, color2, self.health_bar2, border_radius=10)

        #energy bar
        pygame.draw.rect(screen, WHITE, self.energy_bar_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.energy_bar_rect2, border_radius=10)
        pygame.draw.rect(screen, BLUE, self.energy_bar, border_radius=10)
        pygame.draw.rect(screen, YELLOW, self.energy_bar2, border_radius=10)

        #LINE GAME 
        pygame.draw.aaline(screen, WHITE, (0,450),(WIDTH,450))

        #Player Score
        player1_score = self.fontTitle.render(str(self.score[0]), True, BLUE)
        player2_score = self.fontTitle.render(str(self.score[1]), True, YELLOW)

        screen.blit(player1_score, (35, 30))
        screen.blit(player2_score, (WIDTH-75, 30))
        #player name 
        screen.blit(self.text_player1, (self.fighter1.rect.centerx,self.fighter1.rect.y - 35))
        screen.blit(self.text_player2, (self.fighter2.rect.centerx,self.fighter2.rect.y - 35))

        if self.state_menu and not self.is_lunch:
            screen.blit(self.text_restart, (WIDTH//2-self.text_restart.get_width()//2, 50))

    def menu_animations(self):
        #vérifier si le joueur a lancé la partie 
        if self.is_lunch:
            #le décompte est lancée
            now = pygame.time.get_ticks()  # Obtenir le temps actuel
            if now - self.last_update > self.animation_time:  # Vérifier si le temps écoulé est supérieur au temps d'animation
                self.last_update = now
                self.frame += 1
                if self.frame > len(self.all_text)-1:
                    self.frame = 0
                    self.is_lunch = False
                    intro_music.stop()
                    self.start() #lancement de la partie 
        
            #affichage du décompte 
            self.text_decompte = self.fontTitle.render(self.all_text[self.frame], True, YELLOW)
            screen.blit(self.text_decompte, (WIDTH//2-self.text_decompte.get_width()//2, HEIGHT//2))

        #credit 
        if not self.is_lunch:
            screen.blit(self.text_mycode, (WIDTH-self.text_mycode.get_width()-25, HEIGHT-50))
        #animer les joueurs sans les mouvement de celle-ci 
        self.fighter1.animations(game.fighter2, screen)
        self.fighter2.animations(game.fighter1, screen)

    
    def dead(self, num):
        self.score[num-1] += 1 
        self.state_menu = True
    
    def super_son(self):
        #fonction pour lancer la musique lorsque le suyper est obtenu 
        son_bonus.stop()
        son_bonus.play()

    def sword_son(self):
        #fonction pour lancer la musique lorsque le suyper est obtenu 
        son_effect_sword.play()
    
    def activ_super(self):
        son_effect_super.stop()
        son_effect_super.play()
    
    def fin_super(self):
        son_effect_super.stop()
    
    def son_shurigen(self):
        son_effet_shurigen.play()


#constante 
WIDTH, HEIGHT = 1080, 600
FPS = 60
YELLOW = (241, 196, 15)
RED = (231, 76, 60)
WHITE = (236, 240, 241)
PURPLE = (125, 60, 152)
PURPLE2 = (74, 35, 90)
BLUE = (52, 152, 219)

# Définir les touches pour chaque joueur
KEYS_PLAYER1 = {
    'left': pygame.K_q,
    'right': pygame.K_d,
    'up': pygame.K_z,
    'attack': pygame.K_a,
    'attack2': pygame.K_e,
    'combo' : pygame.K_s
}

KEYS_PLAYER2 = {
    'left': pygame.K_k,
    'right': pygame.K_m,
    'up': pygame.K_o,
    'attack': pygame.K_i,
    'attack2': pygame.K_p,
    'combo' : pygame.K_l
}

#Screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("FIGHTER")

#current dir
current_dir = os.path.dirname(__file__)  # Répertoire du script 

#load image
sprite_fighters = pygame.image.load(os.path.join(current_dir, 'assets', 'img', 'perso.png')).convert_alpha()
sprite_by_lines = [2,2,4,8,6,8,3,8,8]
data_sprite = (192,192) # 1: WIDTh / 2:HEIGHT

#load icon 
icon_manette = pygame.image.load(os.path.join(current_dir, 'assets', 'img', 'Joystickfullgame_Joystickllena_5562.png')).convert_alpha()
icon_clavier = pygame.image.load(os.path.join(current_dir, 'assets', 'img', 'keyboard_5643.png')).convert_alpha()

#load font path
PATH_FONT = os.path.join(current_dir, 'assets','font', 'Anton-Regular.ttf')

#shurigen load image
shurigen = pygame.image.load(os.path.join(current_dir, 'assets','img', 'arme1.png')).convert_alpha()

#load sound 
son_effect_super = pygame.mixer.Sound(os.path.join(current_dir, 'assets','audio', '441123__xhale303__epic-hybrid-intro2.wav'))
son_bonus = pygame.mixer.Sound(os.path.join(current_dir, 'assets','audio', 'game-bonus-144751.mp3'))
son_effect_sword = pygame.mixer.Sound(os.path.join(current_dir, 'assets','audio',  'sword.wav'))
son_effet_shurigen = pygame.mixer.Sound(os.path.join(current_dir, 'assets','audio',  'fast-whoosh-118248.mp3'))
son_effet_shurigen.set_volume(0.4)
son_effect_sword.set_volume(0.1)

#intro music
intro_music = pygame.mixer.Sound(os.path.join(current_dir, 'assets','audio', 'time-has-come-203034.mp3'))

#time
timer = pygame.time.Clock()

#game loop
running = True

game = Game()

square1 = pygame.Rect(50, HEIGHT-110, 50,50)
square2 = pygame.Rect(50, HEIGHT-50, 50,50)
icon1, icon2 = game.icon1, game.icon2

#lunch music
intro_music.play()

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.state_menu:
                if event.key == pygame.K_SPACE: 
                    game.is_lunch = True
        
    screen.fill((0,0,0))  

    if not game.state_menu: 
        game.move_func()
    else: 
        game.menu_animations()
        #affichage des icon
        if not game.is_lunch:
            pygame.draw.rect(screen, WHITE, square1, border_radius=30)
            pygame.draw.rect(screen, WHITE, square2,border_radius=30)
            screen.blit(icon1, (square1.x + 8, square1.y + 8))
            screen.blit(icon2, (square2.x + 8, square2.y + 8))
            screen.blit(game.text_player1, (120,HEIGHT-100))
            screen.blit(game.text_player2, (120,HEIGHT-40))
    #dessiner
    
    game.draw()  
    game.all_fighters.draw(screen)

    if not game.state_menu:
        for fighter in game.all_fighters:
            for shurigen in fighter.all_shurigens:
                shurigen.move()
            fighter.all_shurigens.draw(screen)


    pygame.display.update()    
    timer.tick(FPS)


