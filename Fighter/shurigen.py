import pygame

class Shurigen(pygame.sprite.Sprite):

    def __init__(self,x,y, image, speed, opponent, player):
        super().__init__()
        self.speed = speed
        self.opponent = opponent
        self.player = player

        self.origin_image = image
        self.image = image
        self.angle = 0
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x += self.speed
        self.rotate()

        if self.rect.x <= 0 or self.rect.x >= 1060:
            self.kill()
        
        if pygame.sprite.collide_rect(self, self.opponent):
            self.opponent.subir_attaque(3,self.player, 0)
            self.kill()
        
        if pygame.sprite.spritecollide(self, self.opponent.all_shurigens, True):
            self.kill()

    def rotate(self):
        self.angle += 9
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
       