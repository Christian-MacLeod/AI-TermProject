import numpy as np
#import communication

#Dictionary of possible turn-end actions and their order of precedence (higher is better)
PRIORITY = {"hold":0, "move_up":5, "move_right":5, "move_down":5, "move_left":5, "evade_hold":6, "evade_up":7, "evade_down":7, "evade_left":7, "evade_right":7,
            "seek_up":4, "seek_down":3, "seek_left":2, "seek_right":1}


class Controller:
    selected_action = "hold"

    type = "undefined"
    memory = {}
    def __init__(self, faction, body):
        self.visited = np.full(((body.env.y_upper - body.env.y_lower), (body.env.x_upper - body.env.x_lower)), False)
        self.faction = faction
        self.body = body
        self.body.registerController(self)
        #self.private_channel = communication.PrivateChannel()


    def setAction(self, action_code):
        if PRIORITY[action_code] >= PRIORITY[self.selected_action]:
            self.selected_action = action_code

    def getType(self):
        return self.type

    def getFaction(self):
        return self.faction

    def getPosition(self):
        return self.body.x, self.body.y

    def executeAction(self):
        sa = self.selected_action
        action_result = False
        if sa == "hold" or sa == "evade_hold":
            action_result = True
        elif sa == "move_up" or sa == "evade_up" or sa == "seek_up":
            action_result = self.body.move("up")
        elif sa == "move_down" or sa == "evade_down" or sa == "seek_down":
            action_result = self.body.move("down")
        elif sa == "move_left" or sa == "evade_left" or sa == "seek_left":
            action_result = self.body.move("left")
        elif sa == "move_right" or sa == "evade_right" or sa == "seek_right":
            action_result = self.body.move("right")

        return action_result


        #Perform other actions

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

                #Ensure coordinates are within bounds
                x_bounded = self.body.env.x_lower <= x_test and x_test < self.body.env.x_upper
                y_bounded = self.body.env.y_lower <= y_test and y_test < self.body.env.y_upper

                # Mark visited if already visited, or if Euclidean distance less than/equal to 10
                if x_bounded and y_bounded:
                    if not self.visited[x_test][y_test]:
                        euclid_dist = np.sqrt((x_test-x)**2 + (y_test-y)**2)
                        self.visited[x_test][y_test] = euclid_dist <= 10

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
                self.setAction("seek_up")
            if self.perceiveBelow():
                self.setAction("seek_down")
            if self.perceiveLeft():
                self.setAction("seek_left")
            if self.perceiveRight():
                self.setAction("seek_right")

        else:
            #Found something

            #Check all radar hits
            for entity in visible:
                if entity.controller.getType() != "target":
                    #Other agent, Evade!
                    #TODO; Establish comms, decide where to go
                    #Temporarily just holding position;
                    self.setAction("evade_hold")
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
        #TODO: Change action if failed; Use priority stack on selected_action?

        return action_report



class TargetController(Controller):
    type = "target"
    collected = False

    def perceiveCollected(self):
        return self.collected

    def collect(self):
        self.collected = True
        return True
