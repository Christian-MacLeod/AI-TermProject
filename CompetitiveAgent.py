import agent
import random


class CompetitiveAgent(agent.Agent):
    def __init__(self, targ_type, x_pos, y_pos, playfield):
        super().__init__(targ_type, x_pos, y_pos, playfield)
        self.openness = random.randrange(0,100)/100.0




