"""
- Jeu du Snake crée par Mycode Developpment
- Début : 29/07
- Fin : ---
- Durée : ---
"""

import pygame, sys, os
from player import Player
from cars import Car
from random import randint, choice
import button1

pygame.init()

class Game():
    def __init__(self):
        self.pos = [(125, -90), (270,-105), (400,-100)]
        self.start()
        

    def start(self):
        self.player = Player(IMAGE_PATH_CAR, self) 
        self.all_players = pygame.sprite.Group(self.player)
        self.all_cars = pygame.sprite.Group()
        self.spawn_possibility = [False, False, False, False, 1, 1 ,1 , 2, 2, 2]
        self.bar = 0
        self.score = 0
        self.speed_car = 3
    
    def loose(self):
        global state_menu
        state_menu = True

    def detect_col(self):
        return pygame.sprite.spritecollideany(self.player, self.all_cars)

    def spawn_car(self):
        num = randint(0, len(self.spawn_possibility)-1)
        if self.spawn_possibility[num] == 1:
            num =randint(0,2)
            self.all_cars.add(Car(self.pos[num][0],self.pos[num][1], self.speed_car + randint(0,1), game))
        elif self.spawn_possibility[num] == 2:
            num, num2 =choice(self.spawn_possibility), choice(self.spawn_possibility)
            if num == num2:
                num2 +=1
                if num2 == 3:
                    num2 = 0

            self.all_cars.add(Car(self.pos[num][0],self.pos[num][1], self.speed_car + randint(0,1), game))
            self.all_cars.add(Car(self.pos[num2][0],self.pos[num2][1], self.speed_car + randint(0,1), game))
        
        self.bar += 1
        if self.bar == 10:
            self.speed_car += 0.5
            self.spawn_possibility.pop(0)





#CONSTANTE : 
WIDTH, HEIGHT = 600,650
FPS = 60

state_menu = True

#PAGE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RACING GAME") 

#timer 
timer = pygame.time.Clock()
EVENT_SPAWN = pygame.USEREVENT
pygame.time.set_timer(EVENT_SPAWN, 2000)

#Charger image 
current_dir = os.path.dirname(__file__)  # Répertoire du script 
path = os.path.join(current_dir, 'assets', 'bg_car.png')
IMAGE_BG = pygame.image.load(path)
IMAGE_PATH_CAR =  os.path.join(current_dir, 'assets', 'voitures.png')

current_dir = os.path.dirname(__file__)  # Répertoire du script pong.py
image_path_resume = os.path.join(current_dir, 'assets', 'button_resume.png')
resume_img = pygame.image.load(image_path_resume).convert_alpha()
resume_button = button1.Button(WIDTH//2-100, HEIGHT//2-100., resume_img, 1)

#font 
font = pygame.font.SysFont("Comic Sans", 18)

#loop game 
running = True

#game init 
game = Game()


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit() 
            sys.exit()
        
        if event.type == EVENT_SPAWN:
            game.spawn_car()

    if not state_menu:

        
        # Récupérer l'état de toutes les touches
        keys = pygame.key.get_pressed()

        # Changer la couleur de fond en fonction des touches enfoncées
        if keys[pygame.K_RIGHT]:
            game.player.move_right()
        if keys[pygame.K_LEFT]:
            game.player.move_left()
        if keys[pygame.K_UP]:
            game.player.move_top()
        if keys[pygame.K_DOWN]:
            game.player.move_down()
        
        
        #move bot
        for car in game.all_cars:
            car.move()

        if game.detect_col():
            game.player.collision()
   
        #affichage
        screen.blit(IMAGE_BG, (0,0)) #bg 

        game.all_cars.draw(screen)
        game.all_players.draw(screen)
    
    if state_menu:
        screen.blit(IMAGE_BG, (0,0)) #bg 
        game.all_cars.draw(screen)
        
        for car in game.all_cars:
            car.move()
        if resume_button.draw(screen):
            state_menu = False
            game.start()
    
    text_score = font.render(f"Score: {game.score}", True, (0,0,0))
    screen.blit(text_score,(WIDTH-90,150))
    pygame.display.update()
    timer.tick(FPS)