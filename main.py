import pygame
import sys
from my_game import Game


class Menu:
    def __init__(self):
        # parametry
        self.screen_x = 800
        self.screen_y = 800

        # inicjalizacja
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption("Mario Tower")
        self.options = ["Start Game", "High Scores", "Exit"]
        self.control_options = ["Keys", "Camera1", "Camera2"]
        self.selected_option = 0
        self.selected_control = 0

        # obrazy
        self.background = pygame.image.load("obrazki/tlo2.png").convert()
        self.font_logo = pygame.font.SysFont('Arial', 180)
        self.font_options = pygame.font.SysFont('Arial', 80)
        self.font_title = pygame.font.SysFont('Arial', 120)
        self.font_score = pygame.font.SysFont('Arial', 45)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:
                            self.start_game()
                        elif self.selected_option == 1:
                            self.high_scores()
                        elif self.selected_option == 2:
                            sys.exit(0)

            self.draw_menu()
            pygame.display.flip()

    def start_game(self):
        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_UP:
                        self.selected_control = (self.selected_control - 1) % len(self.control_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_control = (self.selected_control + 1) % len(self.control_options)
                    elif event.key == pygame.K_RETURN:
                        choosing = False

            self.draw_control()
            pygame.display.flip()


        game = Game(self.screen, self.screen_x, self.screen_y, self.selected_control+1)
        score = game.run()

        with open('score.txt', 'a') as file:
            file.write(str(score) + '\n')

        self.game_over(score)

    def game_over(self, score):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN):
                    return

            self.draw_game_over(score)
            pygame.display.flip()

    def high_scores(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN):
                    return

            self.draw_high_scores()
            pygame.display.flip()

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))
        logo1 = self.font_logo.render("MARIO", True, (134, 16, 16))
        logo2 = self.font_logo.render("TOWER", True, (134, 16, 16))
        logo1_rect = logo1.get_rect()
        logo2_rect = logo2.get_rect()
        logo1_rect.center = (self.screen_x // 2, 130)
        logo2_rect.center = (self.screen_x // 2, 300)
        self.screen.blit(logo1, logo1_rect)
        self.screen.blit(logo2, logo2_rect)


        for i, option in enumerate(self.options):
            if i == self.selected_option:
                text = self.font_options.render(option, True, (150, 50, 50))
            else:
                text = self.font_options.render(option, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (self.screen_x // 2, (2 * self.screen_y // 3) + i * 80)
            self.screen.blit(text, text_rect)

    def draw_control(self):
        self.screen.fill((0, 0, 0))

        text1 = self.font_options.render("CHOOSE", True, (134, 16, 16))
        text2 = self.font_options.render("CONTROL OPTION", True, (134, 16, 16))
        text1_rect = text1.get_rect()
        text2_rect = text2.get_rect()
        text1_rect.center = (self.screen_x // 2, 130)
        text2_rect.center = (self.screen_x // 2, 220)
        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)

        for i, option in enumerate(self.control_options):
            if i == self.selected_control:
                text = self.font_options.render(option, True, (150, 50, 50))
            else:
                text = self.font_options.render(option, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (self.screen_x // 2, ( self.screen_y // 2) + i * 80)
            self.screen.blit(text, text_rect)

    def draw_scores(self, last_score=None):
        with open("score.txt", "r") as file:
            lines = file.readlines()
            lines = [score.strip() for score in lines]

        scores = sorted([int(score) for score in lines], reverse=True)

        score_number = 10
        if len(scores) < score_number:
            score_number = len(scores)

        for i in range(0, score_number):
            if last_score is not None and scores[i] == last_score:
                text = self.font_score.render(str(i + 1) + ". " + str(scores[i]), True, (0, 255, 0))
            else:
                text = self.font_score.render(str(i + 1) + ". " + str(scores[i]), True, (255, 255, 255))

            self.screen.blit(text, (self.screen_x // 8, (self.screen_y // 3) + i * 45))

    def draw_game_over(self, score):
        self.screen.fill((0, 0, 0))
        title_text = self.font_title.render("GAME OVER", True, (134, 16, 16))
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (self.screen_x // 2, 130)
        self.screen.blit(title_text, title_text_rect)
        self.draw_scores(score)

    def draw_high_scores(self):
        self.screen.fill((0, 0, 0))
        title_text = self.font_title.render("HIGH SCORES", True, (134, 16, 16))
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (self.screen_x // 2, 130)
        self.screen.blit(title_text, title_text_rect)
        self.draw_scores()


menu = Menu()
menu.run()
