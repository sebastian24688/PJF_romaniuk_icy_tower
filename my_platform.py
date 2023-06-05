import pygame
import random


class Platform(object):
    def __init__(self, game, x, y, platform_width, type_possibility):
        # inicjalizacja
        self.game = game

        # parametry
        self.x = x
        self.y = y
        self.platform_width = platform_width
        self.platform_height = 15
        self.color = (60, 60, 60)
        self.under_player = False
        self.type_list = [1, 2, 3]
        # 1 - zwykła, 2 - ruchoma, 3 - zapadnia
        self.type_possibility = type_possibility
        self.type = random.choices(self.type_list, type_possibility)[0]
        self.collision_count = 5

        if self.type == 2:
            self.color = (0, 51, 102)
            self.direction = random.choice([1, -1])
        elif self.type == 3:
            self.collision_count = 1

        # obrazy
        self.platform = pygame.Rect(self.x, self.y, self.platform_width, self.platform_height)

    def collision(self):
        self.collision_count -= 1

    def tick(self):
        # kolor platformy
        if self.collision_count == 3:
            self.color = (80, 60, 60)
        if self.collision_count == 2:
            self.color = (150, 30, 30)
        if self.collision_count == 1:
            self.color = (255, 0, 0)

        # platforma ruchoma
        if self.type == 2:
            self.x += self.direction
            if self.x < 100 or self.x > 700 - self.platform_width:
                self.direction = -self.direction

    def draw(self):
        self.platform = pygame.Rect(self.x, self.y, self.platform_width, self.platform_height)
        pygame.draw.rect(self.game.screen, self.color, self.platform)
