#################################################################
#   Filename:   Agent.py
#   Desc:       This file contains playing agent codes
#
#################################################################

class Agent():

    def __init__(self, player_name):
        self.score = 0
        self.player_name = player_name
        self.target = 0 #normal

    def ToogleTarget(self):
        if self.target == 0: self.target = 1;
        else: self.target = 0