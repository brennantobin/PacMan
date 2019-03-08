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

        self.expand = False
        self.compress = False

    # def update(self):

    def draw(self):
        # draw the bullet onto the screen
        self.screen.screen.blit(self.image, self.rect)
