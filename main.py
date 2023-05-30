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
        self.slide_border = 300
        self.background_y = 0

        for i in range(8):
            x = random.randint(100, 600)
            y_position = y_position - min_distance - random.randint(0, offtop)
            width = random.randint(70, 150)
            self.platforms.append(Platform(self, x, y_position, width))

        # obrazy
        self.background1 = pygame.image.load("obrazki/tlo2.png").convert()
        self.background2 = pygame.image.load("obrazki/tlo2.png").convert()
        self.granica = pygame.Rect(100, 0, 600, 300)

        while True:
            # zegar
            self.clock.tick(self.FPS)

            # obsługa eventów
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            # przesuwanie tła i platform
            y_position -= self.player.slide
            for platform in self.platforms:
                platform.y -= self.player.slide
                if platform.y > self.screen_y + 50:
                    self.platforms.remove(platform)
                    x = random.randint(100, 600)
                    y_position = y_position - min_distance - random.randint(0, offtop)
                    width = random.randint(70, 150)
                    self.platforms.append(Platform(self, x, y_position, width))
            self.background_y = self.background_y % self.screen_y
            self.background_y -= self.player.slide



            # zdarzenia
            self.tick()
            self.draw()
            pygame.display.flip()

    def tick(self):
        self.player.tick()

    def draw(self):
        self.screen.blit(self.background1, (0, self.background_y))
        self.screen.blit(self.background1, (0, self.background_y-800))
        self.platrorma_startowa.draw()
        for i in self.platforms:
            i.draw()
        self.player.draw()
        pygame.draw.rect(self.screen, (255,255,255),self.granica,2)


Game()