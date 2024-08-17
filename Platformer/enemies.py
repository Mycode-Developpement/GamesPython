import pygame

class Enemie(pygame.sprite.Sprite):
    def __init__(self, x, y, images, sprite_by_line,data, speed, game, HORIZONTAL=True):
        super().__init__()
        self.data = data
        self.images = self.split_image(sprite_by_line, images)
        self.image = self.images[0]
        self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = "RIGHT" if HORIZONTAL else "UP"
        self.speed = speed
        self.game = game
        self.horizontal = HORIZONTAL

        #animations 
        self.last_update = pygame.time.get_ticks()
        self.animation_time = 100  # Temps en millisecondes pour changer de frame

        #remonter pour pas qu'il touche sol 


    def animations(self):
        """while self.game.detect_collision(self, self.game.all_blocks):
            self.rect.y -= 1"""
        self.move()

        now = pygame.time.get_ticks()  # Obtenir le temps actuel
        if now - self.last_update > self.animation_time:  # Vérifier si le temps écoulé est supérieur au temps d'animation
            self.last_update = now  # Mettre à jour le dernier temps
            
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = 0
            self.image = self.images[self.frame]

            if self.direction == "LEFT":
                    self.image = pygame.transform.flip(self.image, True, False)
        

    def move(self):
        if self.horizontal:
            self.rect.y +=1 #vérifier s'il n'y a plus de sol en dessous
            
            if not self.game.detect_collision(self, self.game.all_blocks):
                if self.direction == "LEFT":
                    self.direction = "RIGHT"
                else:
                    self.direction = "LEFT"

            self.rect.y -=1
            #vérifier s'il touche block sur coté
            if self.direction == "RIGHT":
                self.rect.x += self.speed
                if self.game.detect_collision(self, self.game.all_blocks):
                    self.rect.x -= self.speed
                    self.direction = "LEFT"
            
            elif self.direction == "LEFT":
                self.rect.x -= self.speed
                if self.game.detect_collision(self, self.game.all_blocks):
                    self.rect.x += self.speed
                    self.direction = "RIGHT"
        else :
            if self.direction == "DOWN":
                self.rect.y += self.speed
                if self.game.detect_collision(self, self.game.all_blocks):
                    self.rect.y -= self.speed
                    self.direction = "UP"
            
            elif self.direction == "UP":
                self.rect.y -= self.speed
                if self.game.detect_collision(self, self.game.all_blocks):
                    self.rect.y += self.speed
                    self.direction = "DOWN"

    
    def split_image(self, sprite_by_line, images):
        sprite_images = []
        for x in range(sprite_by_line):
            image = images.subsurface(pygame.Rect(x*self.data[0], 0, self.data[0], self.data[1]))
            #image = pygame.transform.scale(image, (28,28))
            sprite_images.append(image)
        return sprite_images