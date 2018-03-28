import threading
class Executioner:

    def __init__(self):
        self.log_file = "G21_1.csv"
        self.results_file = "G21_2.csv"
        return

    def writeToLog(self, lines):
        #Mutex lock to prevent simultaneous writes
        lock = threading.RLock()

        with lock.acquire():
            #Write each line to the log
            with open(self.log_file, "a") as log:
                log.writelines(lines)

    def iterateSimulation(self, amount):
        self.spawnCompetitiveGames(amount)
        self.spawnCollaborativeGames(amount)
        self.spawnCompassionateGames(amount)
        self.compileResults()

    def compileResults(self):
        pass

    def spawnCompetitiveGames(self, amount):

        pass

    def spawnCollaborativeGames(self, amount):
        pass

    def spawnCompassionateGames(self, amount):
        pass