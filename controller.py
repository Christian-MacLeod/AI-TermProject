import numpy as np

class Controller:
    type = "undefined"
    def __init__(self, faction, body):
        self.visited = np.full((body.env.y_upper - body.env.y_lower), (body.env.x_upper - body.env.x_lower), False)
        self.faction = faction
        self.body = body

    def getType(self):
        return self.type

    def getFaction(self):
        return self.faction

    def getPosition(self):
        return self.body.x, self.body.y

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
        #TODO: Implement message receive in inherited controllers
        return None



class CollaborativeController(Controller):
    type = "collaborative_agent"


class TargetController(Controller):
    type = "target"
    collected = False

    def perceiveCollected(self):
        return self.collected

    def collect(self):
        self.collected = True
        return True
