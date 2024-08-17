import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, images, sprite_by_line, data, game):
        super().__init__()
        self.game = game
        self.data = data
        self.images = self.split_image(sprite_by_line, images)
        self.image = self.images[3][0]
        self.rect = self.image.get_rect()


        #stat
        self.speed = 3

        self.origin_co = (x,y)
        self.animation_time = 50  # Temps en millisecondes pour changer de frame

        self.start()
     

    def start(self):  
        self.frame = 0
        self.fruit = 0
        self.is_life = True

        self.direction = "RIGHT"

        self.flip = False
        self.rect.x = self.origin_co[0]
        self.rect.y = self.origin_co[1]
        #state
        self.is_jumping = False
        self.count_jump = 0

        self.action = 3

        #animations 
        self.last_update = pygame.time.get_ticks()
    
    def move_player(self, key):

        if key[pygame.K_UP] and not self.is_jumping and self.is_life: #jump
            self.is_jumping = True
            self.count_jump = 0
            self.action = 0 #jump
            self.frame = -1
        
        if key[pygame.K_RIGHT] and self.is_life: #right
            self.rect.x += self.speed
            if self.game.detect_collision(self, self.game.all_blocks):
                self.rect.x -= self.speed
            self.direction = "RIGHT"
            self.action = 5
        
        if key[pygame.K_LEFT]  and self.is_life: #left
            self.rect.x -= self.speed
            if self.game.detect_collision(self, self.game.all_blocks):
                self.rect.x += self.speed
            
            self.direction = "LEFT"
            self.action = 5

        #jump
        if self.count_jump <= 90 and self.is_jumping:
            self.rect.y -= 15
            self.count_jump += 15
            if self.game.detect_collision(self, self.game.all_blocks):
                self.rect.y += 15
                if self.is_life:
                    self.action = 3
                    self.frame = 0

        #gravity
        self.rect.y += 3
        
        if self.game.detect_collision(self, self.game.all_blocks):
            self.rect.y -= 3
            if self.is_jumping:
                self.is_jumping = False
                if self.is_life:
                    self.action = 3
                    self.frame = 0
        
        #vérifier collision avec traps
        if self.game.detect_collision(self, self.game.all_traps) and self.is_life:
            self.is_life = False
            self.action = 2
            self.frame = -1
                

    def animations(self):
        now = pygame.time.get_ticks()  # Obtenir le temps actuel
        if now - self.last_update > self.animation_time:  # Vérifier si le temps écoulé est supérieur au temps d'animation
            self.last_update = now  # Mettre à jour le dernier temps
            
            if self.action == 3: #immobile 
                self.frame += 1
                if self.frame >= len(self.images[self.action]):
                    self.frame = 0

            elif self.action == 0: #saut 
                self.frame += 1
                if self.frame >= len(self.images[self.action]):
                    self.frame = 0
                    self.action = 3 #immobile
            
            elif self.action == 5: #courrir 
                self.frame += 1
                if self.frame >= len(self.images[self.action]):
                    self.frame = 0
                    self.action = 3 #immobile

                    
            elif self.action ==2 : #dead 
                self.frame += 1
                if self.frame >= len(self.images[self.action]):
                    self.game.dead()
            
            self.image = self.images[self.action][self.frame]

            if self.direction == "LEFT":
                self.image = pygame.transform.flip(self.image, True, False)

    def detect_fruit(self):
        if self.game.detect_coll_fruit():
            self.fruit += 1
            if self.fruit == 3:
                self.game.next_level()
    
    def split_image(self, sprite_by_line, images):
        sprite_images = []
        for y, image_surface in enumerate(images):
            line_image = []
            for x in range(sprite_by_line[y]):
                image = image_surface.subsurface(pygame.Rect(x*self.data[0], 0, self.data[0], self.data[1]))
                image = pygame.transform.scale(image, (28,28))
                line_image.append(image)
            sprite_images.append(line_image)
        return sprite_images