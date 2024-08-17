"""
Projet test des platformer (se familiariser avec)
Début : 12/08
Fin : ---
Durée : ---
"""
import pygame, sys
import os
from block import Block
from player import Player
from fruits import Fruit
from random import randint
from item import Item
from enemies import Enemie
from cloudSprite import Cloud
import map

pygame.init()

class Game():

    def __init__(self, map, fruits):
        self.list_fruits = fruits
        self.all_blocks = pygame.sprite.Group()
        self.all_fruits = pygame.sprite.Group()
        self.all_traps = pygame.sprite.Group()
        self.all_clouds = pygame.sprite.Group(Cloud(1100, randint(50,150), CLOUD, 1))
        self.map = map
        self.font = pygame.font.SysFont('COMIC SANS', 33)
        self.level = 1
        self.generation(self.map[self.level-1])

        self.player = Player(SIZE_BLOCK + 2,HEIGHT-2*SIZE_BLOCK - 2, PLAYER_IMAGE,SPRITE_BY_LINE , DATA, self)
        self.all_players = pygame.sprite.Group(self.player)
        
        self.text_start = self.font.render("Collect 3 fruits to advance to the next level! ", True, (255,255,255))
        self.text_start2 = self.font.render("Watch out for all the traps!", True, (255,255,255))
        self.text_end = self.font.render("Thank you for playing this game ", True, (255,255,255))
        self.text_end2 = self.font.render("MYCODE-DEVELOPPEMENT on Youtube", True, (255,255,255))
        
    def next_level(self):
        self.level += 1
        self.start()

    def dead(self):
        self.start()

    def start(self):
        self.all_blocks.empty()
        self.all_fruits.empty()
        self.all_traps.empty()
        self.generation(self.map[self.level - 1])
        self.player.start()

    def generation(self, map):
        for index1, line in enumerate(map):
            for index2, num in enumerate(line):
                if num == 1:
                    self.all_blocks.add(Block(index2*SIZE_BLOCK,index1*SIZE_BLOCK, TILE_1))
                elif num == 2:
                    self.all_fruits.add(Fruit(index2*SIZE_BLOCK,index1*SIZE_BLOCK, self.list_fruits[randint(0, len(self.list_fruits)-1)]))
                elif num == 3: #spike
                    self.all_traps.add(Item(index2*SIZE_BLOCK,index1*SIZE_BLOCK+10, TRAPS[0],1, (16,16), 32,22))
                
                elif num==4: #scie 
                    self.all_traps.add(Item(index2*SIZE_BLOCK,index1*SIZE_BLOCK, TRAPS[1],8, (38,38) ))
                
                elif num==5: #monster Blink 
                    self.all_traps.add(Enemie(index2*SIZE_BLOCK,index1*SIZE_BLOCK-22, BLINK,4, (54,52), 1, self, False ))
                
                elif num==6: #monster man 
                    self.all_traps.add(Enemie(index2*SIZE_BLOCK,index1*SIZE_BLOCK-2, ENEMIES[randint(0, len(ENEMIES)-1)],12, (32,32), 1, self))
                
                elif num == 7: #demi dalle
                    self.all_blocks.add(Block(index2*SIZE_BLOCK,index1*SIZE_BLOCK, TILE_1, True))
                

    def move(self):
        keys = pygame.key.get_pressed()

        self.player.move_player(keys)
        
        for fruit in self.all_fruits:
            fruit.animations()
        
        self.player.animations()
        for trap in self.all_traps:
            trap.animations()
        
        for cloud in self.all_clouds:
            cloud.move()
        
        #fénérération nuage
        if randint(0,100) == 3 and len(self.all_clouds) < 4:
            self.all_clouds.add(Cloud(1100, randint(50,150), CLOUD, 1))


        self.player.detect_fruit()

    def display_text(self):
        text_score = self.font.render(str(self.level), True, (255, 255, 255))
        screen.blit(text_score, (SIZE_BLOCK+4,SIZE_BLOCK+2))

        if self.level == 1:
            screen.blit(self.text_start, (WIDTH//2-self.text_start.get_width()//2,100))
            screen.blit(self.text_start2, (WIDTH//2-self.text_start2.get_width()//2,200))
        
        if self.level == len(self.map):
            screen.blit(self.text_end, (WIDTH//2-self.text_end.get_width()//2,100))
            screen.blit(self.text_end2, (WIDTH//2-self.text_end2.get_width()//2,200))
    

    def detect_coll_fruit(self):
        return pygame.sprite.spritecollide(self.player, self.all_fruits, True)

    def detect_collision(self, sprite, groups):
        return pygame.sprite.spritecollide(sprite, groups, False)

def return_list_img(dossier_images):
    # Liste pour stocker les surfaces d'images
    liste_images = []

    # Parcourir les fichiers du dossier
    for fichier in os.listdir(dossier_images):
        chemin_complet = os.path.join(dossier_images, fichier)
        
        # Vérifier si c'est un fichier image (vous pouvez ajouter d'autres extensions si nécessaire)
        if fichier.endswith('.png') or fichier.endswith('.jpg') or fichier.endswith('.jpeg'):
            # Charger l'image
            image = pygame.image.load(chemin_complet).convert_alpha()
            # Ajouter l'image à la liste
            liste_images.append(image)
    return liste_images

def create_list_fruits(list_, sprite_by_line, size):
    list_images_sprites = []
    for y, image in enumerate(list_) :
        list_line = []
        for x in range(sprite_by_line):
            sprite = image.subsurface(pygame.Rect(x*size, 0, size, size))
            list_line.append(sprite)
        list_images_sprites.append(list_line)
    return list_images_sprites


#CST
WIDTH, HEIGHT = 960,600
FPS = 60
SIZE_BLOCK = 30

#window
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PLATFORMER")


MAP = map.MAP

#time
timer = pygame.time.Clock()

#load images
current_dir = os.path.dirname(__file__)  # Répertoire du script 
#block : 
TILE_1 = pygame.image.load(os.path.join(current_dir, 'img', 'Blocks', 'tile_1.png')).convert_alpha()

# Définir le dossier contenant les images
dossier_images = os.path.join(current_dir, 'img', 'Ninja Frog')
PLAYER_IMAGE = return_list_img(dossier_images)
DATA =(32,32)
SPRITE_BY_LINE = [6,1,7,11, 1, 12, 5]

#FRUITS
APPLE_IMG = pygame.image.load(os.path.join(current_dir, 'img',"fruits", 'Apple.png')).convert_alpha() 
BANANAS_IMG = pygame.image.load(os.path.join(current_dir, 'img',"fruits", 'Bananas.png')).convert_alpha() 
CHERRIES_IMG = pygame.image.load(os.path.join(current_dir, 'img',"fruits", 'Cherries.png')).convert_alpha() 
STRAWBERRY_IMG = pygame.image.load(os.path.join(current_dir, 'img',"fruits", 'Strawberry.png')).convert_alpha() 
LIST_FRUITS = create_list_fruits([APPLE_IMG, BANANAS_IMG, CHERRIES_IMG, STRAWBERRY_IMG], 17,32 )

#ENEMIES
BLINK = pygame.image.load(os.path.join(current_dir, 'img','Enemies', 'Blink.png')).convert_alpha()
ENEMIES = [pygame.image.load(os.path.join(current_dir, 'img','Enemies', 'BlueMan.png')).convert_alpha(), pygame.image.load(os.path.join(current_dir, 'img','Enemies', 'mask.png')).convert_alpha(),pygame.image.load(os.path.join(current_dir, 'img','Enemies', 'pinkMan.png')).convert_alpha()]

#TRAPS
TRAPS = [pygame.image.load(os.path.join(current_dir, 'img','Traps', 'spike.png')).convert_alpha(),pygame.image.load(os.path.join(current_dir, 'img','Traps', 'scie.png')).convert_alpha(), ]

#DECOR
FLAG = pygame.image.load(os.path.join(current_dir, 'img', 'flag.png')).convert_alpha()
CLOUD = pygame.image.load(os.path.join(current_dir, 'img', 'cloud.png')).convert_alpha()

#game loop
running = True

game = Game(MAP, LIST_FRUITS)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    #move player
    game.move()

    screen.fill((93, 173, 226))
    game.all_clouds.draw(screen)
    game.all_blocks.draw(screen)
    game.all_fruits.draw(screen)
    game.all_traps.draw(screen)
    game.all_players.draw(screen)
    game.display_text()
    pygame.display.update()
    timer.tick(FPS)

