import pygame
from pygame.sprite import Sprite
from sprite_sheet import SpriteSheet
# from timer import Timer


class Ghost(Sprite):
    def __init__(self, screen, color):
        super(Ghost, self).__init__()
        self.screen = screen

        # the number of the color will be 0 through 5
        # 0 = pink, 1 = red, 2 = orange, 3 = blue, 4 = white, 5 = blue
        self.color = color

        self.right = (4, self.color, 15, 15)
        self.right_in = (20, self.color, 15, 15)
        self.left = (35, self.color, 15, 15)
        self.left_in = (52, self.color, 15, 15)
        self.up = (68, self.color, 15, 15)
        self.up_in = (84, self.color, 15, 15)
        self.down = (100, self.color, 15, 15)
        self.down_in = (155, self.color, 15, 15)

        self.is_blue = False
        self.blue_last = 0
        self.blue_wait = 5000
        self.white_last = 0
        self.white_wait = 1000
        self.white = (163, 65, 15, 15)
        self.white_in = (180, 65, 15, 15)
        self.blue = (132, 65, 15, 15)
        self.blue_in = (148, 65, 15, 15)

        self.eye = False
        self.is_dead = False
        self.destroyed = False
        self.destroy_last = 0
        self.destroy_wait = 1000
        self.eye_right = (132, 81, 15, 15)
        self.eye_left = (148, 81, 15, 15)
        self.eye_up = (163, 81, 15, 15)
        self.eye_down = (180, 81, 15, 15)

        self.position = [self.up, self.up_in]
        self.location_x = 100
        self.location_y = 220
        self.screen = screen
        self.sprite_sheet = SpriteSheet('sprites/pacman.png')

        self.image = self.sprite_sheet.image_at(self.position[0], None)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = self.location_x
        self.rect.y = self.location_y

        self.ismoving = False
        self.ismoving_up = False
        self.ismoving_down = False
        self.ismoving_right = False
        self.ismoving_left = False

        self.wait_count = 0
        self.time = pygame.time.get_ticks()
        self.animation_counter = 0
        self.moving_speed = 4

        self.intro = False
        self.intro_blinky = False
        self.intro_pinky = False
        self.intro_inky = False
        self.intro_clyde = False
        self.title_blinky = False
        self.title_pinky = False
        self.title_inky = False
        self.title_clyde = False
        self.title_last = 0
        self.wait = 1000
        self.wait_count = 100
        self.last = 0

        self.next_route = True

    def update(self):
        self.moving_down()
        self.moving_up()
        self.moving_left()
        self.moving_right()
        self.moving()
        if self.is_dead:
            self.ismoving = False
            self.position = (19, 130, 15, 15)
            if self.screen.ghosts_destroyed == 1:
                self.position = (3, 130, 15, 15)
            if self.screen.ghosts_destroyed == 2:
                self.position = (19, 130, 15, 15)
            if self.screen.ghosts_destroyed == 3:
                self.position = (35, 130, 16, 15)
            if self.screen.ghosts_destroyed == 4:
                self.position = (50, 130, 17, 15)
            self.image = self.sprite_sheet.image_at(self.position, None)
            if self.screen.ghosts_destroyed == 3 and not self.destroyed:
                self.screen.ghosts_destroyed = 4
            if self.screen.ghosts_destroyed == 2 and not self.destroyed:
                self.screen.ghosts_destroyed = 3
            if self.screen.ghosts_destroyed == 1 and not self.destroyed:
                self.screen.ghosts_destroyed = 2
            if self.screen.ghosts_destroyed == 0 and not self.destroyed:
                self.screen.ghosts_destroyed = 1
            self.destroyed = True
            now = pygame.time.get_ticks()
            if self.destroy_last == 0:
                self.destroy_last = now
            if self.destroy_last + self.destroy_wait < now:
                self.position = self.eye_right
                self.image = self.sprite_sheet.image_at(self.position, None)
                self.image = pygame.transform.scale(self.image, (30, 30))
                self.ismoving = True
                self.is_dead = False
                self.eye = True

    def draw(self):
        self.screen.screen.blit(self.image, self.rect)

    def change_location(self, x_location, y_location):
        self.rect.x = x_location
        self.rect.y = y_location

    def change_type(self, position):
        self.position = position

    def moving_right(self):
        if self.ismoving_right and not self.screen.game_active:
            self.rect.x = self.rect.x + self.moving_speed

    def moving_left(self):
        if self.ismoving_left and not self.screen.game_active:
            self.rect.x = self.rect.x - self.moving_speed

    def moving_up(self):
        if self.ismoving_up and not self.screen.game_active:
            self.rect.y = self.rect.y - self.moving_speed

    def moving_down(self):
        if self.ismoving_down and not self.screen.game_active:
            self.rect.y = self.rect.y + self.moving_speed

    def moving(self):
        if self.ismoving:
            if self.ismoving_down:
                self.position = [self.down, self.down_in]
            if self.ismoving_up:
                self.position = [self.up, self.up_in]
            if self.ismoving_right:
                self.position = [self.right, self.right_in]
            if self.ismoving_left:
                self.position = [self.left, self.left_in]
            if self.is_blue:
                now = pygame.time.get_ticks()
                self.position = [self.blue, self.blue_in]
                if self.blue_last == 0:
                    self.blue_last = now
                if self.blue_last + self.blue_wait < now:
                    self.position = [self.blue, self.white_in]
                    now_two = pygame.time.get_ticks()
                    if self.white_last == 0:
                        self.white_last = now_two
                    if self.white_last + self.white_wait < now_two:
                        self.is_blue = False
                        self.screen.ghosts_destroyed = 0
            if self.eye and self.ismoving_left:
                self.position = [self.eye_left, self.eye_left]
            if self.eye and self.ismoving_right:
                self.position = [self.eye_right, self.eye_right]
            if self.eye and self.ismoving_up:
                self.position = [self.eye_up, self.eye_up]
            if self.eye and self.ismoving_down:
                self.position = [self.eye_down, self.eye_down]

            now = pygame.time.get_ticks()
            if self.last == 0:
                self.last = now
            if self.last + self.wait_count < now:
                self.position = self.position[self.animation_counter]
                self.image = self.sprite_sheet.image_at(self.position, None)
                self.image = pygame.transform.scale(self.image, (30, 30))
                self.animation_counter += 1
                self.wait_count += 250
                if self.animation_counter > 1:
                    self.animation_counter = 0

    def move(self, end):
        stop = False
        self.last = 0
        final_up = self.rect.centery - end
        final_down = self.rect.centery + end
        final_right = self.rect.centerx + end
        final_left = self.rect.centerx - end
        while not stop:
            if self.ismoving:
                if self.ismoving_down:
                    self.position = [self.down, self.down_in]
                if self.ismoving_up:
                    self.position = [self.up, self.up_in]
                if self.ismoving_right:
                    self.position = [self.right, self.right_in]
                if self.ismoving_left:
                    self.position = [self.left, self.left_in]
                if self.is_blue:
                    now = pygame.time.get_ticks()
                    self.position = [self.blue, self.blue_in]
                    if self.blue_last == 0:
                        self.blue_last = now
                    if self.blue_last + self.blue_wait < now:
                        self.position = [self.blue, self.white_in]
                        now_two = pygame.time.get_ticks()
                        if self.white_last == 0:
                            self.white_last = now_two
                        if self.white_last + self.white_wait < now_two:
                            self.is_blue = False
                            self.screen.ghosts_destroyed = 0
                if self.eye and self.ismoving_left:
                    self.position = [self.eye_left, self.eye_left]
                if self.eye and self.ismoving_right:
                    self.position = [self.eye_right, self.eye_right]
                if self.eye and self.ismoving_up:
                    self.position = [self.eye_up, self.eye_up]
                if self.eye and self.ismoving_down:
                    self.position = [self.eye_down, self.eye_down]

                now = pygame.time.get_ticks()
                if self.last == 0:
                    self.last = now
                if self.last + self.wait_count < now:
                    self.position = self.position[self.animation_counter]
                    self.image = self.sprite_sheet.image_at(self.position, None)
                    self.image = pygame.transform.scale(self.image, (30, 30))
                    self.animation_counter += 1
                    self.wait_count += 250
                    print(self.rect.centerx, final_right)
                    print(self.rect.centery, final_down)
                    print(self.ismoving_up)
                    print(self.ismoving_down)
                    print(self.ismoving_right)
                    print(self.ismoving_left)
                    if self.rect.centery > final_up and self.ismoving_up:
                        self.rect.centery -= 1
                        if self.rect.centery <= final_up:
                            stop = True

                    if self.rect.centery < final_down and self.ismoving_down:
                        self.rect.centery += 1
                        if self.rect.centery >= final_down:
                            stop = True
                    if self.rect.centerx < final_right and self.ismoving_right:
                        self.rect.centerx += 1
                        if self.rect.centerx >= final_right:
                            stop = True
                    if self.rect.centerx > final_left and self.ismoving_left:
                        self.rect.centerx -= 1
                        if self.rect.centery <= final_left:
                            stop = True
                    if self.animation_counter > 1:
                        self.animation_counter = 0

    def move_ghosts(self, dijkstra_route, dijkstra_graph):

        self.next_route = False
        print(dijkstra_route)
        for i in range(len(dijkstra_route)):
            current = dijkstra_route[i] # aA
            # print(current)
            next_destination = dijkstra_route[i+1]
            destinations = dijkstra_graph.get(dijkstra_route[i]) # dijkstra_route[i] this is aA
            # print(destinations) # aC, bA
            final_distance = destinations.get(next_destination) # dijkstra_route[i+1] this is bA
            # print(final_distance)
            done_moving = False
            if current[0] < next_destination[0] and current[1] == next_destination[1]:
                print('going down')
                # final_location = self.rect.y + final_distance
                self.ismoving = True
                self.ismoving_down = True
                self.ismoving_left = False
                self.ismoving_up = False
                self.ismoving_right = False
                self.move(final_distance)
                # while self.rect.y <= final_location:
                #     self.rect.centery += 1
                # if self.rect.y >= final_location:
                #     self.ismoving_down = False
                #     done_moving = True
            if current[0] > next_destination[0] and current[1] == next_destination[1]:
                print('going up')
                # final_location = self.rect.y - final_distance
                self.ismoving = True
                self.ismoving_down = False
                self.ismoving_left = False
                self.ismoving_up = True
                self.ismoving_right = False
                self.move(final_distance)
                # while self.rect.y >= final_location:
                #     self.rect.centery -= 1
                # if self.rect.y <= final_location:
                #     self.ismoving_up = False
                #     done_moving = True
            if current[1] < next_destination[1] and current[0] == next_destination[0]:
                print('going right')
                print(self.rect.x)
                print(final_distance)
                # final_location = self.rect.x + final_distance
                self.ismoving = True
                self.ismoving_down = False
                self.ismoving_left = False
                self.ismoving_up = False
                self.ismoving_right = True
                self.move(final_distance)
                # while self.rect.x <= final_location:
                #     self.rect.centerx += 1
                # if self.rect.x >= final_location:
                #     self.ismoving_right = False
                #     done_moving = True
            if current[1] > next_destination[1] and current[0] == next_destination[0]:
                print('going left')
                # final_location = self.rect.x - final_distance
                self.ismoving = True
                self.ismoving_down = False
                self.ismoving_left = True
                self.ismoving_up = False
                self.ismoving_right = False
                self.move(final_distance)
                # while self.rect.x >= final_location:
                #     self.rect.centery -= 1
                # if self.rect.x <= final_location:
                #     self.ismoving_left = False
                #     done_moving = True

        self.next_route = True
