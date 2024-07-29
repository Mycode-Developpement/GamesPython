import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.direction = ""
        self.direction2 = ''
        self.speed = 1
        self.score = 0
        self.images = [(0,0),(16,0), (32,0), (48,0), (64,0), (80, 0), (96, 0), (112, 0)]
        self.pos = 0
        self.animation_time = 100  # Temps en millisecondes pour changer de frame
        self.last_update = pygame.time.get_ticks()

        # Charge la feuille de sprites
        self.tileset = pygame.image.load(self.get_image_path("assets/PacMan.png")).convert_alpha()
        # Définir la taille du sprite à extraire
        sprite_width = 16
        sprite_height = 16
        
        # Définir la position du sprite sur la feuille
        sprite_x = 0  # Par exemple, le premier sprite sur la feuille
        sprite_y = 0 # Par exemple, le premier sprite sur la feuille
        
        # Extraire le sprite souhaité
        self.image = self.tileset.subsurface(pygame.Rect(sprite_x, sprite_y, sprite_width, sprite_height))
        
        # Redimensionner le sprite à la taille de la cellule
        self.image = pygame.transform.scale(self.image, (20,20))
        
        # Définir le rectangle de la sprite
        self.rect = self.image.get_rect()
        self.rect.x = 10 * SIZE_CELL + 5
        self.rect.y =10 * SIZE_CELL + 5
    
    def change_direction(self, new):
        if new != self.direction:
            self.direction2 = self.direction
            self.direction = new
    
    def move(self):  
        if self.direction == "UP":
            self.move_up()      
        elif self.direction == "DOWN":
            self.move_down()
        elif self.direction == "LEFT":
            self.move_left()  
        elif self.direction == "RIGHT":
            self.move_right()
        if self.game.check_collision_ghost():
            self.game.restart()
            self.kill()

            #verifier s'il la pièce a été touché
        elif self.game.check_collision_coin():
            self.score += 1    
              

    def move_right(self):
        self.rect.x += self.speed
        if self.game.check_collision_block():
            self.rect.x -= self.speed
            #si le mouvement n'est pas possible faire l'autre 
            self.move_second()
        
    def move_left(self):
        self.rect.x -= self.speed
        if self.game.check_collision_block():
            self.rect.x += self.speed
            #si le mouvement n'est pas possible faire l'autre 
            self.move_second()
        
    
    def move_up(self):
        self.rect.y -= self.speed
        if self.game.check_collision_block():
            self.rect.y += self.speed
            #si le mouvement n'est pas possible faire l'autre 
            self.move_second()
        

    def move_down(self):
        self.rect.y += self.speed
        if self.game.check_collision_block():
            self.rect.y -= self.speed
            #si le mouvement n'est pas possible faire l'autre
            self.move_second()
            

    def move_second(self):
        if self.direction2 == "UP":
            self.rect.y -= self.speed
            if self.game.check_collision_block():
                self.rect.y += self.speed     
        
        elif self.direction2 == "DOWN":
            self.rect.y += self.speed
            if self.game.check_collision_block():
                self.rect.y -= self.speed

        elif self.direction2 == "LEFT":
            self.rect.x -= self.speed
            if self.game.check_collision_block():
                self.rect.x += self.speed

        elif self.direction2 == "RIGHT":
            self.rect.x += self.speed
            if self.game.check_collision_block():
                self.rect.x -= self.speed
        

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
            self.image = pygame.transform.scale(self.image, (25, 25))


            if self.direction == "UP":
                self.image = pygame.transform.rotate(self.image, 90)    
            elif self.direction == "DOWN":
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.direction == "LEFT":
                self.image = pygame.transform.rotate(self.image, 180)
                self.image = pygame.transform.flip(self.image, False, True)
            elif self.direction == "RIGHT":
                self.image = pygame.transform.rotate(self.image, 0)

            

    
    def get_image_path(self, relative_path):
        """Retourne le chemin absolu de l'image en fonction du chemin relatif."""
        base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)
    
SIZE_CELL = 30