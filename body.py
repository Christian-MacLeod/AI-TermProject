
class Body:
    #Create new body at given position
    def __init__(self, env, x, y):
        self.x = x
        self.y = y
        self.env = env

    #Move 1 unit in the given direction, if valid
    def move(self, direction):
        new_x = self.x
        new_y = self.y

        #Increment appropriate axis
        if direction == "up":
            new_y += 1
        elif direction == "down":
            new_y -= 1
        elif direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1

        #Set new position if valid
        if self.env.validPosition(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        else:
            return False

    #Ask the environment for a list of elements visible to the Agent
    def scan(self):
        return self.env.elementsAround(self.x, self.y)
