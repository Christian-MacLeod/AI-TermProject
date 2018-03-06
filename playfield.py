import math
import numpy

class Field:
    agents = []
    targets = []
    time = 0
    #directions = ["up", "down", "left", "right"]
    def __init__(self, x_size, y_size, pm_enabled):
        self.dimensions = [x_size, y_size]
        self.pm_enabled = pm_enabled
        return


    def addAgent(self, newAgent):
        if self.inBounds(newAgent):
            self.agents.append(newAgent)
            return 1
        else:
            return -1


    def addTarget(self, newTarget):
        if self.inBounds(newTarget):
            self.targets.append(newTarget)
            return 1
        else:
            return -1


    def scan(self, scanningAgent): # Scan for all entities within scanning distance
        objectsInRange = []

        for agent in self.agents: # Check if any agents are within scanning distance
            if scanningAgent.pos != agent.pos and self.radar(scanningAgent.pos, agent.pos):
                objectsInRange.append(["agent", agent.targ_type, agent.pos])

        for target in self.targets: # Check if any targets are within scanning distance
            if self.radar(scanningAgent.pos, target.pos):
                if not target.found:
                    objectsInRange.append(["target", target.targ_type, target.pos])

        return objectsInRange


    def broadcast(self, sender, message):
        for agent in self.agents:
            if agent.targ_type != sender.targ_type:
                agent.receive(sender, message)
        return


    def privateMessage(self, sender, recipient, message):
        reply = -1
        if self.pm_enabled:
            for agent in self.agents:
                if agent.targ_type == recipient.targ_type:
                    reply = agent.receive(sender, message)
        return reply


    def collect(self, target_type, target_pos):
        for target in self.targets:
            if target.targ_type == target_type:
                if target.pos == target_pos:
                    target.found = True
                    return


    def inBounds(self, objPos):
        if (objPos[0] >= 0) and (objPos[1] >= 0) and (objPos[0] <= self.dimensions[0]) and (objPos[1] <= self.dimensions[1]):
            return True
        else:
            return False

    def toBounds(self, objPos):
        if objPos[0] <= 0: # Set x to bounds
            objPos[0] = 0
        elif objPos[0] >= self.dimensions[0]:
            objPos[0] = self.dimensions[0]

        if objPos[1] <= 0: #Set y to bounds
            objPos[1] = 0
        elif objPos[1] >= self.dimensions[1]:
            objPos[1] = self.dimensions[1]

        return objPos

    @staticmethod
    def radar(sourcePos, objPos):
        # NOTE: Considered visible if within a 20 diameter circle centered on the source

        x_diff = sourcePos[0] - objPos[0]
        y_diff = sourcePos[1] - objPos[1]

        return math.sqrt(x_diff * x_diff + y_diff * y_diff) <= 10

class Radar:
    @staticmethod
    def square(sourcePos, objPos):# Returns true if the objects are within scanning distance
        #NOTE: Considered visible if within a 20 x 20 square centered on the source
        visible = False
        if abs(sourcePos[0] - objPos[0]) >= 10:
            visible = True
        elif abs(sourcePos[1] - objPos[1]) >= 10:
            visible = True
        return visible

    @staticmethod
    def circle(sourcePos, objPos):# Returns true if the objects are within scanning distance
        #NOTE: Considered visible if within a 20 diameter circle centered on the source

        x_diff = sourcePos[0] - objPos[0]
        y_diff = sourcePos[1] - objPos[1]

        if math.sqrt(x_diff*x_diff + y_diff*y_diff) <= 10:
            return True
        else:
            return False


class FieldMap:
    def __init__(self, playfield):
        self.observed = numpy.full((playfield.bounds[0], playfield.bounds[1]), False)
        self.inBounds = playfield.inBounds
        self.revertToBounds = playfield.toBounds

    def visit(self, x, y):
        #do something

        self.observed[x][y] = True


    @staticmethod
    def circle(r):
