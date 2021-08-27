import pygame
import conf
import math
import random
import os

from player import Player
from game_state import GameState
from units import Units


class Game:
    def __init__(self, screen):
        self.score = 0
        self.screen = screen
        self.objects = []
        self.objects_units = []
        self.game_state = GameState.NONE
        self.map = []
        self.camera = [0, 0]
        list = os.listdir(".\maps")
        number_files = len(list)
        self.map_name = random.randint(1, number_files)

    def set_up(self):
        player = Player(1, 1)
        self.spawn_danger(random.randint(1,20), random.randint(1,20))
        self.player = player
        self.objects.append(player)
        print("Set up")
        self.game_state = GameState.RUN
        list = os.listdir(".\maps")
        number_files = len(list)
        self.load_map(str(self.map_name))

    def update(self):
        self.render_map(self.screen)
        self.handle_events()

        for objects_units in self.objects_units:
            objects_units.render(self.screen, self.camera)

        for object in self.objects:
            object.render(self.screen, self.camera)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            # handle key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.RESTART
                elif event.key == pygame.K_UP and self.player.state == 0: # up
                    self.move_unit(self.player , [0, -1])
                elif event.key == pygame.K_DOWN and self.player.state == 0: # down
                    self.move_unit(self.player, [0, 1])
                elif event.key == pygame.K_LEFT and self.player.state == 0: # left
                    self.move_unit(self.player, [-1, 0])
                elif event.key == pygame.K_RIGHT and self.player.state == 0: # right
                    self.move_unit(self.player, [1, 0])

    def map_size(self, file_name):
        i = 0
        j = 0
        with open("maps/" + file_name + ".txt") as map_file:
            for line in map_file:
                i+=1
                for char in range(0, len(line) - 1, 2):
                    j+=1
        return i, round(j/i)

    def load_map(self, file_name):
        with open("maps/" + file_name + ".txt") as map_file:
            for line in map_file:
                tiles = []
                for i in range(0, len(line) - 1, 2):
                    tiles.append(line[i])
                self.map.append(tiles)
            print("Map Loaded")

    def render_map(self, screen):
        self.determine_camera()
        y_pos = 0
        for line in self.map:
            x_pos = 0
            for tile in line:
                img = map_tile_img[tile]
                rect = pygame.Rect(x_pos * conf.SCALE - (self.camera[0] * conf.SCALE), y_pos * conf.SCALE - (self.camera[1] * conf.SCALE), conf.SCALE, conf.SCALE)
                screen.blit(img, rect)
                x_pos = x_pos + 1
            y_pos = y_pos + 1

    def move_unit(self, unit, pos_change):
        new_position = [unit.position[0] + pos_change[0], unit.position[1] + pos_change[1]]
        if self.collision(new_position):
            return
        if new_position[0] < 0 or new_position[0] > (len(self.map[0])-1):
            return
        if new_position[1] < 0 or new_position[1] > (len(self.map)-1):
            return
        if self.map[new_position[1]][new_position[0]] == "W":
            return
        if self.map[new_position[1]][new_position[0]] == "A":
            Player.kill_player(self.player)
            return
        unit.update_position(new_position)

    def determine_camera(self):
        max_y_pos = len(self.map) - conf.SCREEN_H / conf.SCALE
        y_pos = self.player.position[1]-math.ceil(round(conf.SCREEN_H / conf.SCALE / 2))
        if y_pos <= max_y_pos and y_pos >= 0:
            self.camera[1] = y_pos
        elif y_pos < 0:
            self.camera[1] = 0
        else:
            self.camera[1] = max_y_pos

    def spawn_danger(self, mob, barrels):
        map_number = self.map_size(str(self.map_name))
        print(map_number)
        while mob > 0:
            units = Units(random.randint(0, map_number[0]), random.randint(0, map_number[1])
                          ,"img\Cat.png")
            self.objects_units.append(units)
            mob -= 1
        while barrels > 0:
            units = Units(random.randint(0, map_number[0]), random.randint(0, map_number[0])
                          , "img\Bar.png")
            self.objects_units.append(units)
            barrels -= 1
        return

    def collision(self, pos):
        i = len(self.objects_units)
        while i > 0:
            i -= 1
            if self.objects_units[i].position == pos:
                self.objects_units[i].kill
                if self.objects_units[i].type == "img\Cat.png" and self.objects_units[i].state == 0 :
                    self.score += 1
                    self.objects_units[i].kill()
                    print(self.score)
                elif self.objects_units[i].type == "img\Bar.png" :
                    Player.kill_player(self.player)
                print(self.objects_units[i].type)
                return True
        return False

map_tile_img = {
    "H": pygame.transform.scale(pygame.image.load("img\sol.png"),(conf.SCALE, conf.SCALE)),
    "W": pygame.transform.scale(pygame.image.load("img\water.png"),(conf.SCALE, conf.SCALE)),
    "A": pygame.transform.scale(pygame.image.load("img\Acide.png"), (conf.SCALE, conf.SCALE)),
}
