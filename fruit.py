import pygame
from pygame.sprite import Sprite
from sprite_sheet import SpriteSheet
# from timer import Timer


class Fruit(Sprite):
    def __init__(self, screen, type_fruit):
        super(Fruit, self).__init__()
        self.is_dead = False
        self.type_fruit = type_fruit
        self.points = 0
        self.position = [(35, 50, 14, 14), (52, 50, 14, 14), (67, 50, 14, 14), (83, 50, 14, 14), (100, 50, 14, 14),
                         (115, 50, 14, 14), (132, 50, 14, 14), (147, 50, 14, 14)]
        self.location_x = 600
        self.location_y = 585
        self.screen = screen
        self.sprite_sheet = SpriteSheet('sprites/pacman.png')

        self.image = self.sprite_sheet.image_at(self.position[self.type_fruit], None)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = self.location_x
        self.rect.y = self.location_y

    def draw(self):
        self.screen.screen.blit(self.image, self.rect)

    def set_points(self):
        if self.type_fruit == 0:
            self.points = 100
        elif self.type_fruit >= 4:
            self.points = (self.type_fruit - 3) * 1000
        elif self.type_fruit == 1:
            self.points = 300
        elif self.type_fruit == 2:
            self.points = 500
        else:
            self.points = 700
