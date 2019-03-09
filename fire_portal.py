import pygame
from pygame.sprite import Sprite


class FirePortal(Sprite):

    def __init__(self, screen, pacman):

        super(FirePortal, self).__init__()
        self.screen = screen

        self.image = pygame.image.load("sprites/red_block.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()

        self.up = pacman.ismoving_up
        self.down = pacman.ismoving_down
        self.right = pacman.ismoving_right
        self.left = pacman.ismoving_left

        # you must be moving to fire the portal
        if self.up:
            self.rect.x = pacman.rect.centerx - 10
            self.rect.y = pacman.rect.top
        if self.down:
            self.rect.x = pacman.rect.centerx - 10
            self.rect.y = pacman.rect.bottom
        if self.right:
            self.rect.x = pacman.rect.right
            self.rect.y = pacman.rect.centery - 10
        if self.left:
            self.rect.x = pacman.rect.left
            self.rect.y = pacman.rect.centery - 10

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.speed_factor = 5

    def update(self):
        # moving the bullet
        if self.up:
            self.y -= self.speed_factor
            self.rect.y = self.y
        if self.down:
            self.y += self.speed_factor
            self.rect.y = self.y
        if self.right:
            self.x += self.speed_factor
            self.rect.x = self.x
        if self.left:
            self.x -= self.speed_factor
            self.rect.x = self.x

    def draw(self):
        # draw the bullet onto the screen
        self.screen.screen.blit(self.image, self.rect)
