import pygame
import os
from settings import *
from player import *
from ball import Ball

class MainGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(GAME_NAME)
        self.score_font = pygame.font.SysFont("arial", 40, False)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.players = [Player(self, POS_PLAYER_LEFT), Player(self, POS_PLAYER_RIGHT)] 
        self.players[1].ai = 1
        self.ball = Ball(self, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.score = [0,0]
        self.sound_fx = [pygame.mixer.Sound("pong/sound_fx/pong_pong.mp3"),\
                            pygame.mixer.Sound("pong/sound_fx/pong_wall.mp3"), \
                            pygame.mixer.Sound("pong/sound_fx/pong_score.mp3")]

    def update(self):
        self.clock.tick(MAX_FPS)

    def draw_background(self):
        start = Vector2(WINDOW_WIDTH/2, 0) 
        end = Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT)
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.line(self.screen, MIDDLE_LINE_COLOR, start, end)

    def draw_score(self):
        if self.score[0] < 10:
            score_text = "0" + str(self.score[0]) + ":"
        else:
            score_text = str(self.score[0]) + ":"

        if self.score[1] < 10:
            score_text = score_text + "0" + str(self.score[1])
        else:
            score_text = score_text + str(self.score[1])

        text_surface = self.score_font.render(score_text, True, TEXT_COLOR, bgcolor=BACKGROUND_COLOR)
        text_center = (WINDOW_WIDTH/2, 20)
        text_rect = text_surface.get_rect(center=text_center)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.draw_background()
        self.draw_score()
        # Draw here the game things
        for player in self.players:
                player.update()

        self.ball.update()
        pygame.display.flip()

    def check_collisions(self):
        ball_center = (self.ball.center.x, self.ball.center.y)
        rect_pos_x = ball_center[0] - self.ball.radius
        rect_pos_y = ball_center[1] - self.ball.radius
        ball_rect = Rect(rect_pos_x, rect_pos_y, 2*self.ball.radius, 2*self.ball.radius)
        center_y = self.ball.center.y 

        # Collisions with borders
        if (rect_pos_y < 0) or (rect_pos_y + 2*self.ball.radius > WINDOW_HEIGHT):
            self.ball.direction = Vector2(self.ball.direction.x, -self.ball.direction.y) 
            self.sound_fx[1].play()

        # Check collision on left player
        if (rect_pos_x - (POS_PLAYER_LEFT[0] + PLAYER_WIDTH)) <= 0:
            # Check here if the player is in the ball boundariers
            if not self.ball.collide_left:
                if (self.players[0].rect.topright[1] - 2*self.ball.radius) <= rect_pos_y <= (self.players[0].rect.bottomright[1]):
                    self.ball.collide_left = 1
                    self.ball.direction = Vector2(-self.ball.direction.x, self.ball.direction.y) + self.players[0].direction
                    print("Collide left")
                    self.sound_fx[0].play()

        # Check collision on right player
        if (POS_PLAYER_RIGHT[0] - (rect_pos_x + 2*self.ball.radius)) <= 0:
            # Check here if the player is in the ball boundariers
            if not self.ball.collide_right:
                if (self.players[1].rect.topleft[1] - 2*self.ball.radius) <= rect_pos_y <= (self.players[1].rect.bottomleft[1]):
                    self.ball.collide_right = 1
                    self.ball.direction = Vector2(-self.ball.direction.x, self.ball.direction.y) + self.players[1].direction
                    print("Collide right")
                    self.sound_fx[0].play()
        
        #if self.players[0].rect.colliderect(ball_rect): # Check collision with the left player            
        #    self.ball.direction = Vector2(-self.ball.direction.x, self.ball.direction.y) + self.players[0].direction
        #    self.ball.collide_left = 1
        #    
            #move_to_position = self.players[1].compute_movement(self.ball)
            #self.players[1].rect.x = move_to_position.x
            #self.players[1].rect.y = move_to_position.y - PLAYER_HEIGHT/2
            
        
        #if self.players[1].rect.colliderect(ball_rect): # Check collision with the right player
        #    self.ball.direction = Vector2(-self.ball.direction.x, self.ball.direction.y) + self.players[1].direction
        #    self.sound_fx[0].play()

        if (rect_pos_x < (POS_PLAYER_LEFT[0])):
            self.score[1] += 1
            self.restore_ball()
            self.sound_fx[2].play()

        if (rect_pos_x + 2*self.ball.radius) > (POS_PLAYER_RIGHT[0] + PLAYER_WIDTH):
            self.score[0] += 1
            self.restore_ball()
            self.sound_fx[2].play()
        
    def restore_ball(self):
        self.ball = Ball(self, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.players[0].down_pressed = 1
                if event.key == pygame.K_UP:
                    self.players[0].up_pressed = 1
                if event.key == pygame.K_SPACE: # Start moving the ball
                    self.start_game = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.players[0].down_pressed = 0
                if event.key == pygame.K_UP:
                    self.players[0].up_pressed = 0
                if event.key == pygame.K_SPACE:
                    self.start_game = 0

    def run(self):
        while True:
            self.event_handler()
            self.check_collisions()
            self.draw()
            self.update()

# Main Game
if __name__ == '__main__':
    main_game = MainGame()
    main_game.run()
