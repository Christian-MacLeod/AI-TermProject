import threading
import gamemaster

class GrandMaster:

    def __init__(self, thread_limit):
        self.log_file = "C:/Users/100560504/Downloads/_Artificial Intelligence/G21_1.csv"
        self.results_file = "C:/Users/100560504/Downloads/_Artificial Intelligence/G21_2.csv"
        self.thread_count_sem = threading.BoundedSemaphore(thread_limit)
        return

    def writeToLog(self, lines):
        #Mutex lock to prevent simultaneous writes
        #lock = threading.RLock()
        lock = threading.RLock()
        try:
            lock.acquire()
            # Write each line to the log
            with open(self.log_file, "a") as log:
                log.writelines(lines)
        finally:
            lock.release()


    def iterateSimulation(self, amount):
        self.spawnCompetitiveGames(amount)
        self.spawnCollaborativeGames(amount)
        self.spawnCompassionateGames(amount)
        self.compileResults()

    def compileResults(self):
        pass

    def spawnCompetitiveGames(self, amount):
        for i in range(amount):
            self.thread_count_sem.acquire()
            game = gamemaster.GameMaster("competition", self.thread_count_sem, i, self.writeToLog)
            game.start()

    def spawnCollaborativeGames(self, amount):
        for i in range(amount):
            self.thread_count_sem.acquire()
            game = gamemaster.GameMaster("collaboration", self.thread_count_sem, i, self.writeToLog)
            game.start()

    def spawnCompassionateGames(self, amount):
        for i in range(amount):
            self.thread_count_sem.acquire()
            game = gamemaster.GameMaster("compassion", self.thread_count_sem, i, self.writeToLog)
            game.start()