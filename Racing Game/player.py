import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, path, game):
        super().__init__()
        self.game = game
        self.speed = 3
        self.tileset = pygame.image.load(path).convert_alpha()
        
        sprite_width = 64
        sprite_height = 100
        
        # Définir la position du sprite sur la feuille
        sprite_x = 0  # Par exemple, le premier sprite sur la feuille
        sprite_y = 0 # Par exemple, le premier sprite sur la feuille
        
        # Extraire le sprite souhaité
        self.image = self.tileset.subsurface(pygame.Rect(sprite_x, sprite_y, sprite_width, sprite_height))
        self.image = pygame.transform.scale(self.image, (70, 112))
        self.rect = self.image.get_rect()

        self.rect.x = 270
        self.rect.y = 525

    
    def move_right(self):
        if self.rect.x <= 450:
            self.rect.x += self.speed

    def move_left(self):
        if self.rect.x >= 100:
            self.rect.x -= self.speed
    
    def move_top(self):
        if self.rect.y >= 0:
            self.rect.y -= self.speed
    
    def move_down(self):
        if self.rect.y <= 550:
            self.rect.y += self.speed

    def collision(self):
        self.game.loose()
        self.kill()