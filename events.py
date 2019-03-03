import pygame
import sys


def check_events(buttons, play_button, score_button, back_button, pacmen, ghosts, screen, scoreboard):
    for event in pygame.event.get():
        for pacman in pacmen:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                check_key_down(event, pacman, screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                play_button.check_play_button(mouse_x, mouse_y, scoreboard)
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
            pacman.next_direction = 'right'
        if event.key == pygame.K_LEFT:
            pacman.next_direction = 'left'
        if event.key == pygame.K_UP:
            pacman.next_direction = 'up'
        if event.key == pygame.K_DOWN:
            pacman.next_direction = 'down'
    if event.key == pygame.K_q:
        sys.exit()


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


def hit_block(scoreboard, pacman, maze, ghosts):
    for i in range(len(maze.bricks)):
        for rect in maze.barriers:
            if pygame.Rect.colliderect(pacman.rect, maze.bricks[i]) or pygame.Rect.colliderect(pacman.rect, rect):
                # possible fix ---- now pacman can't hit the walls
                pacman.ismoving_right = False
                pacman.ismoving_left = False
                pacman.ismoving_up = False
                pacman.ismoving_down = False
                pacman.ismoving = False
    # for i in range(len(maze.bricks)):
    #     for rect in maze.barriers:
    #         for ghost in ghosts:
    #             if pygame.Rect.colliderect(ghost.rect, maze.bricks[i]) or pygame.Rect.colliderect(ghost.rect, rect):
    #                 if ghost.ismoving_right:
    #                     ghost.rect.centerx -= ghost.moving_speed
    #                     ghost.ismoving_right = False
    #                     ghost.ismoving_left = True
    #                     return
#
    #                 if ghost.ismoving_left:
    #                     ghost.rect.centerx += ghost.moving_speed
    #                     ghost.ismoving_left = False
    #                     ghost.ismoving_right = True
    #                     return
#
    # for i in range(len(maze.bricks)):
    #     for rect in maze.barriers:
    #         for ghost in ghosts:
    #             if pygame.Rect.colliderect(ghost.rect, maze.bricks[i]) or pygame.Rect.colliderect(ghost.rect, rect):
    #                 if ghost.ismoving_up:
    #                     ghost.rect.centerx -= ghost.moving_speed
    #                     ghost.ismoving_up = False
    #                     ghost.ismoving_down = True
    #                     return
#
    #                 if ghost.ismoving_down:
    #                     ghost.rect.centerx += ghost.moving_speed
    #                     ghost.ismoving_down = False
    #                     ghost.ismoving_up = True
    #                     return
#
    k = len(maze.dots)
    if k == 0:
        scoreboard.level += 1
        scoreboard.prep_level()
    for j in range(k):
        if pygame.Rect.colliderect(pacman.rect, maze.dots[j]):
            del(maze.dots[j])
            scoreboard.score += scoreboard.dot_points
            scoreboard.prep_score()
            break
    for l in range(len(maze.powerpills)):
        if pygame.Rect.colliderect(pacman.rect, maze.powerpills[l]):
            del(maze.powerpills[l])
            # blues.play()
            for ghost in ghosts:
                ghost.is_blue = True
            break

    for l in range(len(maze.a)):
        if pygame.Rect.colliderect(pacman.rect, maze.a[l]):
            pacman.left_allowed = True
            pacman.right_allowed = False
            pacman.up_allowed = False
            pacman.down_allowed = False
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            pacman.rect = maze.a[l].rect
            if pacman.ismoving_right:
                pacman.right_stopper = True
            if pacman.next_direction == 'left':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.b)):
        if pygame.Rect.colliderect(pacman.rect, maze.b[l]):
            pacman.left_allowed = False
            pacman.right_allowed = True
            pacman.up_allowed = False
            pacman.down_allowed = False
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.ismoving_left:
                pacman.left_stopper = True
            if pacman.next_direction == 'right':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.c)):
        if pygame.Rect.colliderect(pacman.rect, maze.c[l]):
            pacman.dont_stop = True
            pacman.left_allowed = False
            pacman.right_allowed = False
            pacman.up_allowed = True
            pacman.down_allowed = True
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.next_direction == 'up' or pacman.next_direction == 'down':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.d)):
        if pygame.Rect.colliderect(pacman.rect, maze.d[l]):
            pacman.left_allowed = True
            pacman.right_allowed = False
            pacman.up_allowed = True
            pacman.down_allowed = False
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.ismoving_down:
                pacman.down_stopper = True
            if pacman.ismoving_right:
                pacman.right_stopper = True
            if pacman.next_direction == 'up' or pacman.next_direction == 'left':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.e)):
        if pygame.Rect.colliderect(pacman.rect, maze.e[l]):
            pacman.left_allowed = False
            pacman.right_allowed = True
            pacman.up_allowed = True
            pacman.down_allowed = False
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.ismoving_down:
                pacman.down_stopper = True
            if pacman.ismoving_left:
                pacman.left_stopper = True
            if pacman.next_direction == 'right' or pacman.next_direction == 'up':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.f)):
        if pygame.Rect.colliderect(pacman.rect, maze.f[l]):
            pacman.left_allowed = True
            pacman.right_allowed = False
            pacman.up_allowed = False
            pacman.down_allowed = True
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.ismoving_up:
                pacman.up_stopper = True
            if pacman.ismoving_right:
                pacman.right_stopper = True
            if pacman.next_direction == 'left' or pacman.next_direction == 'down':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.g)):
        if pygame.Rect.colliderect(pacman.rect, maze.g[l]):
            pacman.left_allowed = False
            pacman.right_allowed = True
            pacman.up_allowed = False
            pacman.down_allowed = True
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.ismoving_up:
                pacman.up_stopper = True
            if pacman.ismoving_left:
                pacman.left_stopper = True
            if pacman.next_direction == 'right' or pacman.next_direction == 'down':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.h)):
        if pygame.Rect.colliderect(pacman.rect, maze.h[l]):
            pacman.rect.center = (maze.h[l]).center
            pacman.left_allowed = True
            pacman.right_allowed = True
            pacman.up_allowed = False
            pacman.down_allowed = False
            pacman.dont_stop = True
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.next_direction == 'left' or pacman.next_direction == 'right':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.i)):
        if pygame.Rect.colliderect(pacman.rect, maze.i[l]):
            pacman.left_allowed = True
            pacman.right_allowed = True
            pacman.up_allowed = True
            pacman.down_allowed = False
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.ismoving_down:
                pacman.down_stopper = True
            if pacman.next_direction != 'down':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.j)):
        if pygame.Rect.colliderect(pacman.rect, maze.j[l]):
            pacman.left_allowed = True
            pacman.right_allowed = True
            pacman.up_allowed = False
            pacman.down_allowed = True
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.ismoving_up:
                pacman.up_stopper = True
            if pacman.next_direction != 'up':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.k)):
        if pygame.Rect.colliderect(pacman.rect, maze.k[l]):
            pacman.left_allowed = False
            pacman.right_allowed = True
            pacman.up_allowed = True
            pacman.down_allowed = True
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.ismoving_left:
                pacman.left_stopper = True
            if pacman.next_direction != 'left':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.l)):
        if pygame.Rect.colliderect(pacman.rect, maze.l[l]):
            pacman.left_allowed = True
            pacman.right_allowed = False
            pacman.up_allowed = True
            pacman.down_allowed = True
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.ismoving_right:
                pacman.right_stopper = True
            if pacman.next_direction != 'right':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.m)):
        if pygame.Rect.colliderect(pacman.rect, maze.m[l]):
            pacman.left_allowed = True
            pacman.right_allowed = True
            pacman.up_allowed = True
            pacman.down_allowed = True
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            pacman.direction = pacman.next_direction
