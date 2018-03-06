
class Agent:
    recent_messages = []
    destination = []
    next_move = ""
    known_nodes = []
    collected_count = 0

    commands = ["what_destination", "destination", "diverting", "no_diversion", "assert_destination", "what_nodes", "found_node", "node_at", "found_all"]

    def __init__(self, targ_type, x_pos, y_pos, playfield):
        self.targ_type = targ_type
        self.pos = [x_pos, y_pos]
        self.playfield = playfield
        return

    def receive(self, sender, message):
        self.recent_messages.append([message, sender, self.playfield.turn])
        return

    def send(self, recipient, message):
        if recipient == -1:
            self.playfield.broadcast(self, message)
        else:
            self.playfield.message(self, recipient, message)

    # Moves the agent in the specified direction
    def move(self):
        if self.next_move == "up":
            self.pos[1] += 1
        elif self.next_move == "down":
            self.pos[1] -= 1
        elif self.next_move == "left":
            self.pos[0] -= 1
        elif self.next_move == "right":
            self.pos[0] += 1
        self.next_move = ""

    # Checks if the agent can legally move in the chosen direction
    def canMove(self, direction):
        temp = self.pos.copy()
        if direction == self.playfield.directions[0]:
            temp[1] += 1
        elif direction == self.playfield.directions[1]:
            temp[1] -= 1
        elif direction == self.playfield.directions[2]:
            temp[0] -= 1
        elif direction == self.playfield.directions[3]:
            temp[0] += 1
        else:
            print("Invalid direction code: " + direction + " Agent Type: " + self.targ_type)
            return -1
        return self.playfield.inBounds(temp)

    def divert(self, sender_direction):
        if sender_direction == 1:  # If sender diverting down, divert up if possible, maintain heading if not
            if self.canMove("up"):
                self.next_move = "up"
            else:
                return -1
        elif sender_direction == 0:  # If sender diverting up, divert down if possible, maintain heading if not
            if self.canMove("down"):
                self.next_move = "down"
            else:
                return -1
        elif sender_direction == 2:  # If sender diverting left, divert right if possible, maintain heading if not
            if self.canMove("left"):
                self.next_move = "left"
            else:
                return -1
        elif sender_direction == 3:  # If sender diverting right, divert left if possible, maintain heading if not
            if self.canMove("right"):
                self.next_move = "right"
            else:
                return -1
        return self.next_move


    def selectDestination(self):
        return


    def playTurn(self):
        #Check sensors
            #Check radar
            #Check position
            #Check messages
            #Check memory

        #Evaluate goals
            #Check if reachable
            #Determine where to search for targets
        #Execute action
            #Send messages
            #Update memory
            #Update position
        return
        # Three stage model, high reaction time
        #self.controller.checkSensors()
        #self.controller.evaluateGoals()
        #self.controller.executeActions()


# NAVAL SEARCH PATTERNS USEFUL:
# Parallel Track
    # Steer straight courses on all legs
    # Each leg is one track spacing from the other
    # Legs are parallel to the long side or major axis of the search area
    # Commence Search Point (CSP) for parallel patterns is located at a point I/2 of the
        #distance selected as the search track spacing inside a corner of the search area
        #The first and last search legs then run I/2 track spacing inside the search area
        #boundaries. This prevents excessive duplicate coverage, eliminates the posibility
        #of leaving an unsearched track at the search area boundary, and gives SRU's in
        #adjacent search areas a margin of safety
# Expanding Square



