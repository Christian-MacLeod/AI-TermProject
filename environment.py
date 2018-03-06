
class Environment:
    #Create new environment with the given bounds
    def __init__(self, x_upper, x_lower, y_upper, y_lower):
        self.x_upper = x_upper
        self.x_lower = x_lower
        self.y_upper = y_upper
        self.y_lower = y_lower

    #Check if given position is within bounds
    def validPosition(self, x, y):
        if self.x_upper >= x >= self.x_lower:
            if self.y_upper >= y >= self.y_lower:
                return True
        return False

