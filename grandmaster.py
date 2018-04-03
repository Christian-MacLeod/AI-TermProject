import threading
import gamemaster
import userinterface

class GrandMaster:

    def __init__(self, thread_limit):
        self.log_file = "C:/Users/100560504/Downloads/_Artificial Intelligence/G21_1.csv"
        self.results_file = "C:/Users/100560504/Downloads/_Artificial Intelligence/G21_2.csv"
        self.thread_count_sem = threading.BoundedSemaphore(thread_limit)
        self.ui = userinterface.Interface()
        self.ui_lock = threading.BoundedSemaphore(1)
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
            if self.ui_lock.acquire(False):
                game.registerUI(self.ui, self.ui_lock.release)
            game.beginGame(1)
            #game.start()

    def spawnCollaborativeGames(self, amount):
        for i in range(amount):
            self.thread_count_sem.acquire()
            game = gamemaster.GameMaster("collaboration", self.thread_count_sem, i, self.writeToLog)
            if self.ui_lock.acquire(False):
                game.registerUI(self.ui, self.ui_lock.release)
            game.beginGame(2)
            #game.start()

    def spawnCompassionateGames(self, amount):
        for i in range(amount):
            self.thread_count_sem.acquire()
            game = gamemaster.GameMaster("compassion", self.thread_count_sem, i, self.writeToLog)
            if self.ui_lock.acquire(False):
                game.registerUI(self.ui, self.ui_lock.release)
            game.beginGame(3)
            #game.start()