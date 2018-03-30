
class Body:
    controller = None
    #Create new body at given position
    def __init__(self, env, x, y):
        self.x = x
        self.y = y
        self.env = env

    def registerController(self, controller):
        self.controller = controller

    def getController(self):
        return self.controller

    #Move 1 unit in the given direction, if valid
    def move(self, direction):
        new_x = self.x
        new_y = self.y

        #Increment appropriate axis
        if direction == "up":
            new_y -= 1
            print("Trying to move up to ({0}, {1})".format(new_x, new_y))
        elif direction == "down":
            new_y += 1
            print("Trying to move down to ({0}, {1})".format(new_x, new_y))
        elif direction == "left":
            new_x -= 1
            print("Trying to move left to ({0}, {1})".format(new_x, new_y))
        elif direction == "right":
            new_x += 1
            print("Trying to move right to ({0}, {1})".format(new_x, new_y))

        #Set new position if valid
        if self.env.validPosition(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        else:
            print("Can't move!")
            return False

    #Ask the environment for a list of elements visible to the Agent
    def scan(self):
        return self.env.elementsAround(self.x, self.y)

