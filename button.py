import pygame.font
from pygame.sprite import Sprite


class Button(Sprite):

    def __init__(self, screen, msg, height_varient):
        super(Button, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.screen.get_rect()
        self.height_varient = height_varient

        self.width, self.height = 200, 50
        self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery + self.height_varient

        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def update(self):
        self.screen.screen.fill(self.button_color, self.rect)
        self.screen.screen.blit(self.msg_image, self.msg_image_rect)

    def check_play_button(self, mouse_x, mouse_y, scoreboard):
        button_clicked = self.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.screen.game_active:
            pygame.mouse.set_visible(False)
            self.screen.game_active = True
            scoreboard.prep_score()
            scoreboard.prep_high_score()
            scoreboard.prep_level()
            scoreboard.prep_pacman()

    def check_score_button(self, mouse_x, mouse_y, buttons, back_button):
        button_clicked = self.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.screen.game_active:
            self.screen.score_screen(buttons, back_button)
            self.screen.score_active = True

    def check_back_button(self, mouse_x, mouse_y, buttons, play_button, back_button, pacman, pacmen, ghosts):
        button_clicked = self.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.screen.game_active:
            self.screen.score_active = False
            # self.screen.start_screen(buttons, play_button, back_button, pacman, pacmen, ghosts)
