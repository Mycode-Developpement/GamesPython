"""
Création jeu Pong 
Début : 21/07
Fin : 22/07
Durée : 3H
"""

import pygame, sys, button
pygame.init()

class Game():
    def __init__(self):
        self.player2 = pygame.Rect(50, HEIGHT//2-30, 15,60)
        self.player1 = pygame.Rect(WIDTH-50, HEIGHT//2-30, 15,60)
        self.ball = pygame.Rect(WIDTH//2-10, HEIGHT//2-10, 20,20)
        #texte
        self.font = pygame.font.SysFont(None,70)
        self.score1 = 0 
        self.score2 = 0

        self.text1 = self.font.render(str(self.score1), True, COLOR2)
        self.text2 = self.font.render(str(self.score2), True, COLOR2)

        #variable jeu
        self.x_speed = 2
        self.y_speed = 2
        self.player_speed = 6
    
    def draw(self):
        pygame.draw.aaline(screen,COLOR2,(WIDTH//2, 0),(WIDTH//2, HEIGHT))
        pygame.draw.circle(screen, COLOR2, (WIDTH//2, HEIGHT//2), 45, width=1)

        pygame.draw.rect(screen, COLOR2, self.player1)
        pygame.draw.rect(screen, COLOR2, self.player2)
        pygame.draw.ellipse(screen, COLOR2, self.ball)

        screen.blit(self.text1, (WIDTH//4,50))
        screen.blit(self.text2, (WIDTH-WIDTH//4,50))
    
    
    def move_player(self,keys):
        if keys[pygame.K_UP]:
            if self.player1.y >= 0:
                self.player1.y -= self.player_speed
        if keys[pygame.K_DOWN]:
            if self.player1.y <= HEIGHT-50:
                self.player1.y += self.player_speed
        if keys[pygame.K_a]:
            if self.player2.y >= 0:
                self.player2.y -= self.player_speed
        if keys[pygame.K_q]:
            if self.player2.y <= HEIGHT-50:
                self.player2.y += self.player_speed

    
    def detect_col(self):
        #vérif collision 
        if self.ball.x <= 0:
            self.score2+=1
            self.text2 = self.font.render(str(self.score2), True, COLOR2)
            self.point_marque()

        elif self.ball.x >= WIDTH:
            self.score1+= 1
            self.text1 = self.font.render(str(self.score1), True, COLOR2)
            self.point_marque()

        if self.ball.y <= 0 or self.ball.y >= HEIGHT:
            self.y_speed *= -1
        
        if self.player1.colliderect(self.ball):
            self.x_speed *= -1
            self.speed_up()
            


        if self.player2.colliderect(self.ball):
            self.x_speed *= -1
            self.speed_up()

        #déplacement 
        self.ball.x += self.x_speed
        self.ball.y += self.y_speed
    
    def speed_up(self):
        if self.x_speed < 0:
            self.x_speed -= 0.7
        else:
            self.x_speed += 0.7
        
        if self.y_speed < 0:
            self.y_speed -= 0.3
        else:
            self.y_speed += 0.3


    def point_marque(self):
        global text_win
        if self.score1 == 3:
            text_win = "Player 1 win ! "
            self.restart()
        elif self.score2 == 3:
            text_win = "Player 2 win ! "
            self.restart()

        self.ball.x = WIDTH//2-15
        self.ball.y = HEIGHT//2-15
        self.player1.y = HEIGHT//2-30
        self.player2.y = HEIGHT//2-30
        
        if self.x_speed < 0:
            self.x_speed = 2
        else:
            self.x_speed = -2
        
        self.y_speed = 2

    def restart(self):
        global state_menu
        self.ball.x = WIDTH//2-15
        self.ball.y = HEIGHT//2-15
        self.player1.y = HEIGHT//2-30
        self.player2.y = HEIGHT//2-30
        self.score1, self.score2 = 0,0
        self.x_speed = 2
        self.y_speed = 2
        self.text1 = self.font.render(str(self.score1), True, COLOR2)
        self.text2 = self.font.render(str(self.score2), True, COLOR2)
        state_menu = True


#Variable constante
HEIGHT, WIDTH = 550,920
FPS = 60
COLOR1 =  (33, 47, 60)
COLOR2 = (255,255,255)

#Page custom 
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PONG")

#police d'écriture
font = pygame.font.SysFont("Comic Sans", 55)
font2 = pygame.font.SysFont("Futura", 20)

#image bouton 
resume_img = pygame.image.load("img/button_resume.png").convert_alpha()
quit_img = pygame.image.load("img/button_quit.png").convert_alpha()
resume_button = button.Button(WIDTH//2-100, HEIGHT//2-100., resume_img, 1)
quit_button = button.Button(WIDTH//2-75, HEIGHT//2+50, quit_img, 1)

#variable du jeu :
text_win = "Game Pong"
state_menu = True
running = True
timer = pygame.time.Clock()

game = Game()

#boucle du jeu 
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state_menu = True #revenir au menu 

    if state_menu: #si dans les menus 
        screen.fill(COLOR1)
        #texte
        text_render = font.render(text_win, True, COLOR2)
        screen.blit(text_render, (WIDTH//2-text_render.get_width()//2, 50))
        text_info = font2.render("Appuie sur espace pour faire pause à tout moment !", True, COLOR2)
        screen.blit(text_info, (WIDTH//2-text_render.get_width()//2, HEIGHT-76))
        
        if resume_button.draw(screen):
            state_menu = False
        if quit_button.draw(screen):
            running = False
            pygame.quit()
            sys.exit()
    else:
        screen.fill(COLOR1)
        game.move_player( pygame.key.get_pressed())
        game.detect_col()
    
        #affichage page  
        game.draw()     
    
    pygame.display.update()
    timer.tick(FPS)

    
