import numpy as np
#import communication

#Dictionary of possible turn-end actions and their order of precedence (higher is better)
#PRIORITY = {"hold":0, "move_up":5, "move_right":5, "move_down":5, "move_left":5, "evade_hold":6, "evade_up":7, "evade_down":7, "evade_left":7, "evade_right":7,
#            "seek_up":4, "seek_down":3, "seek_left":2, "seek_right":1}


class Controller:
    action_classes = {"move":1, "evade":3, "seek":2, "hold":0}
    action_patterns = {"up":4, "right":3, "down":2, "left":1, "steady":0}

    selected_pattern = { "steady" }
    selected_action = "hold"

    type = "undefined"
    memory = {}
    def __init__(self, faction, body):
        self.body = body
        self.visited = [ [0 for y in range(0, self.body.env.y_upper - self.body.env.y_lower)] for x in range(0, self.body.env.x_upper - self.body.env.y_lower) ]
        self.faction = faction
        self.body.registerController(self)
        #self.private_channel = communication.PrivateChannel()


    def setAction(self, action_class, action_code):
        if self.action_classes[action_class] >= self.action_classes[self.selected_action] and self.selected_action != action_class:
            self.selected_action = action_class
            self.selected_pattern = {"steady", action_code}
        elif self.selected_action == action_class:
            self.selected_pattern.add(action_code)


    def getType(self):
        return self.type

    def getFaction(self):
        return self.faction

    def getPosition(self):
        return self.body.x, self.body.y

    def executeAction(self):
        #Do nothing if holding position
        if self.selected_action == "hold":
            return True
        else:
            #Repeat until successful action or empty action list
            while True:
                #Grab something from the list and add it back
                chosen = self.selected_pattern.pop()
                self.selected_pattern.add(chosen)

                #Choose the highest priority item still in the list
                for pattern in self.selected_pattern:
                    if self.action_patterns[pattern] >= self.action_patterns[chosen]:
                        chosen = pattern

                #Try to execute
                action_result = False
                if chosen == "steady":
                    return True
                else:
                    if chosen == "up":
                        action_result = self.body.move("up")
                    elif chosen == "down":
                        action_result = self.body.move("down")
                    elif chosen == "left":
                        action_result = self.body.move("left")
                    elif chosen == "right":
                        action_result = self.body.move("right")
                #Return if finished, else check if anything left to try
                if action_result:
                    return True
                else:
                    self.selected_pattern.remove(chosen)
                    if len(self.selected_pattern) == 0:
                        return False

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
                if not self.visited[x_observing][y_observing]:
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
                if not self.visited[x_observing][y_observing]:
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
                if not self.visited[x_observing][y_observing]:
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
                if not self.visited[x_observing][y_observing]:
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

                #Ensure coordinates are within bounds
                x_bounded = self.body.env.x_lower <= x_test and x_test < self.body.env.x_upper
                y_bounded = self.body.env.y_lower <= y_test and y_test < self.body.env.y_upper

                # Mark visited if already visited, or if Euclidean distance less than/equal to 10
                if x_bounded and y_bounded:
                    if not self.visited[x_test][y_test]:
                        euclid_dist = np.sqrt((x_test-x)**2 + (y_test-y)**2)
                        self.visited[x_test][y_test] = int (euclid_dist <= 10)

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

        return None


class CompetitiveController(Controller):
    type = "competitive_agent"

    def perceiveMessage(self, message):
        #Receive message!
        #NOTE: Called by other agents during their turn
        return None


    def runTurn(self):
        print("{0} agent running turn".format(self.faction))
        action_report = {"action_performed":"", "action_result":"", "collected_target":False}
        #Do the stuff!
        visible = self.perceiveRadar()
        if len(visible) == 0:
            #Nothing seen
            #Check in all directions, move towards highest priority direction with unobserved cells
            if self.perceiveAbove():
                self.setAction("seek","up")
            if self.perceiveBelow():
                self.setAction("seek","down")
            if self.perceiveLeft():
                self.setAction("seek","left")
            if self.perceiveRight():
                self.setAction("seek","right")

        else:
            #Found something

            #Check all radar hits
            for entity in visible:
                if entity.controller.getType() != "target":
                    #Other agent, Evade!
                    print("I've got you in my sights!")
                    #TODO; Establish comms, decide where to go
                    #Temporarily just holding position;
                    self.setAction("evade", "steady")
                else:
                    #Found a target
                    if entity.getFaction() == self.getFaction():
                        #Found my target!
                        if not entity.perceiveCollected():
                            entity.collect()
                            action_report["collected_target"] = True
                    else:
                        #Found someone else's target
                        entity_x, entity_y = entity.getPosition()
                        #Remember this for later
                        if entity.getFaction() in self.memory:
                            self.memory[entity.getFaction()].append([entity_x, entity_y])
                        else:
                            self.memory[entity.getFaction()] = [[entity_x, entity_y]]

        action_report["action_performed"] = self.selected_action
        action_report["action_result"] = self.executeAction()
        return action_report



class TargetController(Controller):
    type = "target"
    collected = False

    def perceiveCollected(self):
        return self.collected

    def collect(self):
        self.collected = True
        return True
