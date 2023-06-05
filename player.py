import pygame
from pygame.math import Vector2
from my_control import Control


class Player(object):
    def __init__(self, game, control_option):
        # inicjalizacja
        self.game = game
        self.control = Control()
        self.position = Vector2(self.game.screen_x / 2, self.game.screen_y - 150)
        self.mario_width = 51
        self.mario_hight = 67
        self.skip = 0
        self.pressed = 'S'
        self.control_option = control_option

        # parametry
        self.speed_x = 3
        self.gravity = 0.03
        self.velocity = 0
        self.drag = 0.5
        self.temp = 0
        self.slide = 0
        self.boost = False
        self.rotate = False
        self.angle = 0

        # obrazy
        mario = pygame.image.load("obrazki/mario2.png").convert_alpha()
        self.image = pygame.transform.scale(mario, (self.mario_width, self.mario_hight))
        self.inverted = self.rotate_direction = False
        self.contour = pygame.Rect(self.position[0], self.position[1], self.mario_width, self.mario_hight)

    def tick(self):
        # sterowanie klawiszami
        if self.control_option == 1:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                # ściana lewa
                if self.position[0] <= 103:
                    self.boost = True
                if self.position[0] > 103:
                    self.temp = -self.speed_x
                self.inverted = True
            if pressed[pygame.K_RIGHT]:
                # ściana prawa
                if self.position[0] >= 700 - self.mario_width - 3:
                    self.boost = True
                if self.position[0] < 700 - self.mario_width - 3:
                    self.temp = self.speed_x
                self.inverted = False

        # sterowanie gestami - przedziały
        if self.control_option == 2:
            self.skip = (self.skip + 1) % 7
            if self.skip == 0:
                self.control.tick()
                self.pressed = self.control.position()

            if self.pressed == 'L':
                # ściana lewa
                if self.position[0] <= 103:
                    self.boost = True
                if self.position[0] > 103:
                    self.temp = -self.speed_x
                self.inverted = True
            if self.pressed == 'P':
                # ściana prawa
                if self.position[0] >= 700 - self.mario_width - 3:
                    self.boost = True
                if self.position[0] < 700 - self.mario_width - 3:
                    self.temp = self.speed_x
                self.inverted = False

        if self.temp > 0:
            self.temp -= self.drag
        elif self.temp < 0:
            self.temp += self.drag

        self.position[0] += self.temp

        # sterowanie gestami - płynnie
        if self.control_option == 3:
            self.skip = (self.skip + 1) % 6
            if self.skip == 0:
                self.control.tick()
                self.position[0] = self.control.position2()

        # grawitacja
        self.velocity -= -self.gravity

        # kolizja z platformą
        if self.game.platforma_startowa is not None:
            if pygame.Rect.colliderect(self.game.platforma_startowa.platform, self.contour):
                self.velocity = -3.2
                if self.boost:
                    self.velocity = -6
                    self.boost = False
                    self.rotate = True
                    self.rotate_direction = self.inverted

        for platform in self.game.platforms:
            if self.position[1] + self.mario_hight < platform.y:
                platform.under_player = True
            if self.position[1] + self.mario_hight - 10 > platform.y:
                platform.under_player = False

            if pygame.Rect.colliderect(platform.platform, self.contour):
                if self.velocity > 0 and platform.under_player is True:
                    self.velocity = -3.2
                    if self.boost:
                        self.velocity = -6
                        self.boost = False
                        self.rotate = True
                        self.rotate_direction = self.inverted
                    platform.collision()
                    # print("{} + {} > {}".format(self.position[1], self.mario_hight, platform.y))


        # ruch oraz wartość przesunięcia platform
        if self.position[1] <= 300 and self.velocity < 0:
            self.slide = self.velocity
        else:
            self.slide = 0
            self.position[1] += self.velocity

        # salto mario
        if self.rotate is True:
            if self.inverted:
                self.angle += 3
            else:
                self.angle -= 3

            if self.angle == 360 or self.angle == -360:
                self.rotate = False
                self.angle = 0

    def draw(self):
        image = pygame.transform.flip(self.image, self.inverted, False)  # odbicie lustrzane
        position = (self.position[0], self.position[1])
        image = pygame.transform.rotate(image, self.angle)
        self.game.screen.blit(image, position)  # wyświetlenie mario

        self.contour = pygame.Rect(self.position[0], self.position[1], self.mario_width, self.mario_hight)
        # pygame.draw.rect(self.game.screen, (200, 200, 200), self.contour, 2)

    def __del__(self):
        self.control.remove()