import pygame
from time import sleep


class Screen:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.rect = self.screen.get_rect()
        self.game_active = False
        self.score_active = False
        self.semiactive = False
        self.count = 0
        self.ghosts_destroyed = 0
        self.reset_game = True
        self.go_back = False

    def update(self, pacmen, ghosts):
        self.screen.fill(self.bg_color)
        if len(pacmen) > 0 or len(ghosts) > 0:
            pacmen.draw(self.screen)
            ghosts.draw(self.screen)
            pygame.display.flip()

    def start_screen(self, buttons, play_button, score_button, pacmen, ghosts):
        buttons.empty()
        if len(pacmen) == 0:
            self.make_title('Pac  Man', 100, (255, 255, 255), 200, 600)
            return
        buttons.add(play_button)
        buttons.add(score_button)
        if len(pacmen) == 1:
            for pacman in pacmen:
                if pacman.rect.x <= (self.rect.centerx-50):
                    pacman.ismoving_right = True
                    pacman.ismoving = True
                else:
                    pacman.ismoving_right = False
                    pacman.ismoving = False
        for pacman in pacmen:
            if pacman.rect.x >= (self.rect.centerx-50):
                self.make_title('Pa  Man', 100, (255, 255, 255, 255), 200, 600)
                if pacman.is_big:
                    pacman.change_type(pacman.big_mid)
                    pacman.image = pacman.sprite_sheet.image_at(pacman.position, None)
        for ghost in ghosts:
            if ghost.title_blinky and self.count == 0:
                self.make_title('"Blinky"', 48, (100, 0, 0), 400, 600)
            if ghost.title_pinky and self.count == 1:
                self.make_title('"Pinky"', 48, (200, 100, 100), 400, 600)
            if ghost.title_inky and self.count == 2:
                self.make_title('"Inky"', 48, (0, 0, 100), 400, 600)
            if ghost.title_clyde and self.count == 3:
                self.make_title('"Clyde"', 48, (250, 125, 0), 400, 600)

        pacmen.update()
        buttons.update()
        ghosts.update()
        pygame.display.flip()

    def score_screen(self, buttons, back_button):
        buttons.empty()
        buttons.add(back_button)
        self.make_title("High Scores", 48, (255, 255, 255), 200, 600)
        f = open('highscores.txt', 'r')
        score = f.read()
        self.make_title(score, 30, (255, 255, 255), 400, 600)
        f.close()
        buttons.update()
        pygame.display.flip()

    def game_screen(self, maze, node_maze, dijkstra_nodes, scoreboard, fruit):
        self.bg_color = (0, 0, 0)
        maze.blitme()
        if len(maze.dots) in range(25, 50) and not scoreboard.no_fruit:
            fruit.draw(self.screen)
        if len(maze.dots) in range(100, 125) and not scoreboard.no_new_fruit:
            fruit.draw(self.screen)
        node_maze.blitme()
        dijkstra_nodes.blitme()
        scoreboard.show_score()
        pygame.display.flip()

    def reset_the_game(self, maze, scoreboard, pacman, ghosts):
        sleep(0.1)
        maze.first = True
        maze.bricks = []
        maze.barriers = []
        maze.fill_powerpills()
        maze.fill_dots()
        maze.blitme()
        scoreboard.prep_level()
        scoreboard.prep_pacman()
        pacman.ismoving_right = False
        pacman.ismoving_left = False
        pacman.ismoving_down = False
        pacman.ismoving_up = False
        pacman.ismoving = False
        pacman.change_location(597, 585)
        location_counter = 0
        for ghost in ghosts:
            ghost.change_location(560 + location_counter, 390)
            # ghost.ismoving_up = True
            # ghost.ismoving = True
            location_counter += 30
        pygame.display.flip()

    def make_title(self, title, font_size, color, y_variant, x_variant):
        font = pygame.font.SysFont(None, font_size)
        title_image = font.render(title, True, color)
        title_image_rect = title_image.get_rect()
        title_image_rect.top = y_variant
        title_image_rect.centerx = x_variant
        self.screen.blit(title_image, title_image_rect)

    def screen_intro(self, pacman, ghosts):
        if self.count == 0:
            count = 1
            for ghost in ghosts:
                if ghost.rect.left > self.rect.right:
                    count += 1
            if count == len(ghosts):
                pacman.ismoving_right = False
                pacman.ismoving_left = True
                pacman.moving_speed += 0.5

                for ghost in ghosts:
                    ghost.ismoving_right = False
                    ghost.ismoving_left = True
                    ghost.is_blue = True

    def introduce_blinky(self, ghost):
        if ghost.color == 65:
            ghost.ismoving_left = False
            ghost.ismoving = True
            ghost.ismoving_right = True
            ghost.eye = False
            if ghost.rect.x >= 665:
                ghost.title_blinky = True
                ghost.ismoving_right = False
                ghost.ismoving = False
                now = pygame.time.get_ticks()
                if ghost.title_last == 0:
                    ghost.title_last = now
                if (ghost.title_last+ghost.wait) < now:
                    ghost.intro_blinky = True
                    ghost.title_blinky = False
                    ghost.ismoving_right = True
                    ghost.ismoving = True

    def introduce_pinky(self, ghost):
        if ghost.color == 81:
            ghost.ismoving_left = False
            ghost.ismoving = True
            ghost.ismoving_right = True
            ghost.eye = False
            if ghost.rect.x >= 665:
                ghost.title_pinky = True
                ghost.ismoving_right = False
                ghost.ismoving = False
                now = pygame.time.get_ticks()
                if ghost.title_last == 0:
                    ghost.title_last = now
                if (ghost.title_last + ghost.wait) < now:
                    ghost.intro_pinky = True
                    ghost.title_pinky = False
                    ghost.ismoving_right = True
                    ghost.ismoving = True

    def introduce_inky(self, ghost):
        if ghost.color == 97:
            ghost.ismoving_left = False
            ghost.ismoving = True
            ghost.ismoving_right = True
            ghost.eye = False
            if ghost.rect.x >= 665:
                ghost.title_inky = True
                ghost.ismoving_right = False
                ghost.ismoving = False
                now = pygame.time.get_ticks()
                if ghost.title_last == 0:
                    ghost.title_last = now
                if (ghost.title_last + ghost.wait) < now:
                    ghost.intro_inky = True
                    ghost.title_inky = False
                    ghost.ismoving_right = True
                    ghost.ismoving = True

    def introduce_clyde(self, ghost, ghosts):
        if ghost.color == 113:
            ghost.ismoving_left = False
            ghost.ismoving = True
            ghost.ismoving_right = True
            ghost.eye = False
            if ghost.rect.x >= 665:
                ghost.title_clyde = True
                ghost.ismoving_right = False
                ghost.ismoving = False
                now = pygame.time.get_ticks()
                if ghost.title_last == 0:
                    ghost.title_last = now
                if (ghost.title_last + ghost.wait) < now:
                    ghost.intro_clyde = True
                    ghost.title_clyde = False
                    ghost.ismoving_right = True
                    ghost.ismoving = True
                    if ghost.rect.left >= 10 + self.rect.right:
                        ghosts.empty()
