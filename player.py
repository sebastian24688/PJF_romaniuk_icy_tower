import pygame
from pygame.math import Vector2


class Player(object):
    def __init__(self, game):
        # inicjalizacja
        self.game = game
        self.position = Vector2(self.game.screen_x/4, 100)
        self.velocity = 0
        self.mario_width = 51
        self.mario_hight = 67

        # parametry
        self.speed_x = 3
        self.gravity = 0.03

        # obrazy
        self.mario = pygame.image.load("obrazki/mario2.png").convert_alpha()
        self.image = pygame.transform.scale(self.mario, (self.mario_width, self.mario_hight))
        self.inverted = False


    def tick(self):
        # ruch prawo/lewo
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            # ściana lewa
            if self.position[0] > 100:
                self.position[0] -= self.speed_x
            self.inverted = True
        if pressed[pygame.K_RIGHT]:
            # ściana prawa
            if self.position[0] < 700-self.mario_width:
                self.position[0] += self.speed_x
            self.inverted = False

        # skakanie

        # grawitacja
        self.velocity -= -self.gravity

        # odbicie od podłogi
        if self.position[1] > self.game.screen_x - 100 - 67:
            self.velocity = -3.2

        # odbicie od podłogi
        self.position[1] += self.velocity



    def draw(self, ):
        image = pygame.transform.flip(self.image, self.inverted, False) # odbicie lustrzane
        position = (self.position[0], self.position[1])
        self.game.screen.blit(image, position) # wyświetlenie mario
