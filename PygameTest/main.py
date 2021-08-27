import pygame
import conf

from game import Game
from game_state import GameState

def start():

    pygame.init()

    screen = pygame.display.set_mode((conf.SCREEN_W, conf.SCREEN_H))

    pygame.display.set_caption("Jeu Python test")

    clock = pygame.time.Clock()
    game = Game(screen)
    game.set_up()

    while game.game_state == GameState.RUN:
        # frame rate
        clock.tick(30)
        game.update()
        pygame.display.flip()
        if game.game_state == GameState.RESTART:
            start()
    print("Score: ", game.score)
    bestsc = open("highscore.txt", "w+")
    best = bestsc.read()
    if best == '':
        bestsc.write('0')
        best = '0'
    if game.score > int(best):
        bestsc.write(str(game.score))
    print("Record =", best)
start()

