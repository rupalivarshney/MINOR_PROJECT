#################################################################
#   Filename:   Board.py
#   Desc:       This file contains score board codes
#
#################################################################

import pygame

class ScoreBoard():
    pygame.font.init()

    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 24, True)
        self.board = pygame.Surface((900, 50)) # width, height

    def Show(self, player1, player2, whose_chance):
        self.board.fill((0, 0, 0)) # black
        player1_name = self.font.render(player1.player_name, 1, (255, 0, 0))
        player1_score = self.font.render(str(player1.score), 1, (255, 0, 0))

        score1_pos = (900 - 12 - 12*3)/2
        int_player1_score_pos = score1_pos - len(str(player1.score))
        int_player1_name_pos = ( 12 * 3 - 5)
        player1_turn = self.font.render(">", 1, (255, 0, 0))

        player2_name = self.font.render(player2.player_name, 1, (0, 255, 0))
        player2_score = self.font.render(str(player2.score), 1, (0, 255, 0))
        score2_pos = (900 - 12 + 12 * 3) / 2
        int_player2_score_pos = score2_pos - len(str(player2.score))
        int_player2_name_pos = (900 - 12 * 3 -5) - len(player2.player_name) * 12
        player2_turn = self.font.render("<", 1, (0, 255, 0))

        # drawing
        self.board.blit(player1_name, (int_player1_name_pos, 50/2))
        self.board.blit(player1_score, (int_player1_score_pos, 50 / 2))

        self.board.blit(player2_name, (int_player2_name_pos, 50 / 2))
        self.board.blit(player2_score, (int_player2_score_pos, 50 / 2))

        if whose_chance == player1:
            self.board.blit(player1_turn, (0, 50/2))
        else: self.board.blit(player2_turn, (900 - 12*3, 50/2))


