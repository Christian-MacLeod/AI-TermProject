import numpy as np
#import communication

class Controller:
    type = "undefined"
    memory = {}
    def __init__(self, faction, body):
        self.visited = np.full((body.env.y_upper - body.env.y_lower), (body.env.x_upper - body.env.x_lower), False)
        self.faction = faction
        self.body = body
        #self.private_channel = communication.PrivateChannel()

    def getType(self):
        return self.type

    def getFaction(self):
        return self.faction

    def getPosition(self):
        return self.body.x, self.body.y

    # Return True if unobserved cells above agent
    def perceiveAbove(self):
        #Get position
        x_pos, y_pos = self.getPosition()

        #Ensure x_low within environment boundary
        if (x_pos - 10) >= self.body.env.x_lower:
            x_low = x_pos - 10
        else:
            x_low = self.body.env.x_lower

        #Ensure x_high within environment boundary
        if (x_pos + 10) <= self.body.env.x_upper:
            x_high = x_pos + 10
        else:
            x_high = self.body.env.x_upper


        #Check upwards until unvisited element or boundary
        for y_observing in range(y_pos, self.body.env.y_upper):
            for x_observing in range(x_low, x_high):
                if not self.visited[x_observing, y_observing]:
                    return True
        return False

    # Return True if unobserved cells below agent
    def perceiveBelow(self):
        # Get position
        x_pos, y_pos = self.getPosition()

        # Ensure x_low within environment boundary
        if (x_pos - 10) >= self.body.env.x_lower:
            x_low = x_pos - 10
        else:
            x_low = self.body.env.x_lower

        # Ensure x_high within environment boundary
        if (x_pos + 10) <= self.body.env.x_upper:
            x_high = x_pos + 10
        else:
            x_high = self.body.env.x_upper

        # Check downwards until unvisited element or boundary
        for y_observing in range(y_pos, self.body.env.y_upper, -1):
            for x_observing in range(x_low, x_high):
                if not self.visited[x_observing, y_observing]:
                    return True
        return False

    # Return True if unobserved cells left of agent
    def perceiveLeft(self):
        #Get position
        x_pos, y_pos = self.getPosition()

        #Ensure y_low within environment boundary
        if (y_pos - 10) >= self.body.env.y_lower:
            y_low = y_pos - 10
        else:
            y_low = self.body.env.y_lower

        #Ensure y_high within element boundary
        if (y_pos + 10) <= self.body.env.y_upper:
            y_high = y_pos + 10
        else:
            y_high = self.body.env.y_upper

        #Check left until unvisited element or boundary
        for x_observing in range(x_pos, self.body.env.x_lower, -1):
            for y_observing in range(y_low, y_high):
                if not self.visited[x_observing, y_observing]:
                    return True
        return False

    # Return True if unobserved cells right of agent
    def perceiveRight(self):
        # Get position
        x_pos, y_pos = self.getPosition()

        # Ensure y_low within environment boundary
        if (y_pos - 10) >= self.body.env.y_lower:
            y_low = y_pos - 10
        else:
            y_low = self.body.env.y_lower

        # Ensure y_high within element boundary
        if (y_pos + 10) <= self.body.env.y_upper:
            y_high = y_pos + 10
        else:
            y_high = self.body.env.y_upper

        # Check right until unvisited element or boundary
        for x_observing in range(x_pos, self.body.env.x_lower):
            for y_observing in range(y_low, y_high):
                if not self.visited[x_observing, y_observing]:
                    return True
        return False

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
