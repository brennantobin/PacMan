import pygame


class Sound:

    def __init__(self):
        self.stop = False

    def chomp(self):
        pacman_chomp = pygame.mixer.Sound('sounds/pacman_chomp.wav')
        pacman_chomp.play()

    def pacman_hit(self):
        hit_sound = pygame.mixer.Sound('sounds/pacman_death.wav')
        hit_sound.play()

    def ghost_hit(self):
        hit_sound = pygame.mixer.Sound('sounds/pacman_eatghost.wav')
        hit_sound.play()

    def eat_fruit(self):
        fruit = pygame.mixer.Sound('sounds/pacman_eatfruit.wav')
        fruit.play()

    def background_music(self):
        start_music = pygame.mixer.Sound('sounds/pacman_intermission.wav')
        start_music.play()
