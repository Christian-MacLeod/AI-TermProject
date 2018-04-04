import environment as Env
import body as Bod
import controller as Con
import random as Rnd
import userinterface as Ui
import communication as Comm
import threading
import numpy

class GameMaster(threading.Thread):
    factions = ["red", "blue", "yellow", "green", "orange"]
    def __init__(self, scenario, sem, iteration, logWriter):
        threading.Thread.__init__(self)
        self.game = None
        self.ui = None
        self.releaseUI = None
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


    def registerUI(self, ui, releaseUI):
        self.ui = ui
        self.releaseUI = releaseUI

    def run(self):

        self.beginGame(self.scenario)

    def beginGame(self, scenario):
        print("Iteration {0}: Beginning {1} type game!".format(self.iteration, self.scenario))


        #Create a game object, and start the loop
        if scenario == 1:
            self.game = Competition([99, 99], self.factions)
        elif scenario == 2:
            self.game = Collaboration([99, 99], self.factions)
        elif scenario == 3:
            self.release()
            return
        else:
            self.release()
            return
        if self.ui is not None:
            self.ui.registerGame(self.game, "Iteration {0}, Game Type {1}".format(self.iteration, self.scenario))
        self.gameLoop()

    def finishGame(self):
        print("Iteration {0}: Finished {1} type game!".format(self.iteration, self.scenario))
        #Compile agent stats into required CSV lines
        lines = []
        for stat_sheet in self.game.agents:
            happiness = stat_sheet["happiness"]
            max_happiness = numpy.max(happiness)
            min_happiness = numpy.min(happiness)
            if max_happiness-min_happiness != 0:
                competitiveness = (happiness[-1]-min_happiness)/(max_happiness-min_happiness)
            else:
                competitiveness = 0

            line = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n".format(self.scenario, self.iteration, self.factions.index(stat_sheet["faction"]),
                                                                         stat_sheet["collected_targets"], stat_sheet["steps_taken"],
                                                                         happiness[-1], max_happiness,
                                                                         min_happiness, numpy.average(happiness),
                                                                         numpy.std(happiness), competitiveness)
            lines.append(line)

        #Write results to log file
        self.writeLog(lines)

        self.release()


    def release(self):
        # Release the thread
        if self.releaseUI is not None:
            self.releaseUI()
        self.sem.release()

    def gameLoop(self):
        while True:
            #Run each agent's turn
            game_won = self.game.playTurns()

            #Draw to display if allowed
            if self.ui is not None:
                try:
                    self.ui.updateDisplay()
                except RuntimeError:
                    pass

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
        self.private_links = {}
        self.broadcast_channel = Comm.PublicLink()
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
                self.targets.append(Con.TargetController(faction, faction_bodies[i], None))

            #Insert agent controller
            agent_stats = {"faction":faction, "controller":self.createAgent(faction, faction_bodies[0], self.broadcast_channel.send),
                           "collected_targets":0, "steps_taken":0, "happiness":[]}
            self.private_links[faction] = Comm.PrivateLink(agent_stats["controller"].perceiveMessage, faction)
            self.broadcast_channel.registerChannel(self.private_links[faction])
            self.agents.append(agent_stats)
        return


    def playTurns(self):
        for agent in self.agents: #For each agent, perform turn and evaluate performance
            turn_report = agent["controller"].runTurn()
            #If agent successfully performed something other than staying still, increment steps
            if turn_report["action_result"]:
                agent["steps_taken"] += 1

            #Increment collected_targets if needed
            agent["collected_targets"] += turn_report["collected_target"]

            #Recalculate happiness
            agent["happiness"].append(agent["collected_targets"]/(agent["steps_taken"]+1))

            #Stop playing if the game is won
            if self.checkWin():
                return True
        return False


    def createAgent(self, faction, body, public_comms):
        return None

    def checkWin(self):
        return None

#Create a game with competitive AI
class Competition(Game):

    def createAgent(self, faction, body, public_comms):
        return Con.CompetitiveController(faction, body, public_comms)

    def checkWin(self):
        for stat_sheet in self.agents:
            if stat_sheet["collected_targets"] == 5:
                print("{0} agent won!".format(stat_sheet["controller"].getFaction()))
                return True
        return False

#Create a game with collaborative AI
class Collaboration(Game):

    def createAgent(self, faction, body, public_comms):
        return Con.CollaborativeController(faction, body, public_comms)

    def checkWin(self):
        for stat_sheet in self.agents:
            if stat_sheet["collected_targets"] != 5:
                return False
        print("All targets found!")
        return True