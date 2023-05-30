import pygame

class Platform(object):
    def __init__(self, game, x, y, platform_width):
        # inicjalizacja
        self.game = game

        # parametry
        self.x = x
        self.y = y
        self.platform_width = platform_width
        self.platform_height = 15
        self.color = (60, 60, 60)
        self.under_player = False

        # obrazy
        self.platform = pygame.Rect(self.x, self.y, self.platform_width, self.platform_height)

    def tick(self):
        pass

    def draw(self, ):
        self.platform = pygame.Rect(self.x, self.y, self.platform_width, self.platform_height)
        pygame.draw.rect(self.game.screen, self.color, self.platform)
