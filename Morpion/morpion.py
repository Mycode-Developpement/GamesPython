"""
Création du jeu tic tac toe (sans vidéo)
Début : 21/07
Fin : 21/07
Durée : 2H
"""

import pygame
pygame.init()

HEIGHT, WIDTH = 450,450
SIZE_CASE = 150
FPS = 30

screen = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("TIC TAC TOE")

timer = pygame.time.Clock()
running = True 


class Game():
    def __init__(self):
        self.position = [0]*9
        self.tour = 1 #Joueur au tour de jouer
        self.list_grille = self.grille() 
        self.placement = []
        self.win = False
        self.font = pygame.font.SysFont(None, 55)
        self.button_restart = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100)
        for j in range(3):
            for i in range(3):
                self.placement.append((i*SIZE_CASE, j*SIZE_CASE))
    
    def grille(self):
        """Création de la liste de la grille"""
        list = []
        for j in range(3):
            for i in range(3):
                case = pygame.Rect(i*SIZE_CASE, j*SIZE_CASE, SIZE_CASE, SIZE_CASE)
                list.append(case)
        return list
    
    
    def affichage(self):
        for case in self.list_grille:
            pygame.draw.rect(screen,pygame.Color("black"), case, width=1)
        
        for index, nb in enumerate(self.position):
            if nb == 1:
                case = pygame.Rect(self.placement[index][0]+5,self.placement[index][1]+5, SIZE_CASE-10,SIZE_CASE-10)
                pygame.draw.rect(screen, pygame.Color("red"), case, border_radius=100)
            
            if nb == 2:
                case = pygame.Rect(self.placement[index][0]+5,self.placement[index][1]+5, SIZE_CASE-10,SIZE_CASE-10)
                pygame.draw.rect(screen, pygame.Color("green"), case, border_radius=100)
        
        if self.win: 
            pygame.draw.rect(screen, pygame.Color("gray"), self.button_restart)
            text = self.font.render('Player {} wins!'.format(1 if self.tour == 2 else 2), True, pygame.Color('blue'))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            
    
    def click(self, pos):
        for i in self.list_grille:
            if i.collidepoint(pos):
                self.action_jeu(self.list_grille.index(i))
        if self.win:
            if self.button_restart.collidepoint(pos):
                self.restart()
        
    def action_jeu(self, index):
        if not self.win:
            if self.position[index] == 0:
                self.position[index] = self.tour 
                if self.tour == 1:
                    self.tour = 2
                else:
                    self.tour = 1

        if self.position[0] == self.position[1] == self.position[2] != 0:
            self.win = True
        elif self.position[3] == self.position[4] == self.position[5] != 0:
            self.win = True
        elif self.position[6] == self.position[7] == self.position[8] != 0:
            self.win = True
        elif self.position[0] == self.position[4] == self.position[8] != 0:
            self.win = True
        elif self.position[2] == self.position[4] == self.position[6] != 0:
            self.win = True
        elif self.position[1] == self.position[4] == self.position[7] != 0:
            self.win = True
        elif self.position[0] == self.position[3] == self.position[6] != 0:
            self.win = True
        elif self.position[1] == self.position[4] == self.position[7] != 0:
            self.win = True
        elif self.position[2] == self.position[5] == self.position[8] != 0:
            self.win = True
        elif not 0 in self.position:
            self.restart() 
        
    def restart(self):
        self.position = [0]*9
        self.tour = 1 #Joueur au tour de jouer
        self.win = False


game = Game()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Récupérer la position du clic de souris
            pos = pygame.mouse.get_pos()
            # Vérifier si le clic est dans le rectangle
            game.click(pos)
            
    
    screen.fill(pygame.Color('white'))
    game.affichage()

    pygame.display.update()
    timer.tick(FPS)