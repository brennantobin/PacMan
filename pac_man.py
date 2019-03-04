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

dijkstra_index = ['aA', 'aC', 'aE', 'aG', 'aI', 'aK', 'bA', 'bC', 'bD',
                  'bE', 'bG', 'bH', 'bI', 'bK', 'cA', 'cC', 'cD', 'cE', 'cG', 'cH',
                  'cI', 'cK', 'dD', 'dE', 'dF', 'dG', 'dH', 'eE', 'eG', 'fA', 'fC',
                  'fD', 'fE', 'fG', 'fH', 'fI', 'fK', 'gE', 'gF', 'gG', 'hD', 'hH',
                  'iA', 'iC', 'iD', 'iE', 'iG', 'iH', 'iI', 'iK', 'jA', 'jB', 'jC', 'jD', 'jE', 'jF',
                  'jG', 'jH', 'jI', 'jJ', 'jK', 'kA', 'kB', 'kC', 'kD', 'kE', 'kG',
                  'kH', 'kI', 'kJ', 'kK', 'lA', 'lE', 'lG', 'lK']


def run_game():
    pygame.init()

    while True:

        if not screen.game_active and not screen.score_active:
            events.check_pacman_collision(pacmen, ghosts)
            screen.update(pacmen, ghosts)
            pacmen.update()
            ghosts.update()
            screen.start_screen(buttons, play_button, score_button, pacman, pacmen, ghosts)
            events.check_events(buttons, play_button, score_button, back_button, pacmen,
                                ghosts, screen, scoreboard)

            if len(pacmen) == 1:
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
            screen.update(pacmen, ghosts)
            screen.score_screen(buttons, back_button)
            events.check_events(buttons, play_button, score_button, back_button, pacmen,
                                ghosts, screen, scoreboard)

        if screen.game_active:
            for ghost in ghosts:
                print(ghost.is_dead)
            if screen.reset_game:
                pacmen.empty()
                ghosts.empty()

                ghost_counter = 65
                location_counter = 0
                for color in range(0, 4):
                    ghosts.add(Ghost(screen, ghost_counter + color))
                    ghost_counter += 15
                for ghost in ghosts:
                    ghost.change_location(560 + location_counter, 390)
                    location_counter += 30
                pacman3 = PacMan(screen, pacmen, ghosts)
                pacman3.change_location(597, 585)
                pacmen.add(pacman3)
                screen.reset_game = False
            ghosts.update()
            pacmen.update()
            screen.game_screen(maze, node_maze, dijkstra_nodes, scoreboard)
            events.check_events(buttons, play_button, score_button, back_button, pacmen,
                                ghosts, screen, scoreboard)
            screen.update(pacmen, ghosts)

            events.check_pacman_collision(pacmen, ghosts)
            for i in pacmen:
                events.hit_block(scoreboard, i, maze, ghosts, True, screen)
                events.hit_block(scoreboard, i, node_maze, ghosts, False, screen)
                for c in ghosts:

                    index = events.dijkstra_collisions(i, c, dijkstra_nodes)
                    new_index = [(dijkstra_index[index[0]]), (dijkstra_index[index[1]])]
                    dijkstra_route = dijkstra.dijkstra(new_index[1], new_index[0])
                    if len(dijkstra_route) <= 1:
                        break
                    curr_node = dijkstra_nodes.dijkstra_nodes[dijkstra_index.index(dijkstra_route[0])]
                    next_node = dijkstra_nodes.dijkstra_nodes[dijkstra_index.index(dijkstra_route[1])]
                    if (next_node.y-curr_node.y) < (next_node.x-curr_node.x):
                        if next_node.x < curr_node.x:
                            c.ismoving_right = True
                            c.ismoving = True
                            c.ismoving_up = False
                            c.ismoving_left = False
                            c.ismoving_down = False
                    if (next_node.y - curr_node.y) < (next_node.x - curr_node.x):
                        if next_node.x > curr_node.x:
                            c.ismoving_left = True
                            c.ismoving = True
                            c.ismoving_up = False
                            c.ismoving_down = False
                            c.ismoving_right = False

                    if (next_node.y - curr_node.y) > (next_node.x - curr_node.x):
                        if next_node.y > curr_node.y:
                            c.ismoving_up = True
                            c.ismoving = True
                            c.ismoving_down = False
                            c.ismoving_left = False
                            c.ismoving_right = False
                        if next_node.y > curr_node.y:
                            c.ismoving_down = True
                            c.ismoving = True
                            c.ismoving_right = False
                            c.ismoving_up = False
                            c.ismoving_left = False


run_game()
