import pygame
from sprite_sheet import SpriteSheet
from pygame.sprite import Sprite


class PacMan(Sprite):
    def __init__(self, screen, pacmen, ghosts):
        super(PacMan, self).__init__()

        self.pacmen = pacmen
        self.ghosts = ghosts
        self.direction = 'right'
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
                    self.screen.reset(self.pacmen, self.ghosts)

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

