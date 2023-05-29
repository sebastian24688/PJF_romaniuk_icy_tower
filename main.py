import pygame, sys, random
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
        self.platrorma_startowa = Platform(self, 100, self.screen_y - 100, 600)
        self.platforms = []
        min_distance = 100 # minimalna odległość między platformami
        offtop = 40
        y_position = self.screen_y - 100
        self.player = Player(self)

        for i in range(4):
            x = random.randint(100, 600)
            y_position = y_position - min_distance - random.randint(0, offtop)
            width = random.randint(70, 150)
            self.platforms.append(Platform(self, x, y_position, width))

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
        self.platrorma_startowa.draw()
        for i in self.platforms:
            i.draw()
        self.player.draw()


Game()