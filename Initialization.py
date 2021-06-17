#################################################################
#   Filename:   Initialization.py
#   Desc:       This file contains codes that initialize ans setup
#                pygame game screen.
#
#################################################################
import time
import pygame
from modules.Logic import Logic
from modules.Debug import Debug
def initialization():
    pygame.init()
    game = Logic()
    screen = pygame.display.set_mode((1200,600))
    game_running = True

    while game_running:
        game.PickBall_White()

        for event in pygame.event.get():
            #Debug(pygame.event.get(), 'initialization')

            if event.type == pygame.QUIT: game_running = False
            if pygame.key.get_pressed()[pygame.K_ESCAPE]: game_running = False

        # rendring
        game.draw.surface.fill((0, 0, 0)) #black
        game.draw.surface.blit(game.table, (100, 50)) # tabel drawing coordinates
        game.draw.surface.blit(game.score.board, ((550 - 900/2), 530)) # score board coordinates

        game.handle()
        game.handle_ball()

        screen.blit(game.draw.surface, (0, 0)) # surface coordinates
        pygame.display.flip()
        Logic.clock.tick(50)

    pygame.quit()
