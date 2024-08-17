import pygame

class Block(pygame.sprite.Sprite):
     def __init__(self, x ,y, image, DEMI=False):
          super().__init__()
          self.image = image
          if DEMI:
               self.image = pygame.transform.scale(self.image, (30,15))
          else:
               self.image = pygame.transform.scale(self.image, (30,30))
          self.rect = self.image.get_rect()
          self.rect.x = x
          self.rect.y = y 