import pygame
from pygame.sprite import Sprite


class BluePortal(Sprite):

    def __init__(self, screen, bullet_rect):

        super(BluePortal, self).__init__()
        self.screen = screen

        self.image = pygame.image.load("sprites/vPortal.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

        self.rect.x = bullet_rect.x
        self.rect.y = bullet_rect.y

        self.expand = True
        self.expansion_counter = 5
        self.compress = False
        self.compression_counter = 5

    def update(self):
        if self.expand:
            self.image = pygame.transform.scale(self.image, (self.expansion_counter, self.expansion_counter))
            self.expansion_counter += 5
        if self.expansion_counter >= 30:
            self.expansion_counter = 0
            self.expand = False
        if self.compress:
            self.image = pygame.transform.scale(self.image, (self.compression_counter, self.compression_counter))
            self.compression_counter -= 5
        if self.compression_counter <= 0:
            self.compress = False
            self.expand = True

    def draw(self):
        # draw the bullet onto the screen
        self.screen.screen.blit(self.image, self.rect)
