import playfield as Playfield
import target as Target
import agent as Agent
import CompetitiveAgent
import CollaborativeAgent
import random


LOGPATH = "C:/NavalSARGamelogs/"

class Scenario:

    @staticmethod
    def Competition():
        field = Playfield.Field(1000, 1000, False)
        rng = random.Random()

        for i in range(0,5): #Create 5 Competitive Agents, each with 5 targets
            #field.addAgent(CompetitiveAgent(i, rng.uniform(0,1000), rng.uniform(0,1000), field))
            for j in range(0,5):
                field.addTarget(Target.Target(i, rng.uniform(0,1000), rng.uniform(0,1000)))

        #Run the turns...
        while True:

            #Evaluate each agent
            #Check win conditions
            if False:
                break
            field.time += 1
            
        return

    @staticmethod
    def Collaboration():
        field = Playfield.Field(1000, 1000, True)
        return

    @staticmethod
    def Compassion():
        field = Playfield.Field(1000, 1000, True)
        return

class GameLog:
    def __init__(self):
        games = 0
        self.filepath = LOGPATH + "operationlog.txt"

    def write(self, data):
        with open(self.filepath, "a") as log:
            log.writelines(data)




