import agent
import body
import random

class CollaborativeController:
    def __init__(self, faction):
        self.faction = faction
        return

    @staticmethod
    def getType():
        return "collaborative_agent"

    def getFaction(self):
        return self.faction


class TargetController:
    #Create a target controller belonging to given faction
    def __init__(self, faction):
        self.faction = faction

    #Returns AI type
    @staticmethod
    def getType():
        return "target"

    #Returns AI faction
    def getFaction(self):
        return self.faction