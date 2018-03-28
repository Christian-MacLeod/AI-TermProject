import environment as Env
import body as Bod
import controller as Con
import random as Rnd
import userinterface as Ui
import threading

class GameMaster(threading.Thread):
    def __init__(self, scenario, sem):
        threading.Thread.__init__(self)
        self.game = None
        self.ui = Ui.Interface()
        self.scenario = scenario
        self.sem = sem

    def run(self):
        self.beginGame(self.scenario)

    def beginGame(self, scenario):
        factions = {"red", "blue", "yellow", "green", "purple"}

        #Create a game object, and start the loop
        if scenario == "competition":
            self.game = Competition([99, 99], factions)
        elif scenario == "collaboration":
            return
        elif scenario == "compassion":
            return
        else:
            return

        self.gameLoop()

    def finishGame(self):
        pass

    def gameLoop(self):
        steps = 0
        while True:
            #Do until done
            self.game.playTurns()

            steps += 1
            #Check if won
            if steps % 10 == 0:
                Ui.Interface.drawMaps(self.game.agents)
                if input("Next 10 turns? (n)") == "n":
                    break


        self.finishGame()


class Game:

    def __init__(self, bounds, factions):
        #Create the environment
        self.field = Env.Environment(bounds[0], 0, bounds[1], 0)
        self.targets = []
        self.agents = []

        #Create factions
        for faction in factions:
            #With 6 bodies each
            faction_bodies = []
            while len(faction_bodies) <= 6:
                #Randomly generate a map coordinate, and create a body at that location
                x_coord = Rnd.randrange(self.field.x_lower, self.field.x_upper)
                y_coord = Rnd.randrange(self.field.y_lower, self.field.y_upper)
                body = Bod.Body(self.field, x_coord, y_coord)
                #If the location is valid, add it to the list; otherwise re-roll
                if self.field.registerAgent(body):
                    faction_bodies.append(body)


            #Insert target controllers
            for i in range(1,len(faction_bodies)):
                self.targets.append(Con.TargetController(faction, faction_bodies[i]))

            #Insert agent controller
            agent_stats = {"faction":faction, "controller":self.createAgent(faction, faction_bodies[0]),
                           "collected_targets":0, "steps_taken":0, "happiness":[]}
            self.agents.append(agent_stats)
        return


    def playTurns(self):
        for agent in self.agents: #For each agent, perform turn and evaluate performance
            turn_report = agent["controller"].runTurn()
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
        return Con.CompetitiveController(faction, body)
