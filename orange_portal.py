import pygame
from pygame.sprite import Sprite


class OrangePortal(Sprite):

    def __init__(self, screen, bullet_rect):
        super(OrangePortal, self).__init__()
        self.screen = screen

        self.image = pygame.image.load("sprites/hPortal.png")
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
