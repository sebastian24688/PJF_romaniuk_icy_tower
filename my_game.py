import pygame, sys, random
from player import Player
from my_platform import Platform


class Game:
    def __init__(self, screen, screen_x, screen_y, selected_control):
        # parametry
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.FPS = 250

        # inicjalizacja
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.platforma_startowa = Platform(self, 100, self.screen_y - 100, 600, [1, 0, 0])
        self.platforms = []
        self.min_distance = 40  # minimalna odległość między platformami
        self.extra_distance = 50  # wysokość między platformami = min. odległość + offtop
        self.y_position = self.screen_y - 100
        self.min_width = 100
        self.max_width = 200
        self.player = Player(self, selected_control)
        self.slide_border = 300
        self.background_y = 0
        self.platform_type_possibility = [0.8, 0.1, 0.1]
        self.score = 0
        self.level = 500

        # utworzenie platform
        for i in range(20):
            width = random.randint(self.min_width, self.max_width)
            x = random.randint(100, 700 - width)
            self.y_position = self.y_position - self.min_distance - random.randint(0, self.extra_distance)
            self.platforms.append(Platform(self, x, self.y_position, width, self.platform_type_possibility))

        # obrazy
        self.background1 = pygame.image.load("obrazki/tlo2.png").convert()
        self.background2 = pygame.image.load("obrazki/tlo2.png").convert()
        self.granica = pygame.Rect(100, 0, 600, 300)
        self.font = pygame.font.SysFont('Arial', 36)

    def run(self):
        while self.player.position[1] < self.screen_x + 300:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return round(self.score//10)

            # przesuwanie tła i platform
            self.y_position -= self.player.slide
            self.score -= self.player.slide
            if self.platforma_startowa is not None:
                self.platforma_startowa.y -= self.player.slide
                if self.platforma_startowa.y > 850:
                    del self.platforma_startowa
                    self.platforma_startowa = None

            for platform in self.platforms:
                platform.y -= self.player.slide
                if platform.y > self.screen_y + 50 or platform.collision_count <= 0:
                    self.platforms.remove(platform)
                    width = random.randint(self.min_width, self.max_width)
                    x = random.randint(100, 700 - width)
                    self.y_position = self.y_position - self.min_distance - random.randint(0, self.extra_distance)
                    self.platforms.append(Platform(self, x, self.y_position, width, self.platform_type_possibility))
            self.background_y = self.background_y % self.screen_y
            self.background_y -= self.player.slide

            # poziomy trudności
            if self.score//10 > self.level:
                self.level += 500
                if self.platform_type_possibility[0] > 0.1:
                    self.platform_type_possibility[0] -= 0.1
                    self.platform_type_possibility[1] += 0.05
                    self.platform_type_possibility[2] += 0.05

                # odległośc między platformami
                self.min_distance += 20 if self.min_distance < 120 else 0
                self.extra_distance -= 10 if self.extra_distance > 0 else 0
                # szerokość platform
                self.min_width -= 10 if self.min_width > 40 else 0
                self.max_width -= 30 if self.max_width > 50 else 0


            # zdarzenia
            self.tick()
            self.draw()
            pygame.display.flip()

        del self.player
        return round(self.score//10)

    def tick(self):
        self.player.tick()
        for platform in self.platforms:
            platform.tick()

    def draw(self):
        self.screen.blit(self.background1, (0, self.background_y))
        self.screen.blit(self.background1, (0, self.background_y - 800))
        if self.platforma_startowa is not None:
            self.platforma_startowa.draw()
        for platform in self.platforms:
            platform.draw()
        self.player.draw()
        # pygame.draw.rect(self.screen, (255, 255, 255), self.granica, 2)
        # punkty
        text_surface = self.font.render('SCORE: ' + str(round(self.score//10)), True, (0, 0, 0))
        self.screen.blit(text_surface, (110, self.screen_y - 43))