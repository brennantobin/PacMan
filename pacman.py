import pygame
from sprite_sheet import SpriteSheet
from pygame.sprite import Sprite


class PacMan(Sprite):
    def __init__(self, screen, pacmen, ghosts, maze, scoreboard):
        super(PacMan, self).__init__()

        self.maze = maze
        self.scoreboard = scoreboard
        self.pacmen = pacmen
        self.ghosts = ghosts
        self.next_direction = ''
        self.direction = ''
        self.no_node = False
        self.right_stopper = False
        self.left_stopper = False
        self.up_stopper = False
        self.down_stopper = False
        self.dont_stop = False
        self.right_allowed = False
        self.left_allowed = False
        self.up_allowed = False
        self.down_allowed = False

        self.a = False
        self.b = False
        self.c = False
        self.d = False
        self.e = False
        self.f = False
        self.g = False
        self.h = False
        self.i = False
        self.j = False
        self.k = False
        self.l = False
        self.m = False

        # each of these are coordinates to the location and size
        # of the sprite on the sheet
        self.is_big = False
        self.big_open = (35, 15, 30, 35)
        self.big_mid = (65, 15, 34, 35)
        self.big_close = (97, 15, 35, 34)

        self.up_open = (4, 30, 16, 16)
        self.up_mid = (19, 30, 16, 16)
        self.close = (34, 0, 15, 15)

        self.down_open = (4, 47, 16, 16)
        self.down_mid = (19, 47, 16, 16)

        self.left_open = (4, 15, 16, 16)
        self.left_mid = (19, 15, 16, 16)

        self.right_open = (4, 0, 15, 15)
        self.right_mid = (20, 0, 15, 15)

        self.destroy_wait = 100
        self.destroy_last = 0
        self.animate = 0
        self.is_dead = False
        self.destroy = [(50, 0, 15, 15), (67, 0, 15, 15), (83, 0, 15, 15),
                        (98, 0, 16, 15), (115, 0, 16, 15), (130, 0, 16, 15),
                        (146, 0, 16, 15), (161, 0, 16, 15), (176, 0, 16, 15),
                        (191, 0, 16, 15), (208, 0, 16, 16)]

        self.position = self.big_open
        self.location_x = 0
        self.location_y = 220
        self.screen = screen
        self.sprite_sheet = SpriteSheet('sprites/pacman.png')

        self.image = self.sprite_sheet.image_at(self.position, None)
        if not self.is_big:
            self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = self.location_x
        self.rect.y = self.location_y

        self.ismoving = False
        self.ismoving_up = False
        self.ismoving_down = False
        self.ismoving_right = False
        self.ismoving_left = False

        self.wait_count = 100
        self.last = 0
        self.time = pygame.time.get_ticks()
        self.animation_counter = 1
        self.moving_speed = 4.00

    def update(self):
        if self.screen.game_active:
            if self.ismoving_right or self.ismoving_left and self.no_node:
                self.ismoving_up = False
                self.ismoving_down = False
            if self.ismoving_up or self.ismoving_down and self.no_node:
                self.ismoving_right = False
                self.ismoving_left = False
            if self.ismoving_right and self.right_stopper:
                self.ismoving_right = False
                self.ismoving = False
                self.change_type(self.right_mid)
            if self.ismoving_left and self.left_stopper:
                self.ismoving_left = False
                self.ismoving = False
                self.change_type(self.left_mid)
            if self.ismoving_up and self.up_stopper:
                self.change_type(self.up_mid)
                self.ismoving_up = False
                self.ismoving = False
            if self.ismoving_down and self.down_stopper:
                self.ismoving_down = False
                self.ismoving = False
                self.change_type(self.down_mid)

            if self.direction == 'right' and self.right_allowed or (self.next_direction == 'right' and self.right_allowed):
                self.ismoving_down = False
                self.ismoving_up = False
                self.ismoving_left = False
                self.ismoving_right = True
                self.ismoving = True
            elif self.direction == 'left' and self.left_allowed or (self.next_direction == 'left' and self.left_allowed):
                self.ismoving_down = False
                self.ismoving_up = False
                self.ismoving_right = False
                self.ismoving_left = True
                self.ismoving = True
            elif self.direction == 'up' and self.up_allowed or (self.next_direction == 'up' and self.up_allowed):
                self.ismoving_down = False
                self.ismoving_left = False
                self.ismoving_right = False
                self.ismoving_up = True
                self.ismoving = True
            elif self.direction == 'down' and self.down_allowed or (self.next_direction == 'down' and self.down_allowed):
                self.ismoving_up = False
                self.ismoving_left = False
                self.ismoving_right = False
                self.ismoving_down = True
                self.ismoving = True

        self.moving_down()
        self.moving_up()
        self.moving_left()
        self.moving_right()
        self.moving()
        if self.is_dead:
            now = pygame.time.get_ticks()
            if self.destroy_last == 0:
                self.destroy_last = now
            if self.destroy_last + self.destroy_wait < now:
                self.position = self.destroy[self.animate]
                self.image = self.sprite_sheet.image_at(self.position, None)
                if not self.is_big:
                    self.image = pygame.transform.scale(self.image, (30, 30))
                self.animate += 1
                self.destroy_wait += 75
                if self.animate >= 11:
                    self.remove(self.pacmen)
                    # self.screen.reset_the_game(self.maze, self.scoreboard, self, self.ghosts)
                    self.screen.reset_game = True

    def draw(self):
        self.screen.screen.blit(self.image, self.rect)

    def change_location(self, x_location, y_location):
        self.rect.x = x_location
        self.rect.y = y_location

    def change_type(self, position):
        self.position = position

    def moving_right(self):
        if self.ismoving_right:
            self.rect.x = self.rect.x + self.moving_speed

    def moving_left(self):
        if self.ismoving_left:
            self.rect.x = self.rect.x - self.moving_speed

    def moving_up(self):
        if self.ismoving_up:
            self.rect.y = self.rect.y - self.moving_speed

    def moving_down(self):
        if self.ismoving_down:
            self.rect.y = self.rect.y + self.moving_speed

    def moving(self):
        if self.ismoving:
            if self.ismoving_down:
                self.position = [self.down_open, self.down_mid,
                                 self.close, self.down_mid]
            if self.ismoving_up:
                self.position = [self.up_open, self.up_mid,
                                 self.close, self.up_mid]
            if self.ismoving_right:
                self.position = [self.right_open, self.right_mid,
                                 self.close, self.right_mid]
            if self.ismoving_left:
                self.position = [self.left_open, self.left_mid,
                                 self.close, self.left_mid]
            if not self.screen.game_active and self.is_big:
                self.position = [self.big_open, self.big_mid,
                                 self.big_close, self.big_mid]

            now = pygame.time.get_ticks()
            if self.last == 0:
                self.last = now
            if self.last + self.wait_count < now:
                self.position = self.position[self.animation_counter]
                self.image = self.sprite_sheet.image_at(self.position, None)
                if not self.is_big:
                    self.image = pygame.transform.scale(self.image, (30, 30))
                self.animation_counter += 1
                self.wait_count += 75
                if self.animation_counter >= 4:
                    self.animation_counter = 0

    def destroy_pacman(self):
        self.ismoving = False
        self.ismoving_down = False
        self.ismoving_left = False
        self.ismoving_right = False
        self.ismoving_up = False
        self.is_dead = True
        self.update()

