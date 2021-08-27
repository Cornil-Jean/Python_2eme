import pygame
import conf

class Player:
    def __init__(self, x_position, y_position):
        print("player created")
        self.position = [x_position, y_position]
        self.img = pygame.image.load(("img\player.png"))
        self.img = pygame.transform.scale(self.img, (conf.SCALE, conf.SCALE))
        self.rect = pygame.Rect(self.position[0] * conf.SCALE, self.position[1] * conf.SCALE, conf.SCALE, conf.SCALE)
        self.state = conf.ALIVE

    def update(self):
        print("player updated")

    def update_position(self, new_position):
        self.position[0] = new_position[0]
        self.position[1] = new_position[1]

    def render(self, screen, camera):
        self.rect = pygame.Rect(self.position[0] * conf.SCALE - (camera[0] * conf.SCALE), self.position[1] * conf.SCALE - (camera[1] * conf.SCALE), conf.SCALE, conf.SCALE)
        screen.blit(self.img, self.rect)

    def kill_player(self):
        self.img = pygame.image.load(("img\Dead.png"))
        self.img = pygame.transform.scale(self.img, (conf.SCALE, conf.SCALE))
        self.state = conf.DEAD