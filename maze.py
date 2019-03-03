import pygame
from imagerect import ImageRect


class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 13

    def __init__(self, screen, mazefile, brickfile, shieldfile, dotfile, powerpillfile):
        self.screen = screen.screen
        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

            self.bricks = []
            self.dots = []
            self.powerpills = []
            self.barriers = []

            self.a = []
            self.b = []
            self.c = []
            self.d = []
            self.e = []
            self.f = []
            self.g = []
            self.h = []
            self.i = []
            self.j = []


            sz = Maze.BRICK_SIZE
            self.brick = ImageRect(screen, brickfile, sz, sz)
            self.dot = ImageRect(screen, dotfile, 3, 3)
            self.powerpill = ImageRect(screen, powerpillfile, 15, 15)
            self.barrier = ImageRect(screen, shieldfile, sz, sz)
            self.deltax = self.deltay = Maze.BRICK_SIZE

            self.first = True
            self.build()

    def __str__(self): return 'maze(' + self.filename + ')'

    def build(self):
        r = self.brick.rect
        w, h = r.width, r.height
        dx, dy = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'x':
                    self.bricks.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 'z':
                    self.dots.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 'p':
                    self.powerpills.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 'o':
                    self.barriers.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 'e':
                    self.e.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 'h':
                    self.h.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 'i':
                    self.i.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 'j':
                    self.j.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 'c':
                    self.c.append(pygame.Rect(ncol * dx, nrow * dy, w, h))

    def blitme(self):
        try:
            if self.first:
                x_change = 300
                y_change = 100
                self.first = False
            else:
                x_change = 0
                y_change = 0
            for rect in self.bricks:
                rect.x += x_change
                rect.y += y_change
                self.screen.blit(self.brick.image, rect)
            for rect in self.dots:
                rect.x += x_change
                rect.y += y_change
                self.screen.blit(self.dot.image, rect)
            for rect in self.powerpills:
                rect.x += x_change
                rect.y += y_change
                self.screen.blit(self.powerpill.image, rect)
            for rect in self.barriers:
                rect.x += x_change
                rect.y += y_change
                self.screen.blit(self.barrier.image, rect)
        except Exception:
            pass
