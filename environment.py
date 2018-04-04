import math
import numpy as np
class Environment:

    #Create new environment with the given bounds
    def __init__(self, x_upper, x_lower, y_upper, y_lower):
        self.x_upper = x_upper
        self.x_lower = x_lower
        self.y_upper = y_upper
        self.y_lower = y_lower

        self.agents = []

    #Registers an agent in the environment
    def registerAgent(self, agent):
        if self.validPosition(agent.x, agent.y):
            self.agents.append(agent)
            return True
        else:
            return False



    #Check if given position is unoccupied and within bounds
    def validPosition(self, x, y):
        for agent in self.agents: #Check unoccupied
            if agent.x == x and agent.y == y and (agent.controller is None or agent.controller.getType() != "target"):
                return False

        if self.x_upper >= x >= self.x_lower: #Check in bounds
            if self.y_upper >= y >= self.y_lower:
                return True
        return False

    #Get a list of elements visible from the given coordinates
    def elementsAround(self, x, y, faction = None):
        visible = []
        #Euclidean distance: distance^2 = xdiff^2 + ydiff^2
        for agent in self.agents:
            #If agent not at scan position AND Euclidean distance less than/equal to 10
            if math.floor(np.sqrt( (x-agent.x)**2 + (y-agent.y)**2 )) <= 10:
                if (agent.controller.getType() == "target" and not agent.controller.collected) or (faction is not None and faction != agent.controller.getFaction()) or (agent.x != x and agent.y != y and agent.controller.getType() != "target"):
                    visible.append(agent)

        return visible

