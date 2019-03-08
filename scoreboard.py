import pygame.font
from pygame.sprite import Group
from pacman import PacMan


class Scoreboard:
    def __init__(self, screen, pacmen, ghosts):
        self.screen = screen
        self.pacmen = pacmen
        self.ghosts = ghosts
        self.life = 3
        self.screen_rect = screen.screen.get_rect()

        self.dot_points = 10
        # self.ghost_points

        self.no_fruit = False
        self.no_new_fruit = False

        self.reset_stats()
        self.game_active = False

        f = open('highscores.txt', 'r')
        score = f.read()
        self.high_score = int(score)
        f.close()

        self.score_scale = 1.5
        self.score = 0
        self.level = 1

        self.text_color = (100, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_pacman()

    def get_score(self):
        return int(round(self.score, -1))

    def prep_score(self):
        rounded_score = int(round(self.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.screen.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 100
        self.score_rect.top = 20

    def show_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.prep_high_score()
        self.screen.screen.blit(self.score_image, self.score_rect)
        self.screen.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.screen.blit(self.level_image, self.level_rect)
        self.pacmen_lives.draw(self.screen.screen)
        self.screen.make_title("Pac Man", 68, (255, 255, 255), 30, self.screen.rect.centerx + 20)

    def prep_high_score(self):
        high_score = int(round(self.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.screen.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.score_rect.centerx
        self.high_score_rect.top = self.score_rect.bottom + 10

    def prep_level(self):
        self.level_image = self.font.render(str(self.level), True, self.text_color, self.screen.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 50

    def prep_pacman(self):
        self.pacmen_lives = Group()
        x_location = 5
        for pacman_number in range(self.pacman_left):
            pacman = PacMan(self.screen, self.pacmen, self.ghosts)
            pacman.change_location(x_location, 5)
            x_location += 5
            pacman.update()
            pacman.rect.x = 10 + pacman_number * pacman.rect.width
            pacman.rect.y = 10
            self.pacmen_lives.add(pacman)

    def reset_stats(self):
        self.pacman_left = self.life
        self.score = 0
        self.level = 1
