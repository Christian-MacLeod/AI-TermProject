import environment as env
import body as bod
import controller as con
import random as rnd

class GameMaster:
    def __init__(self):
        self.game = None
        return

    def beginGame(self, scenario):
        factions = {"red", "blue", "yellow", "green", "purple"}

        if scenario == "competition":
            self.game = Competition([100,100], factions)
            return
        elif scenario == "collaboration":
            return
        elif scenario == "compassion":
            return
        return None

    def drawGUI(self):
        return

    def compileResults(self):
        return

    def finishGame(self):
        return


class Game:

    def __init__(self, bounds, factions):
        #Create the environment
        self.field = env.Environment(bounds[0], 0, bounds[1], 0)
        self.targets = []
        self.agents = []
        self.turns = 0

        #Create factions
        for faction in factions:
            #With 6 bodies each
            faction_bodies = []
            while len(faction_bodies) <= 6:
                #Randomly generate a map coordinate, and create a body at that location
                x_coord = rnd.randrange(self.field.x_lower, self.field.x_upper)
                y_coord = rnd.randrange(self.field.y_lower, self.field.y_upper)
                body = bod.Body(self.field, x_coord, y_coord)
                #If the location is valid, add it to the list; otherwise re-roll
                if self.field.registerAgent(body):
                    faction_bodies.append(body)


            #Insert target controllers
            for i in range(1,len(faction_bodies)):
                self.targets.append(con.TargetController(faction,faction_bodies[i]))

            #Insert agent controller
            agent_stats = {"faction":faction, "controller":self.createAgent(faction, faction_bodies[0]),
                           "collected_targets":0, "steps_taken":0, "happiness":[]}
            self.agents.append(agent_stats)

        return


    def playTurns(self):
        for agent in self.agents: #For each agent, perform turn and evaluate performance
            turn_report = agent["controller"].playTurn()
            #If agent successfully performed something other than staying still, increment steps
            if turn_report["action_performed"] != "hold" and turn_report["action_performed"] != "evade_hold" and turn_report["action_result"] == True:
                agent["steps_taken"] += 1

                #Increment collected_targets if needed
                if turn_report["collected_target"]:
                    agent["collected_targets"] += 1

                #Recalculate happiness
                agent["happiness"].append(agent["collected_targets"]/(agent["steps_taken"]+1))
        return

    def createAgent(self, faction, body):
        return None

#Create a game with competitive AI
class Competition(Game):

    def createAgent(self, faction, body):
        return con.CompetitiveController(faction, body)
