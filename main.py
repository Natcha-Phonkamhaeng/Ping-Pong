# this game is the idea from tutorial, 16 May 2021 8:30 A.M. timestamp
# The code is my own code. (Modified)

import pygame
import sys
import random
pygame.init()

# general setup
pygame.display.set_caption("PingPong Game Version 1")
WIDTH = 600
HEIGHT = 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
LIGHT_GREY = (200,200,200) # use this color for Ball, Player, Opponent
BG_COLOR = pygame.Color('grey12')
game_font = pygame.font.Font('freesansbold.ttf', 20)

pause_event = pygame.USEREVENT + 1
pygame.mouse.set_visible(False)


class Ball():
    def __init__(self, x, y , width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_x = 5
        self.speed_y = 5

    def draw_ball(self):
        self.ball_move()
        self.collide()

        pygame.draw.ellipse(SCREEN, (LIGHT_GREY), (self.x,self.y,self.width,self.height))

    def ball_move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.y <= 0 or self.y + self.height >= HEIGHT:
            self.speed_y *= -1

        if self.x <= 0: # ball hitting left wall
            pygame.time.delay(1000)
            score.player_score += 1
            self.x = WIDTH/2
            self.speed_x *= random.choice((1,-1))
            self.speed_y *= random.choice((1,-1))


        if self.x + self.width >= WIDTH: # ball hitting right wall
            pygame.time.delay(1000)
            score.opp_score += 1
            self.x = WIDTH/2
            self.speed_x *= random.choice((1, -1))
            self.speed_y *= random.choice((1, -1))

    def collide(self):
        if pygame.Rect(ball.x, ball.y, ball.width, ball.height).colliderect(pygame.Rect(player.x, player.y, player.width, player.height))\
                or \
            pygame.Rect(ball.x, ball.y, ball.width,ball.height).colliderect(pygame.Rect(opp.x, opp.y, opp.width, opp.height)):
            ball.speed_x *= -1


class Player():
    def __init__(self, x, y , width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.player_speed = 3

    def draw_player(self):
        self.player_move()
        pygame.draw.rect(SCREEN, LIGHT_GREY, (self.x,self.y,self.width,self.height))

    def player_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.player_speed
        if keys[pygame.K_DOWN] and self.y + self.height < HEIGHT:
            self.y += self.player_speed


class Opp():
    def __init__(self, x, y , width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.opp_speed = 4

    def draw_opp(self):
        self.opp_move()
        pygame.draw.rect(SCREEN, LIGHT_GREY, (self.x,self.y,self.width,self.height))

    def opp_move(self):
        if self.y < ball.y:
            self.y += self.opp_speed
        if self.y > ball.y:
            self.y -= self.opp_speed

class Score():
    def __init__(self):
        self.player_score = 0
        self.opp_score = 0
        self.paused = True
        self.max_health = 5


    def draw_score(self):
        player_text = game_font.render(f"Player: {self.player_score}", True, (255,0,0))
        opp_text = game_font.render(f"Com: {self.opp_score}", True, (255,255,255))

        SCREEN.blit(opp_text, (100, 50 - opp_text.get_height()))
        SCREEN.blit(player_text, (WIDTH - player_text.get_width() - 100, 50 - player_text.get_height()))

        self.won_text()


    def won_text(self):
        won_font = pygame.font.SysFont('comicsans', 50)
        player_won = won_font.render("You Won!!!", True, (255,255,255))
        player_lost = won_font.render("You Lost!!", True, (255,0,0))

        if self.paused:
            if self.player_score >= self.max_health:
                SCREEN.fill((0,0,0))
                self.opp_score = 0

                SCREEN.blit(player_won, (WIDTH/2 - player_won.get_width()/2, HEIGHT/2 - player_won.get_height()/2))
                pygame.time.set_timer(pause_event, 6000)
            elif self.opp_score >= self.max_health:
                SCREEN.fill((0,0,0))
                self.player_score = 0

                SCREEN.blit(player_lost, (WIDTH/2 - player_won.get_width()/2, HEIGHT/2 - player_won.get_height()/2))
                pygame.time.set_timer(pause_event, 6000)


ball = Ball(WIDTH/2 - 10, HEIGHT/2 - 10, 20, 20)
player = Player(WIDTH - 20, HEIGHT/2 - 40, 10, 80)
opp = Opp(10, HEIGHT/2 - 40, 10, 80)
score = Score()


def main_menu():
    menu_text = pygame.font.SysFont("comicsans", 50)
    menu_text = menu_text.render("Press Space to continue", True, (255,255,255))
    # score.paused = False
    run = True
    while run :
        pygame.time.Clock().tick(FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                    main_game()

        SCREEN.fill((0,0,0))
        SCREEN.blit(menu_text, (WIDTH/2 - menu_text.get_width()/2, HEIGHT/2 - menu_text.get_height()/2))
        pygame.display.update()

# main game
def main_game():
    run_main_game = True
    while run_main_game:
        pygame.time.Clock().tick(FPS)

        def draw_window():
            SCREEN.fill(BG_COLOR) # screen color
            ball.draw_ball() # draw ball on screen
            player.draw_player() # draw player on right side
            opp.draw_opp() # draw opponent on left side

            pygame.draw.aaline(SCREEN, LIGHT_GREY, (WIDTH/2, 0), (WIDTH/2,HEIGHT)) # draw line between player and opponent
            score.draw_score()

            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pause_event:
                pygame.time.set_timer(pause_event, 0)
                score.paused = False
                if score.paused == False:
                    run_main_game = False
                    if score.player_score >= score.max_health: # if player win (score = 2), reset player score to 0
                        score.player_score = 0
                    if score.opp_score >= score.max_health : # if com win, reset com score to 0
                        score.opp_score = 0
                    # when score is reset to 0, turn score.pause = True then go to intro
                    score.paused = True
                    main_menu()

        draw_window()

main_menu()
