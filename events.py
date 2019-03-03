import pygame
import sys


def check_events(buttons, play_button, score_button, back_button, pacman, pacmen, ghosts, screen):
    for event in pygame.event.get():
        for pacman in pacmen:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                check_key_down(event, pacman, screen)
            #if event.type == pygame.KEYUP:
            #    check_keyup_events(event, pacman, screen)
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
            pacman.ismoving_down = False
            pacman.ismoving_up = False
            pacman.ismoving_left = False
            pacman.ismoving_right = True
            pacman.ismoving = True
        elif event.key == pygame.K_LEFT:
            pacman.ismoving_down = False
            pacman.ismoving_up = False
            pacman.ismoving_right = False
            pacman.ismoving_left = True
            pacman.ismoving = True
        elif event.key == pygame.K_UP:
            pacman.ismoving_down = False
            pacman.ismoving_left = False
            pacman.ismoving_right = False
            pacman.ismoving_up = True
            pacman.ismoving = True
        elif event.key == pygame.K_DOWN:
            pacman.ismoving_up = False
            pacman.ismoving_left = False
            pacman.ismoving_right = False
            pacman.ismoving_down = True
            pacman.ismoving = True
        # if event.key == pygame.K_SPACE:
        #     fire_bullet(settings, screen, ship, bullets, sound)
    if event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, pacman, screen):
    if screen.game_active:
        if event.key == pygame.K_RIGHT:
            pacman.ismoving = False
            pacman.ismoving_right = False
        if event.key == pygame.K_LEFT:
            pacman.ismoving = False
            pacman.ismoving_left = False
        if event.key == pygame.K_UP:
            pacman.ismoving = False
            pacman.ismoving_up = False
        if event.key == pygame.K_DOWN:
            pacman.ismoving = False
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


def hit_block(pacman, maze, ghosts):
    k = len(maze.dots)
    for j in range(k):
        if pygame.Rect.colliderect(pacman.rect, maze.dots[j]):
            del(maze.dots[j])
            # pacman.waka.play()
            # ai_settings.score += 50 * ai_settings.level
            # if ai_settings.score > ai_settings.hs:
            #     ai_settings.hs = ai_settings.score
            break
    for l in range(len(maze.powerpills)):
        if pygame.Rect.colliderect(pacman.rect, maze.powerpills[l]):
            del(maze.powerpills[l])
            # blues.play()
            for ghost in ghosts:
                ghost.is_blue = True
            break

    for i in range(len(maze.bricks)):
        for rect in maze.barriers:
            if pygame.Rect.colliderect(pacman.rect, maze.bricks[i]) or pygame.Rect.colliderect(pacman.rect, rect):
                # possible fix ---- find if it collides with top bottom left or right of the pacman
                if pacman.ismoving_right:
                    pacman.rect.centerx -= pacman.moving_speed
                    pacman.ismoving_right = False
                    pacman.ismoving_left = True
                    return
                    # pacman.moving_right = False
                if pacman.ismoving_left:
                    pacman.rect.centerx += pacman.moving_speed
                    pacman.ismoving_left = False
                    pacman.ismoving_right = True
                    return
                    # pacman.moving_left = False

    # i = 0
    for i in range(len(maze.bricks)):
        for rect in maze.barriers:
            if pygame.Rect.colliderect(pacman.rect, maze.bricks[i]) or pygame.Rect.colliderect(pacman.rect, rect):
                if pacman.ismoving_up:
                    pacman.rect.centery += pacman.moving_speed
                    pacman.ismoving_up = False
                    pacman.ismoving_down = True
                    return
                    # pacman.moving_up = False
                if pacman.ismoving_down:
                    pacman.rect.centery -= pacman.moving_speed
                    pacman.ismoving_down = False
                    pacman.ismoving_up = True
                    return
                    # pacman.moving_down = False
