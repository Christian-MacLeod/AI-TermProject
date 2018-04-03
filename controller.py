import numpy as np
#import communication
import random
from math import floor


class Controller:
    action_classes = {"move":1, "evade":3, "seek":2, "hold":0}
    action_patterns = {"up":4, "right":3, "down":2, "left":1, "steady":0}



    type = "undefined"

    def __init__(self, faction, body, broadcast_link):
        self.memory = {"agent_reliability": {"red": 0.0, "blue": 0.0, "yellow": 0.0, "green": 0.0, "purple": 0.0},
                       "known_targets": {"red": [], "blue": [], "yellow": [], "green": [], "purple": []},
                       "waypoint": (0, 0), "targets_found": 0
                       }
        self.body = body
        self.visited = [ [0 for y in range(0, self.body.env.y_upper - self.body.env.y_lower + 1)] for x in range(0, self.body.env.x_upper - self.body.env.x_lower + 1) ]
        self.faction = faction
        self.body.registerController(self)
        self.memory["waypoint"] = self.getPosition()
        self.broadcast_link = broadcast_link
        self.selected_pattern = {"steady"}
        self.selected_action = "hold"


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

    def clearAction(self):
        self.selected_pattern = {"steady"}
        self.selected_action = "hold"

    def executeAction(self):
        #Do nothing if holding position
        if self.selected_action == "hold":
            self.clearAction()
            return True
        else:
            #Repeat until successful action or empty action list
            while True:
                #Grab something from the list and add it back
                print(self.selected_pattern)
                chosen = self.selected_pattern.pop()
                self.selected_pattern.add(chosen)

                #Choose the highest priority item still in the list
                for pattern in self.selected_pattern:
                    if self.action_patterns[pattern] >= self.action_patterns[chosen]:
                        chosen = pattern

                #Try to execute
                action_result = False
                if chosen == "steady":
                    self.clearAction()
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
                    self.clearAction()
                    return True
                else:
                    self.selected_pattern.remove(chosen)
                    if len(self.selected_pattern) == 0:
                        self.clearAction()
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
        for y_observing in range(y_pos, self.body.env.y_lower, -1):
            for x_observing in range(x_low, x_high):
                if self.visited[x_observing][y_observing] == 0:
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
        for y_observing in range(y_pos, self.body.env.y_upper):
            for x_observing in range(x_low, x_high):
                if self.visited[x_observing][y_observing] == 0:
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
                if self.visited[x_observing][y_observing] == 0:
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
        for x_observing in range(x_pos, self.body.env.x_upper):
            for y_observing in range(y_low, y_high):
                if self.visited[x_observing][y_observing] == 0:
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
                x_bounded = self.body.env.x_lower <= x_test and x_test <= self.body.env.x_upper
                y_bounded = self.body.env.y_lower <= y_test and y_test <= self.body.env.y_upper
                #print("At:({0}, {1}), Checking: ({2}, {3}), In Bounds:({4}, {5})".format(x, y, x_test, y_test, x_bounded, y_bounded))
                # Mark visited if already visited, or if Euclidean distance less than/equal to 10
                if x_bounded and y_bounded:
                    if not self.visited[x_test][y_test]:
                        euclid_dist = floor(np.sqrt((x_test-x)**2 + (y_test-y)**2))
                        self.visited[x_test][y_test] = int (euclid_dist <= 10)

        #Get list of all elements around body
        return self.body.scan()

    def perceiveMessage(self, message):
        return

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

    def prepareSeekTargets(self):
        # Check in all directions, move towards highest priority direction with unobserved cells
        if self.perceiveAbove():
            self.setAction("seek", "up")
        if self.perceiveBelow():
            self.setAction("seek", "down")
        if self.perceiveLeft():
            self.setAction("seek", "left")
        if self.perceiveRight():
            self.setAction("seek", "right")

        self.setWaypoint()


    def goToWaypoint(self):

        #Already there, nothing to do
        if self.getPosition() == self.memory["waypoint"]:
            return False
        else:
            #Get the difference between the positions
            x_diff = abs(self.getPosition()[0] - self.memory["waypoint"][0])
            y_diff = abs(self.getPosition()[1] - self.memory["waypoint"][1])

            result = False
            #Move in the direction with the most ground to travel
            if x_diff > y_diff:
                if self.getPosition()[0] > self.memory["waypoint"][0]:
                    result = self.body.move("left")
                else:
                    result = self.body.move("right")
            else:
                if self.getPosition()[1] > self.memory["waypoint"][1]:
                    result = self.body.move("up")
                else:
                    result = self.body.move("down")
            return result


    def setWaypoint(self):
        #Check if waypoint reached
        if self.memory["waypoint"] == self.getPosition():
            x_pos, y_pos = self.getPosition()
            ##Choose the highest priority task available
            # Grab something from the list and add it back
            chosen = self.selected_pattern.pop()
            self.selected_pattern.add(chosen)

            # Choose the highest priority item still in the list
            for pattern in self.selected_pattern:
                if self.action_patterns[pattern] >= self.action_patterns[chosen]:
                    chosen = pattern

            #Adjust the coordinates as needed
            if chosen == "up":
                y_pos -= 15
            elif chosen == "down":
                y_pos += 15
            elif chosen == "left":
                x_pos -= 15
            elif chosen == "right":
                x_pos += 15

            #Ensure coordinates are in bounds
            if y_pos > self.body.env.y_upper - 5:
                y_pos = self.body.env.y_upper - 5
            if y_pos < self.body.env.y_lower + 5:
                y_pos = self.body.env.y_lower + 5
            if x_pos > self.body.env.x_upper - 5:
                x_pos = self.body.env.x_upper - 5
            if x_pos < self.body.env.x_lower + 5:
                x_pos = self.body.env.x_lower + 5

            self.memory["waypoint"] = (x_pos, y_pos)
            self.clearAction()
        else: #Not there yet, keep going
            self.clearAction()
            return


    def prepareEvadeAgents(self, dodge):
        if len(dodge) == 0:
            return

        dodge_x, dodge_y = dodge[0].controller.getPosition()
        cur_x, cur_y = self.getPosition()
        new_x, new_y = self.getPosition()


        #if abs(dodge_x-cur_x) >= abs(dodge_y-cur_y):
        new_x += (cur_x-dodge_x)/3 + random.randint(-1,1)
        #else:
        new_y += (cur_y-dodge_y)/3 + random.randint(-1,1)

        self.memory["waypoint"] = (new_x, new_y)


    def prepareGatherKnownTarget(self):
        #If target found and waypoint reached
        if len(self.memory["known_targets"][self.getFaction()]) != 0 and self.memory["waypoint"] == self.getPosition():
            print(self.memory["known_targets"][self.getFaction()])
            print(self.memory["known_targets"])
            print(self.getFaction())
            x, y, found_by = self.memory["known_targets"][self.getFaction()][0]
            self.memory["waypoint"] = (x, y)


    def memorizeObservedTarget(self, entity_pos, entity_faction):
        self.memory["known_targets"][entity_faction].append((entity_pos[0], entity_pos[1], self.getFaction()))
        pass

    def runTurn(self):

        action_report = {"action_result":False, "collected_target":0}
        #Do the stuff!
        dodge = []
        visible = self.perceiveRadar()
        if len(visible) != 0:
            #Found something
            print("Something on radar!")

            #Check all radar hits
            for entity in visible:
                if entity.controller.getType() != "target":
                    #Other agent, dodge it
                    dodge.append(entity)
                else:
                    #Found a target
                    if entity.controller.getFaction() == self.getFaction():
                        #Found my target!
                        if not entity.controller.perceiveCollected():
                            entity.controller.collect()
                            self.memory["targets_found"] += 1
                            action_report["collected_target"] += 1
                            if len(self.memory["known_targets"][self.getFaction()]) != 0:
                                try:
                                    self.memory["known_targets"][self.getFaction()].remove(entity.controller.getPosition())
                                except ValueError:
                                    pass
                    else:
                        #Found someone else's target, remember for later
                        self.memorizeObservedTarget(entity.controller.getPosition(), entity.controller.getFaction())

        self.prepareGatherKnownTarget() #Collect found target
        self.prepareSeekTargets() #Look for targets
        self.prepareEvadeAgents(dodge) #Evade other agents

        #Execute the action and finalize the report
        action_report["action_result"] = self.goToWaypoint()#.executeAction()
        return action_report



class CompassionateController(Controller):
    pass



class TargetController(Controller):
    type = "target"
    collected = False

    def perceiveCollected(self):
        return self.collected

    def collect(self):
        self.collected = True
        print("Target collected!")
        return True
