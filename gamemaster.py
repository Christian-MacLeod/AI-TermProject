import environment as Env
import body as Bod
import controller as Con
import random as Rnd
import userinterface as Ui
import threading
import numpy

class GameMaster(threading.Thread):
    def __init__(self, scenario, sem, iteration, logWriter):
        threading.Thread.__init__(self)
        self.game = None
        self.ui = Ui.Interface()
        self.scenario = scenario
        self.iteration = iteration
        self.sem = sem
        self.writeLog = logWriter

        if scenario == "competition":
            self.scenario = 1
        elif scenario == "collaboration":
            self.scenario = 2
        elif scenario == "compassion":
            self.scenario = 3


    def run(self):
        print("Iteration {0}: Beginning {1} type game!".format(self.iteration, self.scenario))
        self.beginGame(self.scenario)

    def beginGame(self, scenario):
        factions = {"red"}#, "blue", "yellow", "green", "purple"}

        #Create a game object, and start the loop
        if scenario == 1:
            self.game = Competition([99, 99], factions)
        elif scenario == 2:
            return
        elif scenario == 3:
            return
        else:
            return

        self.gameLoop()

    def finishGame(self):
        print("Iteration {0}: Finished {1} type game!".format(self.iteration, self.scenario))
        #Compile agent stats into required CSV lines
        lines = []
        for stat_sheet in self.game.agents:
            factions = ["red", "blue", "yellow", "green", "purple"]

            happiness = stat_sheet["happiness"]
            max_happiness = numpy.max(happiness)
            min_happiness = numpy.min(happiness)
            competitiveness = (happiness[-1]-min_happiness)/(max_happiness-min_happiness)

            line = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}".format(self.scenario, self.iteration, factions.index(stat_sheet["faction"]),
                                                                         stat_sheet["collected_targets"], stat_sheet["steps_taken"],
                                                                         happiness[-1], max_happiness,
                                                                         min_happiness, numpy.average(happiness),
                                                                         numpy.std(happiness), competitiveness)
            lines.append(line)

        #Write results to log file
        self.writeLog(lines)


        #Release the thread
        self.sem.release()

    def gameLoop(self):
        steps = 0
        while True:
            #Run each agent's turn
            game_won = self.game.playTurns()

            #TODO: Replace with proper interface system
            steps += 1
            if steps % 10 == 0 and self.iteration == 0:
                Ui.Interface.drawMaps(self.game.agents)
                #if input("Next 10 turns? (n)") == "n":
                #    break

            #Check for a win, leave the loop if satisfied
            if game_won:
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
            while len(faction_bodies) < 6:
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

            #Stop playing if the game is won
            if self.checkWin():
                return True
        return False


    def createAgent(self, faction, body):
        return None

    def checkWin(self):
        return None

#Create a game with competitive AI
class Competition(Game):

    def createAgent(self, faction, body):
        return Con.CompetitiveController(faction, body)

    def checkWin(self):
        for stat_sheet in self.agents:
            if stat_sheet["collected_targets"] == 5:
                return True
        return False
