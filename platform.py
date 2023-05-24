import pygame
import random

class Platform(object):
    def __init__(self, game):
        # inicjalizacja
        self.game = game

        # parametry
        self.x = 100
        self.y = self.game.screen_y - 100
        self.platform_width = 600
        self.platform_height = 15
        self.color = (60, 60, 60)

        # obrazy
        self.platform = pygame.Rect(self.x, self.y, self.platform_width, self.platform_height)

        # x = random.randint(0, self.screen_x - platform_width)  # Losowa pozycja X
        # y = random.randint(0, self.game.screen_y - platform_height)  # Losowa pozycja Y

    def tick(self):
        pass

    def draw(self, ):
        pygame.draw.rect(self.game.screen, self.color, self.platform)
