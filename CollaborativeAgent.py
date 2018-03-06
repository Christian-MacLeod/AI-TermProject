import agent
import random

class CollaborativeAgent(agent.Agent):
    def __init__(self, targ_type, x_pos, y_pos, playfield):
        super().__init__(targ_type, x_pos, y_pos, playfield)

    #commands = ["what_destination", "destination", "diverting", "no_diversion", "assert_destination", "what_nodes", "found_node", "node_at", "found_all"]

    def receive(self, sender, message):
        self.recent_messages.append([self.playfield.turn, sender, message]) #Log the message

        if message[0] == self.commands[0]: #If requesting destination, send destination
            return [self.commands[1], self.destination]

        elif message[0] == self.commands[2]: #If announcing diversion, divert opposite if possible
            direction = self.divert(message[1])
            return [self.commands[2], direction]

        elif message[0] == self.commands[3]: #If announcing colliding destinations, flip coin; heads assert, tails change course
            coin = random.Random()
            if coin.randint(0,1) == 1:
                return [self.commands[4]]
            else:
                self.selectDestination()
                return [self.commands[1], self.destination]
        elif message[0] == self.commands[4]: #If announcing assertion, change course
            self.selectDestination()

    def avoidRadarRange(self, agent_faction, agent_position): #Called when agent spotted on radar
        return


        # Check sensors
            # Check radar
            # Check position
            # Check messages
            # Check memory

        # Evaluate goals
            # Check if reachable
            # Determine where to search for targets
        # Execute action
            # Send messages
            # Update memory
            # Update position
    def playTurn(self):
        scan_results = self.playfield.scan(self)
        if len(scan_results) > 0:
            #Results!
            print("Found something on radar")
            for entity in scan_results: #[type, faction, coordinates]
                if entity[0] == "agent": #if agent
                    print("Enemy agent spotted!")
                    self.avoidRadarRange(entity[1], entity[2])
                else: #if target
                    if entity[1] == self.targ_type: #if ours, collect
                        print("Found a target!")
                        self.playfield.collect(entity[1], entity[2])
                        self.collected_count += 1
                    else: #if opponent's, log for later trade
                        print("Found an enemy target!")
                        self.known_nodes.append([False, entity[1], entity[2]])
        else:
            print("Nothing on radar")
        return None
