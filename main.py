import pygame, sys
from player import Player
from platform import Platform

class Game(object):
    def __init__(self):
        # parametry
        self.screen_x = 800
        self.screen_y = 800
        self.FPS = 250

        # inicjalizacja
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.platrorma_startowa = Platform(self)

        # obrazy
        self.tlo = pygame.image.load("obrazki/tlo2.png").convert()

        while True:
            # zegar
            self.clock.tick(self.FPS)

            # obsługa eventów
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            # zdarzenia
            self.tick()
            self.draw()
            pygame.display.flip()

    def tick(self):
        self.player.tick()

    def draw(self):
        self.screen.blit(self.tlo, (0, 0))
        self.player.draw()
        self.platrorma_startowa.draw()


Game()