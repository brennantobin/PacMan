import pygame
import events
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

scoreboard = Scoreboard(screen)
# maze = Maze(screen, 1, 'pacmanportalmaze.txt', 'block_blue', 'shield', 'dot')
maze = Maze(screen, mazefile='pacmanportalmaze.txt', brickfile='square', shieldfile='shield',
            dotfile='dot', powerpillfile='powerpill')



def run_game():
    pygame.init()

    while True:

        if not screen.game_active and not screen.score_active:
            events.check_pacman_collision(pacmen, ghosts)
            screen.update(pacmen, ghosts)
            pacmen.update()
            ghosts.update()
            screen.start_screen(buttons, play_button, score_button, pacman, pacmen, ghosts)
            events.check_events(buttons, play_button, score_button, back_button, pacman2, pacmen,
                                ghosts, screen)

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
            events.check_events(buttons, play_button, score_button, back_button, pacman2, pacmen,
                                ghosts, screen)

        if screen.game_active:
            if screen.reset_game:
                pacmen.empty()
                ghosts.empty()

                ghost_counter = 65
                location_counter = 0
                for color in range(0, 4):
                    ghosts.add(Ghost(screen, ghost_counter + color))
                    ghost_counter += 15
                for ghost in ghosts:
                    ghost.change_location(540 + location_counter, 400)
                    location_counter += 30
                pacman3 = PacMan(screen, pacmen, ghosts)
                pacman3.change_location(590, 585)
                pacmen.add(pacman3)
                screen.reset_game = False
            ghosts.update()
            pacmen.update()
            screen.game_screen(maze)
            events.check_events(buttons, play_button, score_button, back_button, pacman2, pacmen,
                                ghosts, screen)
            screen.update(pacmen, ghosts)

            events.check_pacman_collision(pacmen, ghosts)
            for i in pacmen:
                events.hit_block(i, maze, ghosts)


run_game()
