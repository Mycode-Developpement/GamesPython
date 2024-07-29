import pygame
import os
from random import randint

class Ghost(pygame.sprite.Sprite):
    def __init__(self, game, name, player):
        super().__init__()
        self.game = game
        self.name = name
        self.player = player
        self.direction = ""
        self.directions = []
        self.speed = 1
        self.images = [(0,0),(16,0), (32,0), (48,0), (64,0), (80, 0), (96, 0), (112, 0)]
        self.pos = 0
        self.animation_time = 100  # Temps en millisecondes pour changer de frame
        self.last_update = pygame.time.get_ticks()

        # Charge la feuille de sprites
        self.tileset = pygame.image.load(self.get_image_path(f"assets/{self.name}.png")).convert_alpha()
        # Définir la taille du sprite à extraire
        sprite_width = 16
        sprite_height = 16
        
        # Définir la position du sprite sur la feuille
        sprite_x = self.images[self.pos][0]  # Par exemple, le premier sprite sur la feuille
        sprite_y = self.images[self.pos][1] # Par exemple, le premier sprite sur la feuille
        
        # Extraire le sprite souhaité
        self.image = self.tileset.subsurface(pygame.Rect(sprite_x, sprite_y, sprite_width, sprite_height))
        
        # Redimensionner le sprite à la taille de la cellule
        self.image = pygame.transform.scale(self.image, (25, 25))
        
        # Définir le rectangle de la sprite
        self.rect = self.image.get_rect()
        self.rect.x = 23 * SIZE_CELL + 5
        self.rect.y = 3 * SIZE_CELL + 5

    def move(self):
        self.directions= [self.detect_move_up(), self.detect_move_down(), self.detect_move_right(), self.detect_move_left()]
        ##print("Directions avant tri :", self.directions)
        
        # Correction ici: 'self.direction' devrait être 'self.directions'
        self.directions = sorted(self.directions, key=lambda x: x['DISTANCE'], reverse=False)
        ##print("Directions après tri :", self.directions)

        for direction in self.directions:

            if direction["DIRECTION"] == False:
                pass

            elif direction["DIRECTION"] == "UP":
                self.rect.y -= self.speed
                break

            elif direction["DIRECTION"] == "DOWN":
                self.rect.y += self.speed
                break
            
            elif direction["DIRECTION"] == "LEFT":
                self.rect.x -= self.speed
                break

            elif direction["DIRECTION"] == "RIGHT":
                self.rect.x += self.speed    
                break        


    def detect_move_right(self):
        detect = {"DIRECTION":"RIGHT", "DISTANCE":10000}
        self.rect.x += self.speed*2
        if self.game.check_collision_block2(self):
            
            detect["DIRECTION"] = False
        
        else:
            detect["DISTANCE"] = (abs(self.player.rect.x-self.rect.x)+abs(self.player.rect.y-self.rect.y))
        
        self.rect.x -= self.speed
        return detect
    
    def detect_move_left(self):
        detect = {"DIRECTION":"LEFT", "DISTANCE":10000}
        self.rect.x -= self.speed*2
        if self.game.check_collision_block2(self):
            detect["DIRECTION"] = False
        else:
            detect["DISTANCE"] = (abs(self.player.rect.x-self.rect.x)+abs(self.player.rect.y-self.rect.y))
        
        self.rect.x += self.speed
        return detect
    
    def detect_move_up(self):
        detect = {"DIRECTION":"UP", "DISTANCE":10000}
        self.rect.y -= self.speed*2
        if self.game.check_collision_block2(self):
            detect["DIRECTION"] = False
        else:
            detect["DISTANCE"] = (abs(self.player.rect.x-self.rect.x)+abs(self.player.rect.y-self.rect.y))
        
        self.rect.y += self.speed
        return detect
    
    def detect_move_down(self):
        detect = {"DIRECTION":"DOWN", "DISTANCE":10000}
        self.rect.y += self.speed*2
        if self.game.check_collision_block2(self):
            detect["DIRECTION"] = False
        else:
            detect["DISTANCE"] = (abs(self.player.rect.x-self.rect.x)+abs(self.player.rect.y-self.rect.y))
        
        self.rect.y -= self.speed
        return detect
    

    def animations(self):
        now = pygame.time.get_ticks()  # Obtenir le temps actuel
        if now - self.last_update > self.animation_time:  # Vérifier si le temps écoulé est supérieur au temps d'animation
            self.last_update = now  # Mettre à jour le dernier temps
            self.pos += 1  # Passer à l'image suivante
            if self.pos > len(self.images) - 1:  # Si la position dépasse le nombre d'images, revenir à la première image
                self.pos = 0

            # Définir la taille du sprite à extraire
            sprite_width = 16
            sprite_height = 16

            # Définir la position du sprite sur la feuille
            sprite_x = self.images[self.pos][0]
            sprite_y = self.images[self.pos][1]

            # Extraire le sprite souhaité
            self.image = self.tileset.subsurface(pygame.Rect(sprite_x, sprite_y, sprite_width, sprite_height))

            # Redimensionner le sprite à la taille de la cellule
            self.image = pygame.transform.scale(self.image, (25, 25))

    
    
    def get_image_path(self, relative_path):
        """Retourne le chemin absolu de l'image en fonction du chemin relatif."""
        base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)
    
SIZE_CELL = 30