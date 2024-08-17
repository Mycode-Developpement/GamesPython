import pygame

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed



    def move(self):
        self.rect.x -= self.speed
        if self.rect.x <= -50:
            self.kill()