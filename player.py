import pygame
from pygame.math import Vector2


class Player(object):
    def __init__(self, game):
        self.game = game
        self.speed = 1.3
        self.gravity = 0.5
        self.mario = pygame.image.load("obrazki/mario2.png").convert_alpha()
        self.image = pygame.transform.scale(self.mario, (51, 67))
        self.inverted = False

        self.pos = Vector2(self.game.screen_x/4, 0)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def add_force(self, force):
        self.acc += force

    def tick(self):
        # input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.add_force(Vector2(-self.speed, 0))
        if pressed[pygame.K_RIGHT]:
            self.add_force(Vector2(self.speed, 0))

        # opor
        self.vel *= 0.8
        #self.vel -= Vector2(0, -self.gravity)

        # fizyka
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0  # zeruje wektor



    def draw(self, ):
        self.game.screen.blit( pygame.transform.flip(self.image,self.inverted,False), (self.pos[0], self.pos[1]))
