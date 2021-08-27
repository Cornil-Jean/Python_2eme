import pygame
import conf

class Units:
    def __init__(self, x_position, y_position, type):
        self.position = [x_position, y_position]
        self.type = type
        self.img = pygame.image.load(type)
        self.img = pygame.transform.scale(self.img, (conf.SCALE, conf.SCALE))
        self.rect = pygame.Rect(self.position[0] * conf.SCALE, self.position[1] * conf.SCALE, conf.SCALE, conf.SCALE)
        self.state = conf.ALIVE

    def update(self):
        print("player updated")

    def render(self, screen, camera):
        self.rect = pygame.Rect(self.position[0] * conf.SCALE - (camera[0] * conf.SCALE),
                                self.position[1] * conf.SCALE - (camera[1] * conf.SCALE), conf.SCALE, conf.SCALE)
        screen.blit(self.img, self.rect)

    def kill(self):
        self.img = pygame.image.load(("img\DeadCat.png"))
        self.img = pygame.transform.scale(self.img, (conf.SCALE, conf.SCALE))
        self.rect = pygame.Rect(self.position[0] * conf.SCALE, self.position[1] * conf.SCALE, conf.SCALE, conf.SCALE)
        self.state = conf.DEAD