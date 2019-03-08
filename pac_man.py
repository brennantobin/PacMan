import pygame
import events
import dijkstra
from screen import Screen
from button import Button
from pygame.sprite import Group
from pacman import PacMan
from ghost import Ghost
from scoreboard import Scoreboard
from maze import Maze
from fruit import Fruit

screen = Screen()
pygame.display.set_caption("Pac Man")

play_button = Button(screen, 'play', 200)
score_button = Button(screen, 'high scores', 275)
back_button = Button(screen, "back", 300)
buttons = Group()

pacmen = Group()
ghosts = Group()
pacman = PacMan(screen, pacmen, ghosts)
pacman2 = PacMan(screen, pacmen, ghosts)

fruit = Group()

pacman.is_big = True
pacmen.add(pacman)

scoreboard = Scoreboard(screen, pacmen, ghosts)

maze = Maze(screen, mazefile='pacmanportalmaze.txt', brickfile='square', shieldfile='shield',
            dotfile='dot', powerpillfile='powerpill')
node_maze = Maze(screen, mazefile='nodes.txt', brickfile='square', shieldfile='shield',
                 dotfile='dot', powerpillfile='powerpill')
dijkstra_nodes = Maze(screen, mazefile='dijkstra.txt', brickfile='square', shieldfile='shield',
                      dotfile='dot', powerpillfile='powerpill')
dijkstra_nodes.dijkstra_fill()

dijkstra_index = ['aA', 'aC', 'aE', 'aG', 'aI', 'aK', 'bA', 'bC', 'bD', 'bE', 'bG', 'bH', 'bI',
                  'bK', 'cA', 'cC', 'cD', 'cE', 'cG', 'cH', 'cI', 'cK',
                  'dD', 'dE', 'dF', 'dG', 'dH', 'eE', 'eG', 'fA', 'fC', 'fD', 'fE', 'fG', 'fH', 'fI', 'fK',
                  'gE', 'gF', 'gG', 'hD', 'hH', 'iA', 'iC', 'iD', 'iE', 'iG', 'iH', 'iI', 'iK',
                  'jA', 'jB', 'jC', 'jD', 'jE', 'jF', 'jG', 'jH', 'jI', 'jJ', 'jK',
                  'kA', 'kB', 'kC', 'kD', 'kE', 'kG', 'kH', 'kI', 'kJ', 'kK', 'lA', 'lE', 'lG', 'lK']

# c_x = 0
# c_y = 0
# dijkstra_dic = {'aA': (c_x, c_y), 'aC': (c_x, c_y), 'aE': (c_x, c_y), 'aG': (c_x, c_y),
#                 'aI': (c_x, c_y), 'aK': (c_x, c_y), 'bA': (c_x, c_y), 'bC': (c_x, c_y),
#                 'bD': (c_x, c_y), 'bE': (c_x, c_y), 'bG': (c_x, c_y), 'bH': (c_x, c_y),
#                 'bI': (c_x, c_y), 'bK': (c_x, c_y), 'cA': (c_x, c_y), 'cC': (c_x, c_y),
#                 'cD': (c_x, c_y), 'cE': (c_x, c_y), 'cG': (c_x, c_y), 'cH': (c_x, c_y),
#                 'cI': (c_x, c_y), 'cK': (c_x, c_y), 'dD': (c_x, c_y), 'dE': (c_x, c_y),
#                 'dF': (c_x, c_y), 'dG': (c_x, c_y), 'dH': (c_x, c_y), 'eE': (c_x, c_y),
#                 'eG': (c_x, c_y), 'fA': (c_x, c_y), 'fC': (c_x, c_y), 'fD': (c_x, c_y),
#                 'fE': (c_x, c_y), 'fG': (c_x, c_y), 'fH': (c_x, c_y), 'fI': (c_x, c_y),
#                 'fK': (c_x, c_y), 'gE': (c_x, c_y), 'gF': (c_x, c_y), 'gG': (c_x, c_y),
#                 'hD': (c_x, c_y), 'hH': (c_x, c_y), 'iA': (c_x, c_y), 'iC': (c_x, c_y),
#                 'iD': (c_x, c_y), 'iE': (c_x, c_y), 'iG': (c_x, c_y), 'iH': (c_x, c_y),
#                 'iI': (c_x, c_y), 'iK': (c_x, c_y), 'jA': (c_x, c_y), 'jB': (c_x, c_y),
#                 'jC': (c_x, c_y), 'jD': (c_x, c_y), 'jE': (c_x, c_y), 'jF': (c_x, c_y),
#                 'jG': (c_x, c_y), 'jH': (c_x, c_y), 'jI': (c_x, c_y), 'jJ': (c_x, c_y),
#                 'jK': (c_x, c_y), 'kA': (c_x, c_y), 'kB': (c_x, c_y), 'kC': (c_x, c_y),
#                 'kD': (c_x, c_y), 'kE': (c_x, c_y), 'kG': (c_x, c_y), 'kH': (c_x, c_y),
#                 'kI': (c_x, c_y), 'kJ': (c_x, c_y), 'kK': (c_x, c_y), 'lA': (c_x, c_y),
#                 'lE': (c_x, c_y), 'lG': (c_x, c_y), 'lK': (c_x, c_y)}


def run_game():
    pygame.init()

    while True:

        if not screen.game_active and not screen.score_active:
            events.check_pacman_collision(pacmen, ghosts, fruit, scoreboard, maze, screen)
            screen.update(pacmen, ghosts)
            pacmen.update()
            ghosts.update()
            screen.start_screen(buttons, play_button, score_button, pacmen, ghosts)
            if len(pacmen) == 0:
                pacmen.add(pacman)
                screen.go_back = True
            for pacman_loop in pacmen:
                events.check_events(buttons, play_button, score_button, back_button, pacman_loop, pacmen,
                                    ghosts, screen, scoreboard)

            if len(pacmen) == 1 and not screen.go_back:
                for pacman1 in pacmen:
                    if pacman1.rect.x >= screen.rect.centerx-50:
                        pacman1.change_type(pacman1.big_mid)
                        pacmen.add(pacman2)
                        pacman2.ismoving = True
                        pacman2.change_location(0, 400)
                        pacman2.ismoving_right = True
                        ghost_counter = 65
                        for color in range(0, 4):
                            ghosts.add(Ghost(screen, ghost_counter + color))
                            ghost_counter += 15
                        counter = -50
                        for ghost in ghosts:
                            ghost.change_location(counter, 400)
                            counter -= 60
                            ghost.ismoving = True
                            ghost.ismoving_right = True
                        screen.screen_intro(pacman2, ghosts)
                        break

            if not screen.go_back:
                screen.screen_intro(pacman2, ghosts)

            for ghost in ghosts:

                if ghost.ismoving_left and ghost.rect.right + 25 < screen.rect.left:
                    ghost.intro = True
                    ghost.ismoving_left = False
                    ghost.ismoving = False
                if ghost.intro_blinky:
                    if screen.count == 0:
                        screen.count = 1
                if ghost.intro_pinky:
                    if screen.count == 1:
                        screen.count += 1
                if ghost.intro_inky:
                    if screen.count == 2:
                        screen.count += 1
                if ghost.intro and not ghost.intro_blinky:
                    screen.introduce_blinky(ghost)
                if ghost.intro and screen.count == 1:
                    screen.introduce_pinky(ghost)
                if ghost.intro and screen.count == 2:
                    screen.introduce_inky(ghost)
                if ghost.intro and screen.count == 3:
                    screen.introduce_clyde(ghost, ghosts)

        if screen.score_active:
            pacmen.empty()
            ghosts.empty()
            screen.score_screen(buttons, back_button)
            events.check_events(buttons, play_button, score_button, back_button, pacman2, pacmen,
                                ghosts, screen, scoreboard)
            screen.update(pacmen, ghosts)

        if screen.game_active:
            next_fruit = Fruit(screen, scoreboard.level-1)
            fruit.empty()
            fruit.add(next_fruit)
            if screen.reset_game:
                pacmen.empty()
                ghosts.empty()

                ghost_counter = 65
                location_counter = 0
                for color in range(0, 4):
                    ghosts.add(Ghost(screen, ghost_counter + color))
                    ghost_counter += 15
                for ghost in ghosts:
                    if location_counter == 0:
                        ghost.change_location(600, 315)
                    if location_counter == 1:
                        ghost.change_location(615, 400)
                    if location_counter == 2:
                        ghost.change_location(560, 390)
                    if location_counter == 3:
                        ghost.change_location(650, 390)
                    location_counter += 1
                pacman3 = PacMan(screen, pacmen, ghosts)
                pacman3.change_location(597, 585)
                pacmen.add(pacman3)
                screen.reset_game = False
            ghosts.update()
            pacmen.update()
            screen.game_screen(maze, node_maze, dijkstra_nodes, scoreboard, fruit)
            for pacman_loop in pacmen:
                events.check_events(buttons, play_button, score_button, back_button, pacman_loop, pacmen,
                                    ghosts, screen, scoreboard)
            screen.update(pacmen, ghosts)

            events.check_pacman_collision(pacmen, ghosts, fruit, scoreboard, maze, screen)
            for i in pacmen:
                events.hit_block(scoreboard, i, maze, ghosts, True, screen)
                events.hit_block(scoreboard, i, node_maze, ghosts, False, screen)
                # for c in ghosts:
                #     index = events.dijkstra_collisions(i, c, dijkstra_nodes)
                #     new_index = [(dijkstra_index[index[0]]), (dijkstra_index[index[1]])]
                #     dijkstra_route = dijkstra.dijkstra(new_index[1], new_index[0])
                #     c.move_ghosts(dijkstra_route, dijkstra_index)
                ghost1 = Ghost(screen, 4)
                for ghost in ghosts:
                    ghost1 = ghost
                    break
                # My nodes are off since it is putting the wrong start location into the dijkstra algorithm
                if ghost1.next_route:
                    index = events.dijkstra_collisions(i, ghost1, dijkstra_nodes)
                    if index[0] != -1 and index[1] != -1:
                        new_index = [(dijkstra_index[index[0]]), (dijkstra_index[index[1]])]
                        dijkstra_route = dijkstra.dijkstra(new_index[1], new_index[0])
                # I should try to only move the ghost after it has completed its route
                        # ghost1.move_ghosts(dijkstra_route, dijkstra.get_graph())


run_game()
