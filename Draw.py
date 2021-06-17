#################################################################
#   Filename:   Draw.py
#   Desc:       This file drawing methods
#
#################################################################
import pygame
from modules.Balls import Ball
class Draw():

    def __init__(self):
        self.surface = pygame.Surface((1200,600))

    def Ball(self, ball):
        pygame.draw.circle(self.surface,
                           ball.color,
                           (int(ball.coordinate.x), int(ball.coordinate.y)),
                            Ball.RADIUS)

    def Cue(self, cue, initial, final):
        pygame.draw.line(self.surface,
                         cue.color,
                         (int(initial.x),int(initial.y)),
                         (int(final.x),int(final.y)),
                         5)