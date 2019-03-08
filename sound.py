import pygame
pygame.init()


class Sound:

    def __init__(self):
        self.stop = False
        self.chomp_sound = pygame.mixer.Sound('sound/pacman_chomp.wav')
        self.hit_sound = pygame.mixer.Sound('sound/pacman_death.wav')
        self.hit_sound = pygame.mixer.Sound('sound/pacman_eatghost.wav')
        self.fruit = pygame.mixer.Sound('sound/pacman_eatfruit.wav')
        self.start_music = pygame.mixer.Sound('sound/pacman_intermission.wav')
        self.fire = pygame.mixer.Sound("sound/portal_fire.wav")

    def chomp(self):
        self.chomp_sound.play()

    def stop_chomp(self):
        self.chomp_sound.fadeout(1)

    def pacman_hit(self):
        self.hit_sound.play()

    def ghost_hit(self):
        self.hit_sound.play()

    def eat_fruit(self):
        self.fruit.play()

    def background_music(self):
        self.start_music.play()
