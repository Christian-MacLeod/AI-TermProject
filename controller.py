import numpy as np
import communication

class Controller:
    type = "undefined"
    memory = {}
    def __init__(self, faction, body):
        self.visited = np.full((body.env.y_upper - body.env.y_lower), (body.env.x_upper - body.env.x_lower), False)
        self.faction = faction
        self.body = body
        self.private_channel = communication.PrivateChannel()

    def getType(self):
        return self.type

    def getFaction(self):
        return self.faction

    def getPosition(self):
        return self.body.x, self.body.y

    # Return True if unobserved cells above agent
    def perceiveAbove(self):
        return None

    # Return True if unobserved cells below agent
    def perceiveBelow(self):
        return None

    # Return True if unobserved cells left of agent
    def perceiveLeft(self):
        return None

    # Return True if unobserved cells right of agent
    def perceiveRight(self):
        return None

    #Get a list of all entities around the body
    def perceiveRadar(self):
        x, y = self.getPosition()

        #For every point in a 21x21 square
        for i in range(-10, 10):
            for j in range(-10, 10):
                #Shift coordinates from current position
                x_test = x + i
                y_test = y + j

                #Mark visited if already visited, or if Euclidean distance less than/equal to 10
                if not self.visited[x_test][y_test]:
                    self.visited[x_test][y_test] = np.sqrt((x_test-x)**2 + (y_test-y)**2) <=10

        #Get list of all elements around body
        return self.body.scan()

    def perceiveMessage(self, message):
        return None

    def runTurn(self):
        return None



class CollaborativeController(Controller):
    type = "collaborative_agent"

    def perceiveMessage(self, message):
        #Do the things, perceive the message
        return None

    def runTurn(self):
        #Do the stuff!
        visible = self.perceiveRadar()
        action_selected = ["nothing", 0] #Action code, action priority
        if len(visible) == 0:
            #Nothing seen
            return None
        else:
            #Found something, categorize and adjust behaviour
            return None







class CompetitiveController(Controller):
    type = "competitive_agent"

    def perceiveMessage(self, message):
        #Need to do something with this, gonna be global
        return None

    def runTurn(self):
        return None



class TargetController(Controller):
    type = "target"
    collected = False

    def perceiveCollected(self):
        return self.collected

    def collect(self):
        self.collected = True
        return True
