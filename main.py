import pygame, sys
from player import Player

class Game(object):
    def __init__(self):
        self.tps_max = 100.0
        self.screen_x = 800
        self.screen_y = 800

        #inicjalizacja
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0
        self.player = Player(self)

        #obrazy
        self.tlo = pygame.image.load("obrazki/tlo2.png").convert()

        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            self.tps_delta += self.tps_clock.tick() / 1000.0

            while self.tps_delta > 1 / self.tps_max:
                self.tick()
                self.tps_delta -= 1 / self.tps_max

            self.screen.blit(self.tlo, (0, 0))
            self.draw()
            self.player.draw()
            pygame.display.flip()

    def tick(self):
        self.player.tick()

    def draw(self):
        self.player.draw()


Game()