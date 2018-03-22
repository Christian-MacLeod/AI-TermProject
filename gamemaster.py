import environment as env
import body as bod
import controller as con
import random as rnd

class GameMaster:
    def __init__(self):
        self.game = None
        return

    def beginGame(self, scenario):
        if scenario == "competition":
            self.game = Competition([100,100])
            return
        elif scenario == "collaboration":
            return
        elif scenario == "compassion":
            return
        return None

    def drawGUI(self):
        return

    def compileResults(self):
        return None

    def finishGame(self):
        return None


class Game:

    def __init__(self, bounds):
        #Create the playfield
        self.field = env.Environment(bounds[0], 0, bounds[1], 0)

        #Create five factions
        for faction in {"red", "blue", "yellow", "green", "purple"}:
            #With 6 bodies each
            faction_bodies = []
            while len(faction_bodies) <= 6:
                #Randomly generate a map coordinate, and create a body at that location
                x_coord = rnd.randrange(self.field.x_lower, self.field.x_upper)
                y_coord = rnd.randrange(self.field.y_lower, self.field.y_upper)
                body = bod.Body(self.field, x_coord, y_coord)
                #If the location is valid, add it to the list, otherwise re-roll
                if self.field.registerAgent(body):
                    faction_bodies.append(body)
            #TODO: Create the faction brains & attach to bodies
        return


    def start(self):
        return

    def createAgent(self, faction, body):
        return None

#Create a game with competitive AI
class Competition(Game):

    def createAgent(self, faction, body):
        return con.CompetitiveController(faction, body)
