import pygame
import sys


def check_events(buttons, play_button, score_button, back_button, pacman, pacmen, ghosts, screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            check_key_down(event, pacman, screen)
        if event.type == pygame.KEYUP:
            check_keyup_events(event, pacman, screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            play_button.check_play_button(mouse_x, mouse_y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            score_button.check_score_button(mouse_x, mouse_y, buttons, back_button)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            back_button.check_back_button(mouse_x, mouse_y, buttons,
                                          play_button, score_button, pacman, pacmen, ghosts)


def check_key_down(event, pacman, screen):
    if screen.game_active:
        if event.key == pygame.K_RIGHT:
            pacman.ismoving_right = True
        elif event.key == pygame.K_LEFT:
            pacman.ismoving_left = True
        elif event.key == pygame.K_UP:
            pacman.ismoving_up = True
        elif event.key == pygame.K_DOWN:
            pacman.ismoving_down = True
        # if event.key == pygame.K_SPACE:
        #     fire_bullet(settings, screen, ship, bullets, sound)
    if event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, pacman, screen):
    if screen.game_active:
        if event.key == pygame.K_RIGHT:
            pacman.ismoving_right = False
        if event.key == pygame.K_LEFT:
            pacman.ismoving_left = False
        if event.key == pygame.K_UP:
            pacman.ismoving_up = False
        if event.key == pygame.K_DOWN:
            pacman.ismoving_down = False


def check_pacman_collision(pacmen, ghosts):
    kill_ghosts = False
    for ghost in ghosts:
        if ghost.is_blue or ghost.white:
            kill_ghosts = True
    if kill_ghosts:
        collisions = pygame.sprite.groupcollide(pacmen, ghosts, False, False)
    else:
        collisions = pygame.sprite.groupcollide(ghosts, pacmen, True, False)
    if collisions and kill_ghosts:
        for ghosts in collisions.values():
            for ghost in ghosts:
                ghost.is_dead = True
                ghost.is_blue = False
                ghost.is_white = False
                # sound.alien_hit()
                # settings.alien_points = explosion.ufo_points
                # scoreboard.score +=
                # scoreboard.prep_score()

    for ghost in ghosts:
        if collisions and not kill_ghosts and not ghost.white and not ghost.eye:
            for pacmen in collisions.values():
                for pacman in pacmen:
                    pacman.is_dead = True
                    pacman.destroy_pacman()

            for ghost in ghosts:
                ghost.ismoving = False
