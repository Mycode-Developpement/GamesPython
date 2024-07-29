import pygame
import os

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Charge la feuille de sprites
        self.image = pygame.image.load(self.get_image_path("assets/block.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE_CELL, SIZE_CELL))
        
        # Définir le rectangle de la sprite
        self.rect = self.image.get_rect()
        self.rect.x = x * SIZE_CELL
        self.rect.y = y * SIZE_CELL

    def get_image_path(self, relative_path):
        """Retourne le chemin absolu de l'image en fonction du chemin relatif."""
        base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)
    

SIZE_CELL = 30