import pygame
import sys
from fire_portal import FirePortal
from orange_portal import OrangePortal
from blue_portal import BluePortal


def check_events(buttons, play_button, score_button, back_button, pacman, pacmen,
                 ghosts, screen, scoreboard, fire, sound):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            f_in = open('highscores.txt', 'r')
            score = int(f_in.read())
            if score < scoreboard.score:
                f = open('highscores.txt', 'w')
                f.write(str(scoreboard.score))
                f.close()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            check_key_down(event, pacman, screen, scoreboard, fire, sound)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            play_button.check_play_button(mouse_x, mouse_y, scoreboard)
        if event.type == pygame.MOUSEBUTTONDOWN and screen.score_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            back_button.check_back_button(mouse_x, mouse_y, buttons,
                                          play_button, score_button, pacman, pacmen, ghosts)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            score_button.check_score_button(mouse_x, mouse_y, buttons, back_button)


def check_key_down(event, pacman, screen, scoreboard, fire, sound):
    if screen.game_active:
        if event.key == pygame.K_RIGHT:
            pacman.next_direction = 'right'
        if event.key == pygame.K_LEFT:
            pacman.next_direction = 'left'
        if event.key == pygame.K_UP:
            pacman.next_direction = 'up'
        if event.key == pygame.K_DOWN:
            pacman.next_direction = 'down'
        if event.key == pygame.K_SPACE:
            pygame.init()
            if len(fire) == 0:
                bullet = FirePortal(screen, pacman)
                fire.add(bullet)
                sound.fire.play()
    if event.key == pygame.K_q:
        start = True
        f_in = open('highscores.txt', 'r')
        score = int(f_in.read())
        if score < scoreboard.score:
            f = open('highscores.txt', 'w')
            if start:
                f.write(str(scoreboard.score))
                start = False
            f.close()
        sys.exit()


def check_pacman_collision(pacmen, ghosts, fruit, scoreboard, maze, screen, sound, orange_portal, blue_portal):
    # collisions = pygame.sprite.groupcollide(orange_portal, pacmen, False, False)
    # for pacmen in collisions.values():
    #     for pacman in pacmen:
    #         for portal in blue_portal:
    #             pacman.change_location(portal.rect.x, portal.rect.y)

    collisions = pygame.sprite.groupcollide(blue_portal, pacmen, False, False)
    for pacmen in collisions.values():
        for pacman in pacmen:
            for portal in orange_portal:
                pacman.change_location(portal.rect.x, portal.rect.y)
                sound.transport.play()

    collisions = pygame.sprite.groupcollide(pacmen, fruit, False, True)
    for fruits in collisions.values():
        for fruit in fruits:
            if len(maze.dots) in range(25, 50) and not scoreboard.no_fruit:
                sound.eat_fruit()
                fruit.set_points()
                scoreboard.score += fruit.points
                screen.make_title(str(fruit.points), 20, (255, 255, 255), fruit.rect.x, fruit.rect.y)
                scoreboard.no_fruit = True
            if len(maze.dots) in range(100, 125) and not scoreboard.no_new_fruit:
                sound.eat_fruit()
                fruit.set_points()
                scoreboard.score += fruit.points
                screen.make_title(str(fruit.points), 20, (255, 255, 255), fruit.rect.x, fruit.rect.y)
                scoreboard.no_new_fruit = True

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
    else:
        for pacmen in collisions.values():
            for pacman in pacmen:
                pacman.destroy_pacman()
            for ghost in ghosts:
                ghost.ismoving = False
                ghost.ismoving_down = False
                ghost.ismoving_left = False
                ghost.ismoving_right = False
                ghost.ismoving_up = False
            scoreboard.life -= 1


def hit_block(scoreboard, pacman, maze, ghosts, change_score, screen, sound, fire, orange_portal,
              blue_portal):
    pygame.init()

    for i in range(len(maze.bricks)):
        for bullet in fire:
            if pygame.Rect.colliderect(maze.bricks[i], bullet.rect):
                fire.empty()
                rect = bullet.rect
                if len(orange_portal) == 1 and len(blue_portal) == 1:
                    blue_portal.empty()
                    orange_portal.empty()
                if len(orange_portal) == 0 and len(blue_portal) == 0:
                    if bullet.up:
                        rect.y += 10
                    if bullet.down:
                        rect.y -= 30
                    if bullet.left:
                        rect.x += 10
                    if bullet.right:
                        rect.x -= 30
                    orange = OrangePortal(screen, rect)
                    orange_portal.add(orange)
                    sound.open_portal.play()
                elif len(orange_portal) == 1 and len(blue_portal) == 0:
                    if bullet.up:
                        rect.y += 10
                    if bullet.down:
                        rect.y -= 30
                    if bullet.left:
                        rect.x += 10
                    if bullet.right:
                        rect.x -= 30
                    blue = BluePortal(screen, rect)
                    blue_portal.add(blue)
                    sound.open_portal.play()

    for i in range(len(maze.bricks)):
        for rect in maze.barriers:
            if pygame.Rect.colliderect(pacman.rect, maze.bricks[i]) or pygame.Rect.colliderect(pacman.rect, rect):
                # possible fix ---- now pacman can't hit the walls
                pacman.ismoving_right = False
                pacman.ismoving_left = False
                pacman.ismoving_up = False
                pacman.ismoving_down = False
                pacman.ismoving = False

    k = len(maze.dots)
    if change_score:
        if k == 0:
            scoreboard.level += 1
            for ghost in ghosts:
                ghost.speed += 1
                if ghost.speed >= 4:
                    ghost.speed = 4
            scoreboard.no_fruit = False
            scoreboard.no_new_fruit = False
            screen.reset_game = True
    for j in range(k):
        if pygame.Rect.colliderect(pacman.rect, maze.dots[j]):
            if not pygame.mixer.get_busy():
                sound.chomp()
            del(maze.dots[j])
            if change_score:
                scoreboard.score += scoreboard.dot_points
                scoreboard.prep_score()
                break
    for l in range(len(maze.powerpills)):
        if pygame.Rect.colliderect(pacman.rect, maze.powerpills[l]):
            del(maze.powerpills[l])
            for ghost in ghosts:
                ghost.is_blue = True
            break

    for l in range(len(maze.a)):
        if pygame.Rect.colliderect(pacman.rect, maze.a[l]):
            if not pacman.a:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.a[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.a[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.a[l]).center
                pacman.a = True
            pacman.b = False
            pacman.c = False
            pacman.d = False
            pacman.e = False
            pacman.f = False
            pacman.g = False
            pacman.h = False
            pacman.i = False
            pacman.j = False
            pacman.k = False
            pacman.l = False
            pacman.m = False
            pacman.left_allowed = True
            pacman.right_allowed = False
            pacman.up_allowed = False
            pacman.down_allowed = False
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            if pacman.ismoving_right:
                pacman.right_stopper = True
            if pacman.next_direction == 'left':
                pacman.direction = pacman.next_direction

    for l in range(len(maze.b)):
        if pygame.Rect.colliderect(pacman.rect, maze.b[l]):
            if not pacman.b:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.b[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.b[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.b[l]).center
                pacman.b = True
            pacman.a = False
            pacman.c = False
            pacman.d = False
            pacman.e = False
            pacman.f = False
            pacman.g = False
            pacman.h = False
            pacman.i = False
            pacman.j = False
            pacman.k = False
            pacman.l = False
            pacman.m = False
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
            if not pacman.c:
                pacman.rect.centerx = (maze.c[l]).centerx
                pacman.c = True
            pacman.a = False
            pacman.b = False
            pacman.d = False
            pacman.e = False
            pacman.f = False
            pacman.g = False
            pacman.h = False
            pacman.i = False
            pacman.j = False
            pacman.k = False
            pacman.l = False
            pacman.m = False
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
            if not pacman.d:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.d[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.d[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.d[l]).center
                pacman.d = True
            pacman.a = False
            pacman.b = False
            pacman.c = False
            pacman.e = False
            pacman.f = False
            pacman.g = False
            pacman.h = False
            pacman.i = False
            pacman.j = False
            pacman.k = False
            pacman.l = False
            pacman.m = False
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
            if not pacman.e:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.e[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.e[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.e[l]).center
                pacman.e = True
            pacman.a = False
            pacman.b = False
            pacman.c = False
            pacman.d = False
            pacman.f = False
            pacman.g = False
            pacman.h = False
            pacman.i = False
            pacman.j = False
            pacman.k = False
            pacman.l = False
            pacman.m = False
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
            if not pacman.f:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.f[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.f[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.f[l]).center
                pacman.f = True
            pacman.a = False
            pacman.b = False
            pacman.c = False
            pacman.d = False
            pacman.e = False
            pacman.g = False
            pacman.h = False
            pacman.i = False
            pacman.j = False
            pacman.k = False
            pacman.l = False
            pacman.m = False
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
            if not pacman.g:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.g[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.g[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.g[l]).center
                pacman.g = True
            pacman.a = False
            pacman.b = False
            pacman.c = False
            pacman.d = False
            pacman.e = False
            pacman.f = False
            pacman.h = False
            pacman.i = False
            pacman.j = False
            pacman.k = False
            pacman.l = False
            pacman.m = False
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
            if not pacman.h:
                pacman.rect.centery = (maze.h[l]).centery
                pacman.h = True
            pacman.a = False
            pacman.b = False
            pacman.c = False
            pacman.d = False
            pacman.e = False
            pacman.f = False
            pacman.g = False
            pacman.i = False
            pacman.j = False
            pacman.k = False
            pacman.l = False
            pacman.m = False
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
            if not pacman.i:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.i[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.i[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.i[l]).center
                pacman.i = True
            pacman.a = False
            pacman.b = False
            pacman.c = False
            pacman.d = False
            pacman.e = False
            pacman.f = False
            pacman.g = False
            pacman.h = False
            pacman.j = False
            pacman.k = False
            pacman.l = False
            pacman.m = False
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
            if not pacman.j:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.j[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.j[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.j[l]).center
                pacman.j = True
            pacman.a = False
            pacman.b = False
            pacman.c = False
            pacman.d = False
            pacman.e = False
            pacman.f = False
            pacman.g = False
            pacman.i = False
            pacman.h = False
            pacman.k = False
            pacman.l = False
            pacman.m = False
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
            if not pacman.k:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.k[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.k[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.k[l]).center
                pacman.k = True
            pacman.a = False
            pacman.b = False
            pacman.c = False
            pacman.d = False
            pacman.e = False
            pacman.f = False
            pacman.g = False
            pacman.i = False
            pacman.j = False
            pacman.h = False
            pacman.l = False
            pacman.m = False
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
            if not pacman.l:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.l[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.l[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.l[l]).center
                pacman.l = True
            pacman.a = False
            pacman.b = False
            pacman.c = False
            pacman.d = False
            pacman.e = False
            pacman.f = False
            pacman.g = False
            pacman.i = False
            pacman.j = False
            pacman.k = False
            pacman.h = False
            pacman.m = False
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
            if not pacman.m:
                if pacman.ismoving_right or pacman.ismoving_left:
                    pacman.rect.centery = (maze.m[l]).centery
                if pacman.ismoving_up or pacman.ismoving_down:
                    pacman.rect.centerx = (maze.m[l]).centerx
                if not pacman.ismoving:
                    pacman.rect.center = (maze.m[l]).center
                pacman.m = True
            pacman.a = False
            pacman.b = False
            pacman.c = False
            pacman.d = False
            pacman.e = False
            pacman.f = False
            pacman.g = False
            pacman.i = False
            pacman.j = False
            pacman.k = False
            pacman.l = False
            pacman.h = False
            pacman.left_allowed = True
            pacman.right_allowed = True
            pacman.up_allowed = True
            pacman.down_allowed = True
            pacman.right_stopper = False
            pacman.left_stopper = False
            pacman.up_stopper = False
            pacman.down_stopper = False
            pacman.direction = pacman.next_direction


def dijkstra_collisions(pacman, ghost, maze):
    pacman_index = -1
    ghost_index = -1
    for l in range(len(maze.dijkstra_nodes)):
        if pygame.Rect.colliderect(pacman.rect, maze.dijkstra_nodes[l]):
            pacman_index = maze.dijkstra_nodes.index(maze.dijkstra_nodes[l])

        # print(ghost.rect.y, maze.dijkstra_nodes[l].x)
        if pygame.Rect.colliderect(ghost.rect, maze.dijkstra_nodes[l]):
            # print('yes')
            ghost_index = maze.dijkstra_nodes.index(maze.dijkstra_nodes[l])
            ghost.rect.x = maze.dijkstra_nodes[l].centerx
            ghost.rect.y = maze.dijkstra_nodes[l].centery

    return [pacman_index, ghost_index]
