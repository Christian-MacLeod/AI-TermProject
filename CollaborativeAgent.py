import agent
import body
import random

class CollaborativeController():
    def __init__(self, targ_type, x_pos, y_pos, playfield):
        self.body = body.Body(targ_type, x_pos, y_pos, playfield)
        self.known_targets = []


