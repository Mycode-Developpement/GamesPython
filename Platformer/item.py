import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, images, sprite_by_line,data, width=30, height=30):
        super().__init__()
        self.data = data
        self.images = self.split_image(sprite_by_line, images)
        self.image = self.images[0]
        self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

        #animations 
        self.last_update = pygame.time.get_ticks()
        self.animation_time = 50  # Temps en millisecondes pour changer de frame


    def animations(self):
        now = pygame.time.get_ticks()  # Obtenir le temps actuel
        if now - self.last_update > self.animation_time:  # Vérifier si le temps écoulé est supérieur au temps d'animation
            self.last_update = now  # Mettre à jour le dernier temps
            
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = 0
            self.image = self.images[self.frame]
            self.image = pygame.transform.scale(self.image, (self.width,self.height))

    def split_image(self, sprite_by_line, images):
        sprite_images = []
        for x in range(sprite_by_line):
            image = images.subsurface(pygame.Rect(x*self.data[0], 0, self.data[0], self.data[1]))
            #image = pygame.transform.scale(image, (28,28))
            sprite_images.append(image)
        return sprite_images