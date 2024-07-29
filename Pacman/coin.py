import pygame
import os
from random import randint

class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x ,y):
        super().__init__()
        self.game = game
        self.images = [(0,0),(16,0), (32,0), (48,0), (64,0), (80, 0), (96, 0), (112, 0)]
        self.pos = randint(0, len(self.images)-1)
        self.animation_time = 200  # Temps en millisecondes pour changer de frame
        self.last_update = pygame.time.get_ticks()

        # Charge la feuille de sprites
        self.tileset = pygame.image.load(self.get_image_path(f"assets/Coin.png")).convert_alpha()
        
        # Définir la taille du sprite à extraire
        sprite_width = 16
        sprite_height = 16
        
        # Définir la position du sprite sur la feuille
        sprite_x = 0  # Par exemple, le premier sprite sur la feuille
        sprite_y = 0 # Par exemple, le premier sprite sur la feuille
        
        # Extraire le sprite souhaité
        self.image = self.tileset.subsurface(pygame.Rect(sprite_x, sprite_y, sprite_width, sprite_height))
        
        # Redimensionner le sprite à la taille de la cellule
        self.image = pygame.transform.scale(self.image, (SIZE_CELL, SIZE_CELL))
        
        # Définir le rectangle de la sprite
        self.rect = self.image.get_rect()
        self.rect.x = x * SIZE_CELL
        self.rect.y = y * SIZE_CELL

    def detect_coll(self):
        if self.game.check_collision_player(self):
            if len(self.game.all_coins) == 0:
                self.game.restart()
            self.kill()

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
            self.image = pygame.transform.scale(self.image, (SIZE_CELL, SIZE_CELL))
    
    
    def get_image_path(self, relative_path):
        """Retourne le chemin absolu de l'image en fonction du chemin relatif."""
        base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)
    
SIZE_CELL = 30