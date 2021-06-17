#################################################################
#   Filename:   Logic.py
#   Desc:       This file contains actual snooker game logic
#
#################################################################
import pygame
import math
from collections import deque

from modules import Debug
from modules.Vector import Vector
from modules.Balls import *
from modules.Agent import Agent
from modules.Board import ScoreBoard
from modules.Draw import Draw
from modules.Cue import Cue


class Logic():
    clock = pygame.time.Clock()
    pocket_coords = {
        'UPPER_RIGHT':[ Vector((120,70)), Vector(125, 94), Vector(113, 78), Vector(143, 75), Vector(128, 63)],
        'UPPER_LEFT': [Vector((120, 502)), Vector(125, 480), Vector(113, 495), Vector(143, 498), Vector(128, 510)],
        'DOWN_RIGHT': [Vector((980, 70)), Vector(956, 75), Vector(971, 63), Vector(974, 94), Vector(986, 79)],
        'DOWN_LEFT': [Vector((980, 502)), Vector(974, 480), Vector(986, 495), Vector(956, 498), Vector(971, 510)],
        'MIDDLE_RIGHT': [Vector((550, 64)), Vector(530, 75), Vector(539, 63), Vector(568, 75), Vector(560, 63)],
        'MIDDLE_LEFT': [Vector((550, 508)), Vector(530, 498), Vector(539, 510), Vector(568, 498), Vector(560, 510)],
    }

    def PickBall_White(self):
        mouse_coordinate = Vector(pygame.mouse.get_pos())

        if self.ball_White.coordinate.x - 8 < mouse_coordinate.x < self.ball_White.coordinate.x + 8 and self.ball_White.coordinate.y - 8 < mouse_coordinate.y < self.ball_White.coordinate.y + 8:
            for event in pygame.event.get():
                (button1, button2, button3) = pygame.mouse.get_pressed()
                if button1: self.ball_White.hold = True
                else: self.ball_White.hold = False

        if self.ball_White.hold: self.ball_White.coordinate = mouse_coordinate


    def ToogleTurn(self):
        if self.turn == self.player1:
            self.turn = self.player2
            self.cue.color = (27, 55, 0)
        else:
            self.turn = self.player1
            self.cue.color = (91, 35, 25)

        self.turn.target = 0 # red target

    def ReturnBall(self, potted_ball):
        potted_ball.isVisible = True

        return_position = Vector(potted_ball.position)
        color_position = [item.position for item in self.balls if isinstance(item, BallColor)]

        place_empty = False
        current_place = self.CheckPlace(potted_ball)

        if current_place is True:

            for position in color_position:
                place_empty = self.CheckPlace(potted_ball, position=position)

                if place_empty is not True:
                    place_empty = True
                    return_position = position
                    break

        if current_place is True and place_empty is not True:
            found = True
            while found is not True:
                flag = self.CheckPlace(potted_ball, position=return_position)
                if flag is not True: found = True; break;

                return_position.x += 1

            potted_ball.coordinate = return_position
        else: potted_ball.coordinate = return_position


    def __init__(self, app_title = "Snooker", table_path="./res/table.png", player1 = "Player 1 ", player2 = "Player 2  "):
        self.balls_in_motion = deque([])
        self.balls_hitted = deque([])


        pygame.display.set_caption(app_title)

        self.table = pygame.image.load(table_path)

        # color balls
        self.ball_White = BallWhite(positions=(820, 260))

        self.ball_Black = BallColor(positions=(202, 287), color=(25, 25, 25), score=7)
        self.ball_Pink = BallColor(positions=(337, 287), color=(214, 16, 123), score=6)
        self.ball_Blue = BallColor(positions=(550, 287), color=(0, 160, 214), score=5)
        self.ball_Brows = BallColor(positions=(799, 287), color=(125, 31, 31), score=4)
        self.ball_Green = BallColor(positions=(799, 358), color=(102, 205, 0), score=3)
        self.ball_Yellow= BallColor(positions=(799, 216), color=(229, 229, 0), score=2)

        self.ball_red_pos = [(320, 287),
                             (306, 279),
                             (306, 296),
                             (292, 271),
                             (292, 288),
                             (292, 305),
                             (278, 263),
                             (278, 280),
                             (278, 297),
                             (278, 314),
                             (264, 255),
                             (264, 272),
                             (264, 289),
                             (264, 306),
                             (264, 323)
                             ]

        self.ball_red = []
        for pos in self.ball_red_pos:
            self.ball_red.append( BallRed(positions=pos))

        self.player1 = Agent(player1)
        self.player2 = Agent(player2)

        self.balls = deque([
            self.ball_red[0],
            self.ball_red[1],
            self.ball_red[2],
            self.ball_red[3],
            self.ball_red[4],
            self.ball_red[5],
            self.ball_red[6],
            self.ball_red[7],
            self.ball_red[8],
            self.ball_red[9],
            self.ball_red[10],
            self.ball_red[11],
            self.ball_red[12],
            self.ball_red[13],
            self.ball_red[14],

            self.ball_White,
            self.ball_Black,
            self.ball_Pink,
            self.ball_Blue,
            self.ball_Brows,
            self.ball_Green,
            self.ball_Yellow
        ])

        self.cue = Cue()



        self.potted = []

        # init
        self.foul = False
        self.hit = False
        self.turn = self.player1
        self.status = True
        self.color_sequence = iter([i for i in range(2, 8)]) # according to ball points
        self.next_ball = next(self.color_sequence)

        self.condition = "red still"
        self.score = ScoreBoard()

        self.draw = Draw()


    def update(self):
        for i in range(0, len(self.balls)-1):

            for j in range( i+1 , len(self.balls)):

                ball, nextBall = self.balls[i], self.balls[j]
                delta = nextBall.coordinate - ball.coordinate

                if delta.length() <= Ball.RADIUS * 2:
                    # check for collision
                    if ball.velocity.length() > 0 and nextBall.velocity.length() > 0:

                        ball.coordinate += delta.normalize() * (delta.length() - Ball.RADIUS * 2)
                        nextBall.coordinate += Vector.normalize(-delta) * (delta.length() - Ball.RADIUS * 2)

                    elif ball.velocity.length() > 0 :
                        if isinstance(ball, BallWhite):
                            self.balls_hitted.append(nextBall)

                        ball.coordinate += Vector.normalize(delta) * (delta.length() - Ball.RADIUS * 2)
                        self.collision(ball, nextBall)

                    elif nextBall.velocity.length() > 0:
                        if isinstance(nextBall, BallWhite):
                            self.balls_hitted.append(ball)

                        nextBall.coordinate += Vector.normalize(-delta) * (delta.length() - Ball.RADIUS * 2)
                        self.collision(ball, nextBall)




    def isStaticBoard(self):
        for ball in self.balls:
            #if self.status == False and len(self.balls_in_motion) < 2: print(ball.velocity.length())

            if ball.velocity.length() > 0 and ball not in self.balls_in_motion:
                self.balls_in_motion.append(ball)

            elif ball in self.balls_in_motion and ball.velocity.length() < 1:
                self.balls_in_motion.remove(ball)

            elif ball in self.balls_in_motion and ball.velocity.length() > 2000:
                ball.velocity = Vector(0,0) # edge cases
                self.balls_in_motion.remove(ball)

        if not self.balls_in_motion: self.status = True
        else: self.status = False

        #print(self.status, len(self.balls_in_motion), "vel", self.ball_White.velocity.length(), end=', ')

    def checkcondition(self):
        flag = True
        for ball in self.balls:
            if isinstance(ball, BallRed): flag = False; break;

        if flag:
            if self.turn.target == 1: self.condition = 'still red'
            else: self.condition = 'red free'


    def CheckPlace(self, pottedBall, position = None):
        if position is None: position = pottedBall.position

        for ball in self.balls:
            if ball is not pottedBall:
                delta = ball.coordinate - position
                if delta.length() < Ball.RADIUS * 2: return True
        return False

    def handle_potted_ball(self, potted_balls, color_points = None):
        ball_red = 0; ball_color = 0; scores = 0;

        if color_points is None: color_points = [0]
        else: color_points = color_points

        for ball in potted_balls:

            if isinstance(ball, BallWhite):
                self.foul = True

            if isinstance(ball, BallColor):
                ball_color += 1
                color_points.append(ball.score)

                if self.turn.target != 1: self.foul = True

            if isinstance(ball, BallRed):
                if self.turn.target != 0: self.foul = True
                ball_red += 1
                scores += ball.score

            ball.velocity = Vector(0, 0)

            if isinstance(ball, BallRed):
                self.balls.remove(ball)
                ball.isPotted = False

            else:
                self.ReturnBall(ball)

            ball.isPotted = False

        self.potted = []

        if ball_color > 1 or ( ball_red > 0 and ball_color > 0): self.foul = True

        if self.foul is True:
            self.ToogleTurn()

            if max(color_points) > 4 : self.turn.score += max(color_points)
            else: self.turn.score += 4

        else:
            if self.turn.target == 0: # reg
                self.turn.score += scores
            else: self.turn.score == max(color_points)

            self.turn.ToogleTarget()




    def handle_red_game(self):
        scors = [0]

        if self.balls_hitted[0].score == self.next_ball:

            if self.potted:
                if len( self.potted ) > 1 :
                    Debug.Debug("Foul more than 1 color ball potted")
                    self.ToogleTurn()

                    for ball in self.potted:
                        scors.append(ball.score)
                        ball.isPotted = False

                    self.potted = []

                    if max( scors ) > 4: # foul point
                        self.turn.score += max(scors)

                    else:
                        self.turn.score += 4
                else:
                    if self.potted[0].score == self.next_ball:
                        self.turn.score += self.potted[0].score
                        self.balls.remove(self.potted[0])

                        try: self.next_ball = next(self.color_sequence)
                        except:
                            self.next_ball = False
                            Debug.Debug("Game Over")

                    else:
                        Debug.Debug("Foul wrong color ball potted")
                        self.ToogleTurn()

                        if self.potted[0].score > 4: #foul points
                            self.turn.scors += self.potted[0].score
                        else:
                            self.turn.score += 4

                        self.ReturnBall(self.potted[0])

                    self.potted[0].isPotted = False
                    self.potted.remove(self.potted[0])

            else:
                Debug.Debug("No color ball potted")
                self.ToogleTurn()

        else:
            Debug.Debug("Foul ! Wrong Color Ball Hitted")
            self.ToogleTurn()

            if self.potted:
                for ball in self.potted:
                    scors.append(ball.score)

                    self.ReturnBall(ball)
                    ball.isPotted = False

                self.potted = []

                scors.append(self.balls_hitted[0].score)

                if max(scors) > 4 : # fould point
                    self.turn.score += max (scors)
                else:
                    self.turn.score += 4

            else:
                if self.balls_hitted[0].score > 4 :
                    self.turn.score += self.balls_hitted[0].score
                else:
                    self.turn.score += 4






    def handle_cue(self):
        coord = self.ball_White.coordinate
        initial, final = self.cue.Position(coord)
        self.draw.Cue(self.cue, initial, final)

        keys = pygame.key.get_pressed()

        if keys[ pygame.K_SPACE]:
            vel = Vector.normalize(initial-final)

            force = Vector(self.ball_White.coordinate - initial).length()

            self.ball_White.velocity = vel * force **2 / 15

            self.hit = True


    def handle_ball(self):
        for ball in self.balls:

            if ball.velocity.length() > 0: ball.move(self.pocket_coords)

            if ball.isPotted and ball not in self.potted: self.potted.append(ball)

            if ball.isVisible: self.draw.Ball(ball);


    def handle(self):
        self.score.Show(self.player1, self.player2, self.turn)
        self.update() # ball
        self.isStaticBoard()
        self.checkcondition()
        #self.handle_cue()
        self.foul = False

        #if  self.ball_White.velocity.length() < 5: self.handle_cue();

        if self.status == True:
            if not self.balls_hitted and self.hit is True and not self.potted:
                self.ToogleTurn()
                self.turn.score += 4 # foul point

            self.hit = False
            self.handle_cue()

            if self.balls_hitted:

                if self.condition == 'still red':
                    if (isinstance(self.balls_hitted[0], BallColor) and self.turn.target != 1) or (isinstance(self.balls_hitted[0], BallRed) and self.turn.target != 0):

                        if not self.potted:
                            self.foul = True
                            self.ToogleTurn()

                            if self.balls_hitted[0].score > 4: # foul point
                                self.turn.score += self.balls_hitted[0].score
                            else: self.turn.score += 4 # foul point

                        else:
                            self.foul = True
                            points = [self.balls_hitted[0].score]

                            self.handle_potted_ball(self.potted, color_points = points)

                    if self.potted and self.foul is not True:
                        self.handle_potted_ball(self.potted)
                    elif self.foul is not True:
                        self.ToogleTurn()

                else:
                    self.handle_red_game()

                self.balls_hitted = deque([])

            if self.potted: self.handle_potted_ball(self.potted)

    def collision(self, ball, nextBall):
        delta = nextBall.coordinate - ball.coordinate
        unitDelta = Vector(delta/delta.length())
        unitTangent = Vector(unitDelta.perpendicular())

        vel1Normal = unitDelta.dot_product(ball.velocity)
        vel1Tangent = unitTangent.dot_product(ball.velocity)

        vel2Normal = unitDelta.dot_product(nextBall.velocity)
        vel2Tangent = unitTangent.dot_product(nextBall.velocity)

        newVel1Tangent = vel1Tangent
        newVel1Normal = vel2Normal

        newVel2Tangent = vel2Tangent
        newVel2Normal = vel1Normal

        newVel1Tangent = Vector(  unitTangent.mul_vec_scalar(newVel1Tangent))
        newVel1Normal = Vector( unitDelta.mul_vec_scalar(newVel1Normal))

        newVel2Tangent = Vector( unitTangent.mul_vec_scalar(newVel2Tangent))
        newVel2Normal = Vector( unitDelta.mul_vec_scalar(newVel2Normal))

        newVel1 = Vector(newVel1Normal + newVel1Tangent)
        newVel2 = Vector(newVel2Normal + newVel2Tangent)

        ball.velocity = newVel1
        nextBall.velocity = newVel2


