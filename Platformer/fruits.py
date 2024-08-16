import pygame
from random import randint

class Fruit(pygame.sprite.Sprite):
    def __init__(self, x , y , images):
        super().__init__()
        self.images = images
        self.frame = randint(0, len(self.images)-1)
        self.image = images[self.frame]
        
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y 

        self.animation_time = 100  # Temps en millisecondes pour changer de frame
        self.last_update = pygame.time.get_ticks()

    
    def animations(self):
        now = pygame.time.get_ticks()  # Obtenir le temps actuel
        if now - self.last_update > self.animation_time:  # Vérifier si le temps écoulé est supérieur au temps d'animation
            self.last_update = now  # Mettre à jour le dernier temps
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = 0
            
            #changer l'image
            self.image = self.images[self.frame] 