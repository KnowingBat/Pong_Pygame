import pygame
from pygame import Rect, Vector2
from settings import *
from random import randint

class Ball:
    def __init__(self, main_game, pos: Vector2):
        self.radius = BALL_RADIUS
        self.direction = Vector2(0, 0)
        self.randomize_direction()
        self.center = pos
        self.main_game = main_game
        self.collide_left = 0
        self.collide_right = 0

    def update(self):
        self.center += self.direction * BALL_SPEED

        if self.collide_left:
            if (self.center.x - self.radius) >= POS_PLAYER_LEFT[0] + PLAYER_WIDTH:
                self.collide_left = 0

        if self.collide_right:
            if (self.center.x + self.radius) <= POS_PLAYER_RIGHT[0]:
                self.collide_right = 0

        self.draw()

    def randomize_direction(self):
        self.direction = VELOCITY_LIST[randint(0,5)]


    def draw(self):
        pygame.draw.circle(self.main_game.screen, BALL_COLOR, self.center, self.radius)
