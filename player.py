import pygame
from pygame.math import Vector2


class Player(object):
    def __init__(self, game):
        # inicjalizacja
        self.game = game
        self.position = Vector2(self.game.screen_x / 2, self.game.screen_y - 150)
        self.mario_width = 51
        self.mario_hight = 67

        # parametry
        self.speed_x = 3
        self.gravity = 0.03
        self.velocity = 0
        self.drag = 0.5
        self.temp = 0
        self.slide = 0

        # obrazy
        mario = pygame.image.load("obrazki/mario2.png").convert_alpha()
        self.image = pygame.transform.scale(mario, (self.mario_width, self.mario_hight))
        self.inverted = False
        self.contour = pygame.Rect(self.position[0], self.position[1], self.mario_width, self.mario_hight)

    def tick(self):
        # ruch prawo/lewo
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            # ściana lewa
            if self.position[0] > 100:
                self.temp = -self.speed_x
            self.inverted = True
            # self.speed_y = -1
        if pressed[pygame.K_RIGHT]:
            # ściana prawa
            if self.position[0] < 700 - self.mario_width:
                self.temp = self.speed_x
            self.inverted = False
            # self.speed_y = 1

        if self.temp > 0:
            self.temp -= self.drag
        elif self.temp < 0:
            self.temp += self.drag

        self.position[0] += self.temp

        # grawitacja
        self.velocity -= -self.gravity

        # kolizja z platformą
        for platform in self.game.platforms:
            if self.position[1] + self.mario_hight < platform.y:
                platform.under_player = True
            if self.position[1] + self.mario_hight - 10 > platform.y:
                platform.under_player = False

            if pygame.Rect.colliderect(platform.platform, self.contour):
                if self.velocity > 0 and platform.under_player is True:
                    self.velocity = -3.2
                    # print("{} + {} > {}".format(self.position[1], self.mario_hight, platform.y))

        # odbicie od podłogi
        if self.position[1] > self.game.screen_x - 100 - 67:
            self.velocity = -3.2

        # ruch oraz wartość przesunięcia platform
        if self.position[1] <= 300 and self.velocity < 0:
            self.slide = self.velocity
        else:
            self.slide = 0
            self.position[1] += self.velocity


    def draw(self):
        image = pygame.transform.flip(self.image, self.inverted, False)  # odbicie lustrzane
        position = (self.position[0], self.position[1])
        self.game.screen.blit(image, position)  # wyświetlenie mario

        self.contour = pygame.Rect(self.position[0], self.position[1], self.mario_width, self.mario_hight)
        pygame.draw.rect(self.game.screen, (200, 200, 200), self.contour, 2)
