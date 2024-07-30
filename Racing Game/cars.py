import pygame, os
from random import randint

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, game):
        super().__init__()
        self.speed = speed
        self.game = game
        self.tileset = TILESET.convert_alpha()
        
        self.all_car_coor = [(0,0), (70, 0), (135,0), (205,0), (0,100),(68,100), (134,100),(200,100),(0,200),(68,200), (136,200),(0,200),(204,200), (0,300), (0,400),(0,500),(0,600) ]
        self.car_coor = self.all_car_coor[randint(0,len(self.all_car_coor)-1)] 
        # Définir la position du sprite sur la feuille
        sprite_x = self.car_coor[0]  # Par exemple, le premier sprite sur la feuille
        sprite_y =  self.car_coor[1]  # Par exemple, le premier sprite sur la feuille
        
        # Extraire le sprite souhaité
        self.image = self.tileset.subsurface(pygame.Rect(sprite_x, sprite_y, 65, 100))
        #self.image = pygame.transform.rotate(self.image, 180)

        self.image = pygame.transform.scale(self.image, (70, 112))
        
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.y += self.speed
        if self.rect.y >= 650:
            self.game.score += 1
            self.kill()

#Charger image 
current_dir = os.path.dirname(__file__)  # Répertoire du script 
IMAGE_PATH_CAR =  os.path.join(current_dir, 'assets', 'voitures.png')
TILESET = pygame.image.load(IMAGE_PATH_CAR)