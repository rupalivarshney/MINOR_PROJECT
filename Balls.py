#################################################################
#   Filename:   Balls.py
#   Desc:       This file contains balls class
#
#################################################################
from  modules.Vector import *
import math


class Ball():
    RADIUS = 9
    POCKET_RADIUS = 15
    DELTA_TIME = 0.02
    SURFACE_FRICTION = 40
    BORDERS = {'left': 133, 'right': 966, 'down': 490, 'top': 83}
    def __init__(self, positions, **kwds):
        self.position =  Vector(positions)
        self.velocity = Vector(0, 0)
        self.coordinate = Vector(positions)
        self.isVisible = True
        self.isPotted = False

    def collision(self, initial, final):
        incoming = self.coordinate - initial
        pocket = final - initial

        projected = incoming.projection(pocket)
        distance = incoming.distance(projected)

        if 0 <= math.fabs(projected.x) <= math.fabs(final.x - initial.x) and 0 <= math.fabs(projected.y) <= math.fabs(final.y - initial.y) and distance < Ball.RADIUS:
            self.coordinate = Vector.normalize( incoming - projected) * Ball.RADIUS + initial + projected
            tmp = self.velocity.dot_product(pocket) / pocket.dot_product(pocket)

            tmp1 = pocket.mul_vec_scalar(tmp)

            tmp2 = tmp1 * self.velocity

            self.velocity = tmp2
            self.velocity = self.velocity.mul_vec_scalar(2)

    def move(self, pockets):
        nonzero_velocity = Vector(self.velocity)
        self.velocity -= self.velocity.normalize() * Ball.SURFACE_FRICTION * Ball.DELTA_TIME

        self.coordinate += self.velocity * Ball.DELTA_TIME

        if nonzero_velocity.x * self.velocity.x < 0 or nonzero_velocity.y * self.velocity.y < 0:
            self.velocity = Vector(0, 0)

        if int(self.coordinate.x) not in range(139, 534) and int(self.coordinate.x) not in range(564, 960) and int(self.coordinate.y) not in range(90, 484):
            # check for collision
            for p in pockets:
                self.collision(pockets[p][1], pockets[p][2])
                self.collision(pockets[p][3], pockets[p][4])

                if (self.coordinate - pockets[p][0]).length() <= Ball.POCKET_RADIUS:
                    self.isVisible = False
                    self.coordinate = Vector(1000, 1000) + self.position
                    self.velocity = Vector(0, 0)
                    self.isPotted = True
        else:
            if self.coordinate.x < Ball.BORDERS['left'] or self.coordinate.x > Ball.BORDERS['right']:
                if self.coordinate.x < Ball.BORDERS['left'] : self.coordinate.x = Ball.BORDERS['left']
                else: self.coordinate.x = Ball.BORDERS['right']

                self.velocity.x = -self.velocity.x

            elif self.coordinate.y < Ball.BORDERS['top'] or self.coordinate.y > Ball.BORDERS['down']:
                if self.coordinate.y < Ball.BORDERS['top'] : self.coordinate.y = Ball.BORDERS['top']
                else: self.coordinate.y = Ball.BORDERS['down']

                self.velocity.y = -self.velocity.y


class BallRed(Ball):

    def __init__(self, **kwds):
        self.color = (255, 50, 30)
        self.score = 1
        super().__init__(**kwds)

    def move(self, pot):
        super().move(pot)


class BallWhite(Ball):
    def __init__(self, **kwds):
        self.color = (245, 245, 245)
        self.hold = False
        self.score = 4
        super().__init__(**kwds)

    def move(self, pot):
        super().move(pot)


class BallColor(Ball):
    def __init__(self, color, score, **kwds):
        self.color = color
        self.score = score
        super().__init__(**kwds)

    def move(self, pot):
        super().move(pot)

