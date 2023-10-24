import pygame
from pygame import Vector2, Rect
from settings import *

class Player:

    state = 0
    ball_position = Vector2(0,0)

    def __init__(self, main_game, pos: Vector2):
        self.main_game = main_game
        self.pos = pos
        self.color = PLAYER_COLOR
        self.rect = Rect(pos[0], pos[1], PLAYER_WIDTH, PLAYER_HEIGHT)
        self.direction = Vector2(0,0)
        self.up_pressed = 0
        self.down_pressed = 0
        self.ai = 0

    def update(self):
        ball = self.main_game.ball

        if self.ai:
            self.ai_movement(ball.center.x, (ball.center.y - ball.radius))
        
        rect_y = self.rect.y

        if self.up_pressed:
            rect_y -= 1  * PLAYER_SPEED
            self.direction = Vector2(0,-1)
        
        if self.down_pressed:
            rect_y += 1  * PLAYER_SPEED
            self.direction = Vector2(0,1)

        if not self.down_pressed and not self.up_pressed:
            self.direction = Vector2(0,0) 

        self.check_limits(rect_y)
        self.draw()

    def check_limits(self, rect_y):        
        if 0 <= rect_y <= WINDOW_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = rect_y

    def compute_ball_position(self) -> Vector2:
        ball = self.main_game.ball
        actual_pos = Vector2(0,0)
        init_position = Vector2(ball.center.x - ball.radius, ball.center.y - ball.radius)
        dir_vector = ball.direction
        actual_pos = init_position
        while actual_pos.x <= self.pos[0]:
            actual_pos += dir_vector
            if actual_pos.y <= 0 or actual_pos.y >= WINDOW_HEIGHT: # Top wall hit
                dir_vector = Vector2(dir_vector.x, -dir_vector.y)
            
        return actual_pos 
    
    def move_to_position(self, position: Vector2) -> bool:
        res = False
        target_pos = 0
        #center_y = position.y + self.main_game.ball.radius
        if position.y >= (WINDOW_HEIGHT - PLAYER_HEIGHT/2):
            target_pos = WINDOW_HEIGHT - PLAYER_HEIGHT
        elif position.y <= PLAYER_HEIGHT/2:
            target_pos = 0
        else:
            target_pos = target_pos - PLAYER_HEIGHT/2

        diff = (self.rect.y + PLAYER_HEIGHT/2) - target_pos

        if abs(diff) > PLAYER_SPEED: # If away from the ball, move
            if diff > 0: # Needs to go up
                self.rect.y -= 1 * PLAYER_SPEED
            else: # Needs to go down    
                self.rect.y += 1 * PLAYER_SPEED
        else:
            res = True

        return res
    
    def ai_movement(self, pos_x, pos_y):
        """ if pos_x >= WINDOW_WIDTH/2:
            if Player.state == 0: # Ball has just crossed 
                # Compute the estimated position at player position
                Player.ball_position = self.compute_ball_position()
                Player.state = 1
            elif Player.state == 1:
                # Move to the estimated position
                if(self.move_to_position(Player.ball_position)):
                    Player.state = 2
        else:
            Player.state = 0 """

        if pos_x >= WINDOW_WIDTH/2:
           if pos_y >= (WINDOW_HEIGHT - PLAYER_HEIGHT/2):
               pos_y = WINDOW_HEIGHT - PLAYER_HEIGHT
           elif pos_y <= PLAYER_HEIGHT/2:
               pos_y = 0
           else:# PLAYER_HEIGHT < pos_y < (WINDOW_HEIGHT - PLAYER_HEIGHT):
               pos_y = pos_y - PLAYER_HEIGHT/2

           self.rect.y = pos_y


    def draw(self):
        pygame.draw.rect(self.main_game.screen, self.color, self.rect)
        