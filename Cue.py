#################################################################
#   Filename:   Cue.py
#   Desc:       This file contains cue stick codes
#
#################################################################
import pygame
import math
from modules.Vector import Vector

class Cue():
    DELTA_ANGLE = 1;
    DELTA_POSITION = 1
    CUE_ANGLE = 180
    def __init__(self):
        self.width = 185
        self.color = (91, 35, 25)
        self.angle = 0
        self.r = Cue.CUE_ANGLE

    def Position(self, coordinate):
        initial = Vector(0, 0)
        final = Vector(0, 0)

        key_pressed = pygame.key.get_pressed()

        # direction keys
        if key_pressed[pygame.K_d]: self.angle -= Cue.DELTA_ANGLE #left
        if key_pressed[pygame.K_a]: self.angle += Cue.DELTA_ANGLE  # right

        if key_pressed[pygame.K_w]: self.r -= Cue.DELTA_POSITION;  # up
        if self.r < Cue.CUE_ANGLE: self.r = Cue.CUE_ANGLE

        if key_pressed[pygame.K_s]: self.r += Cue.DELTA_POSITION;  # down
        if self.r > Cue.CUE_ANGLE + Cue.CUE_ANGLE/1.5: self.r = Cue.CUE_ANGLE + Cue.CUE_ANGLE/1.5


        final.x = coordinate.x + math.cos(math.radians(self.angle)) * self.r
        final.y = coordinate.y + math.sin(math.radians(self.angle)) * self.r

        initial.x = coordinate.x + math.cos(math.radians(self.angle)) * (self.r - self.width)
        initial.y = coordinate.y + math.sin(math.radians(self.angle)) * (self.r - self.width)

        return (initial, final)



