import pygame
from shurigen import Shurigen
from random import randint

class Fighter(pygame.sprite.Sprite):

    def __init__(self,x,y,image, sprite_by_lines, data, flip, game, image_shuri, keyPlayer, num_player):
        super().__init__()
        #variable 
        self.game = game
        self.num_player = num_player
        self.health_max = 100
        self.position_initial = (x,y)
        self.speed = 5
        self.gravity = 4
        self.flip_ = flip
        self.image_shuri = image_shuri

        self.data = data
        self.all_images = self.split_image(image, sprite_by_lines)
        self.animation_time = 125  # Temps en millisecondes pour changer de frame

        self.keyPlayer = keyPlayer
        self.start()
        
    
    def start(self):
        self.health = 100
        self.is_jumping = False
        self.is_attaking = False
        self.is_protect = False
        self.is_hyper = False
        self.frame = 0
        self.action = 1
        self.all_shurigens = pygame.sprite.Group()
        self.image = self.all_images[0][0]
        self.energy = 100 #si plus d'energie, il est impossible de faire des action
        self.flip()

        self.nb_ulti = 2 #nombre d'utilisation de l'onde de choc
        
        self.attack_nb = 7

        self.hyper = False

        self.rect = self.image.get_rect()

        self.rect.x = self.position_initial[0]
        self.rect.y = self.position_initial[1]

        self.current_sequence = []

        self.last_update = pygame.time.get_ticks()

        self.last_attack= pygame.time.get_ticks()  # Obtenir le temps actuel

    
    def move(self, opponent, screen, keys, joystick=None):
        dx = 0
        dy = 0

        # Gestion des contrôles par clavier
        if joystick is None:  # Si aucune manette n'est utilisée
            if keys[self.keyPlayer["right"]] and not self.is_protect:
                dx = self.speed
                if not self.is_jumping and not self.is_attaking:
                    self.action = 3

            if keys[self.keyPlayer["left"]] and not self.is_protect:
                dx = -self.speed
                if not self.is_jumping and not self.is_attaking:
                    self.action = 3

            if keys[self.keyPlayer["up"]] and (self.action == 1 or self.action == 3) and not keys[self.keyPlayer["combo"]]:
                self.is_jumping = True
                self.action = 5 
                dy = -150

            if keys[self.keyPlayer["attack2"]] and keys[self.keyPlayer["combo"]] and keys[self.keyPlayer["attack"]] and (self.action == 1 or self.action == 3):
                if self.hyper:
                    self.hyper = False
                    self.is_hyper = True
                    self.frame = 0
                    self.action = 6
                    self.attack_nb = 17
                    self.last_attack= pygame.time.get_ticks()
                    self.game.activ_super()
            if keys[self.keyPlayer["attack"]] and keys[self.keyPlayer["combo"]] and keys[self.keyPlayer["attack"]] and (self.action == 1 or self.action == 3) and self.energy >= 60:
                if self.nb_ulti > 0:
                    self.nb_ulti -= 1
                    self.frame = 0
                    self.action = 6
                    self.energy -= 60
                    self.last_attack= pygame.time.get_ticks()
                    self.activ_ulti(opponent)

            if keys[self.keyPlayer["attack"]] and (self.action == 1 or self.action == 3) and self.energy >= 25:
                self.frame = 0
                self.is_attaking = True
                self.action = 8
                self.energy -= 25
                self.last_attack= pygame.time.get_ticks()

            if keys[self.keyPlayer["combo"]] and keys[self.keyPlayer["up"]] and (self.action == 1 or self.action == 3)and self.energy >= 9:
                self.frame = 0
                self.is_protect = True
                self.action = 6
                self.energy -= 9
                self.last_attack= pygame.time.get_ticks()

            if keys[self.keyPlayer["attack2"]] and (self.action == 1 or self.action == 3) and not keys[self.keyPlayer["combo"]]and self.energy >= 10:
                self.frame = 0
                self.is_attaking = True
                self.action = 2
                self.energy -= 10
                self.attack_shurigen(opponent)
                self.last_attack= pygame.time.get_ticks()

        else:  # Utilisation de la manette
            # Axes
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)

            # Boutons
            button_attack = joystick.get_button(2) #ps4 : carré
            button_attack2 = joystick.get_button(1) #rond
            button_protect = joystick.get_button(3)
            button_combo = joystick.get_button(0)

            # Déplacement avec la manette
            if axis_x > 0.2 and not self.is_protect:  # Déplacement vers la droite
                dx = self.speed
                if not self.is_jumping and not self.is_attaking:
                    self.action = 3
            elif axis_x < -0.2  and not self.is_protect:  # Déplacement vers la gauche
                dx = -self.speed
                if not self.is_jumping and not self.is_attaking:
                    self.action = 3

            if axis_y < -0.7 and (self.action == 1 or self.action == 3) and not button_combo:
                self.is_jumping = True
                self.action = 5 
                dy = -150

            if button_attack and button_combo and (self.action == 1 or self.action == 3): #X + carré
                if self.hyper:
                    self.hyper = False
                    self.is_hyper = True
                    self.frame = 0
                    self.action = 6
                    self.attack_nb = 17
                    self.last_attack= pygame.time.get_ticks()
                    self.game.activ_super()

            if button_attack2 and button_combo and (self.action == 1 or self.action == 3)and self.energy >= 60: #croix + rond
                if self.nb_ulti > 0:
                    self.nb_ulti -= 1
                    self.frame = 0
                    self.action = 6
                    self.energy -= 60
                    self.last_attack= pygame.time.get_ticks()
                    self.activ_ulti(opponent)

            if button_attack and (self.action == 1 or self.action == 3)and self.energy >= 25:
                self.frame = 0
                self.is_attaking = True
                self.action = 8
                self.energy -= 25
                self.last_attack= pygame.time.get_ticks()

            if button_protect and (self.action == 1 or self.action == 3) and self.energy >= 9:
                self.frame = 0
                self.is_protect = True
                self.action = 6
                self.energy -= 9
                self.last_attack= pygame.time.get_ticks()

            if button_attack2 and (self.action == 1 or self.action == 3) and not button_combo and self.energy >= 10:
                self.frame = 0
                self.is_attaking = True
                self.action = 2
                self.energy -= 10
                self.last_attack= pygame.time.get_ticks()
                self.attack_shurigen(opponent)

        # Gravitation
        if self.rect.y < 300:
            self.rect.y += self.gravity
        elif self.rect.y > 300:
            self.rect.y = 300

        self.animations(opponent, screen)

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.x > 1000:
            self.rect.x = 1000
        elif self.rect.x < 0:
            self.rect.x = 0


    def animations(self, opponent, screen):
        now = pygame.time.get_ticks()  # Obtenir le temps actuel

        if now - self.last_update > self.animation_time:  # Vérifier si le temps écoulé est supérieur au temps d'animation
            self.frame += 1
            self.last_update = now  # Mettre à jour le dernier temps
            if self.energy < 100:       
                if now - self.last_attack > 3500:
                    if self.energy + 4 > 100:
                        self.energy = 100
                    else:
                        self.energy += 4
                else:
                    self.energy += 1
            
            if self.action == 1: #ne fait rien 
                if self.frame > len(self.all_images[self.action])-1:
                    self.frame = 0
            
            elif self.action == 2: #attaque shurigen 
                if self.frame > len(self.all_images[self.action])-1:
                    self.frame = 0
                    self.action = 1
                    self.is_attaking = False
            
            elif self.action == 3: #marche 
                if self.frame > len(self.all_images[self.action])-1:
                    self.frame = 0
                    self.action = 1
        
            elif self.action == 5: #is jumping 
                if self.frame > len(self.all_images[self.action])-1:
                    self.frame = 0
                    self.action = 1
                    self.is_jumping = False
            
            elif self.action == 6: #is protext 
                if self.frame > len(self.all_images[self.action])-1:
                    self.frame = 0
                    self.action = 1
                    self.is_protect = False

            elif self.action == 7: #dead 
                if self.frame > len(self.all_images[self.action])-1:
                    self.frame = 7
            
            elif self.action == 8: #is attaking 
                if self.frame == 5:
                    self.attack(screen, opponent)
                if self.frame > len(self.all_images[self.action])-1:
                    self.frame = 0
                    self.action = 1
                    self.is_attaking = False

            if self.is_hyper and randint(0,50) == 0:
                self.is_hyper = False 
                self.attack_nb = 7
                self.game.fin_super()

            
            self.image = self.all_images[self.action][self.frame]
            self.detect_flip(opponent)

            

    def attack(self, screen, opponent):
        if pygame.sprite.collide_rect(self, opponent):
            self.game.sword_son()
            opponent.subir_attaque(self.attack_nb, self, 3)
            if randint(0,20) == 1 and not self.is_hyper:
                self.hyper = True
                self.game.super_son()
        
    def attack_shurigen(self, opponent):
        self.all_shurigens.add(Shurigen(self.rect.centerx, self.rect.centery, self.image_shuri, 4 if self.rect.x < opponent.rect.x else -4, opponent, self))
        self.game.son_shurigen()
        
    def activ_ulti(self, opponent):
        #onde de choc
        if self.rect.x > opponent.rect.x:
            opponent.rect.x = 0

        else : opponent.rect.x = 1000
    
    def subir_attaque(self, degat, opponent, contre_degat):
        if not self.is_protect:
            self.health -= degat
        else: #le joueur en se protégent inflige des dégats à son adversaire 
            if contre_degat != 0:
                opponent.subir_attaque(contre_degat, self, 0)
        if self.health <= 0:
                self.action = 7
                self.frame = 0
                self.health = 0
                self.game.dead(opponent.num_player)
    

    
    def split_image(self,images, sprite_by_lines):
        all_images = []
        for y in range(len(sprite_by_lines)):
            images_lines = []
            for x in range(sprite_by_lines[y]):
                image = images.subsurface(pygame.Rect(x*self.data[0], y*self.data[1], self.data[0], self.data[1]))
                images_lines.append(image.subsurface(pygame.Rect(25,15, 132,172)))
            all_images.append(images_lines)
        return all_images
    
    
    def flip(self):
        self.image = pygame.transform.flip(self.image, self.flip_, False)
    
    def detect_flip(self, opponent):
        #direction regardé par le joueurs
        if self.rect.x > opponent.rect.x:
            self.flip_ = True
            self.flip()
        else:
            self.flip_ = False
            self.flip()
       