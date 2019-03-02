import pygame
from pygame import gfxdraw
from imagerect import ImageRect
from timer import Timer


class Portal:
    NUM_FRAMES = 10

    def __init__(self, screen, x, y, color, wait=10):
        self.screen = screen
        self.x, self.y = x, y
        self.color = color
        self.opensize = Portal.NUM_FRAMES

        self.frames = self.loadimages(color)

        self.timeropening = Timer(frames=self.frames, wait=wait, frameindex=0, step=1, looponce=True)
        self.timerclosing = Timer(frames=self.frames, wait=wait, frameindex=len(self.frames) - 1, step=-1,
                                  looponce=True)
        self.timer = None

        self.rect = pygame.Rect(x, y, self.opensize, self.opensize)
        self.isopen = False
        self.isclosed = False
        self.portal_opening = pygame.mixer.Sound("sounds/portal_opening.wav")
        self.portal_closing = pygame.mixer.Sound("sounds/portal_closing.wav")


    def __str__(self): return 'Portal(' + str(self.x) + ',' + str(self.y) +\
                              ', color=' + str(self.color) + ', begin:' + str(self.begin) + ')'

    def loadimages(self, color):
        frames = []
        filename = 'portal_' + color
        for sz in range(Portal.NUM_FRAMES):
            size = int(5 * sz)
            frames.append(ImageRect(self.screen, filename, height=size, width=size))
        return frames

    def open(self, game):
        other = game.portals[0] if self == game.portals[1] else game.portals[0]
        if self.isopen:    # close open portal of same color and reopen it here
            self.close()
        if self.rect.colliderect(other.rect):   # if opening it will overlap other portal, close other too
            other.close()

        pman = game.pacman
        s = pman.posn + 150 * pman.velocity    # s = vt (assume t = 1)
        self.x, self.y = s.x, s.y
        self.rect.x, self.rect.y = self.x, self.y
        # self.rect.x -= int(self.rect.width/2)
        # self.rect.y -= int(self.rect.height/2)
        self.timer = self.timeropening
        self.timer.reset()
        pygame.mixer.Sound.play(self.portal_opening)
        self.isopen = True
        self.isclosed = False

    def close(self):
        if self.isclosed: return

        self.timer = self.timerclosing
        self.timer.reset()
        pygame.mixer.Sound.play(self.portal_closing)
        self.isopen = False
        self.isclosed = True

    def collide_with(self, rect):
        k = 4    # force tiny overlap
        ssmaller = self.rect.inflate(rect.width/k, rect.height/k)
        rsmaller = rect.inflate(rect.width/k, rect.height/k)
        return ssmaller.colliderect(rsmaller)
        # return self.rect.colliderect(rect)

    @staticmethod
    def attempt_transport(character, game):
        if not (game.portals[0].isopen and game.portals[1].isopen): return False
        char = character
        ocollide = game.portals[0].collide_with(char.rect)
        bcollide = game.portals[1].collide_with(char.rect)
        if (not ocollide and not bcollide): return False

        other = game.portals[1] if ocollide else game.portals[0]
        char.posn.x, char.posn.y = other.rect.x, other.rect.y
        other.close()
        return True

    def blit(self):
        if not self.isopen and not self.isclosed:
            return
        imgrect = self.timer.imagerect()
        self.screen.blit(imgrect.image, self.rect)
