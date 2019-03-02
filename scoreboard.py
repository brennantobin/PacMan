import pygame.font


class Scoreboard:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.screen.get_rect()

        self.reset_stats()
        self.game_active = False
        self.high_score = 0
        self.score_scale = 1.5
        self.score = 0
        self.level = 1

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        # self.prep_ships()

    def get_score(self):
        return int(round(self.score, -1))

    def prep_score(self):
        rounded_score = int(round(self.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.screen.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # self.ships.draw(self.screen)

    def prep_high_score(self):
        high_score = int(round(self.high_score, -1))

        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.screen.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        self.level_image = self.font.render(str(self.level), True, self.text_color, self.screen.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    # def prep_ships(self):
    #     self.ships = Group()
    #     for ship_number in range(self.stats.ships_left):
    #         ship = Ship(self.settings, self.screen, self.stats)
    #         ship.update()
    #         ship.rect.x = 10 + ship_number * ship.rect.width
    #         ship.rect.y = 10
    #         self.ships.add(ship)

    def reset_stats(self):
        # self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
