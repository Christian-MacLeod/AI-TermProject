import threading
import gamemaster
import userinterface

class GrandMaster:
    steps_remaining = 0
    def __init__(self, thread_limit):
        self.log_file = "C:/Users/100560504/Downloads/_Artificial Intelligence/G21_1.csv"
        self.results_file = "C:/Users/100560504/Downloads/_Artificial Intelligence/G21_2.csv"
        self.max_threads = thread_limit
        self.thread_count_sem = threading.BoundedSemaphore(thread_limit)
        self.ui_lock = threading.BoundedSemaphore(1)
        if self.max_threads != 1:
            self.ui = None
            self.ui_lock.acquire()
        else:
            self.ui = userinterface.Interface()
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
            self.steps_remaining -= 1
            lock.release()


    def iterateSimulation(self, amount):
        self.steps_remaining = amount * 3
        self.spawnCompetitiveGames(amount)
        self.spawnCollaborativeGames(amount)
        self.spawnCompassionateGames(amount)
        while self.steps_remaining != 0:
            pass
        self.compileResults()

    def compileResults(self):
        sum_k = [0.0, 0.0, 0.0]
        sum_i = [0.0, 0.0, 0.0]
        count = [0.0, 0.0, 0.0]
        with open(self.log_file, "r") as log:
            for cnt, line in enumerate(log):
                segments = line.split(",")
                sum_k[int(segments[0])-1] += float(segments[10])
                sum_i[int(segments[0])-1] += float(segments[8])
                count[int(segments[0])-1] += 1

        lines = []
        for i in range(len(count)):
            lines.append("{0},{1},{2}\n".format(i, sum_i[i]/count[i], sum_k[i]/count[i]))

        with open(self.results_file, "w") as results:
            results.writelines(lines)


    def spawnCompetitiveGames(self, amount):
        for i in range(amount):
            self.thread_count_sem.acquire()
            game = gamemaster.GameMaster("competition", self.thread_count_sem, i, self.writeToLog)
            if self.ui_lock.acquire(False):
                game.registerUI(self.ui, self.ui_lock.release)

            if self.max_threads == 1:
                game.beginGame(1)
            else:
                game.start()

    def spawnCollaborativeGames(self, amount):
        for i in range(amount):
            self.thread_count_sem.acquire()
            game = gamemaster.GameMaster("collaboration", self.thread_count_sem, i, self.writeToLog)
            if self.ui_lock.acquire(False):
                game.registerUI(self.ui, self.ui_lock.release)
            if self.max_threads == 1:
                game.beginGame(2)
            else:
                game.start()

    def spawnCompassionateGames(self, amount):
        for i in range(amount):
            self.thread_count_sem.acquire()
            game = gamemaster.GameMaster("compassion", self.thread_count_sem, i, self.writeToLog)
            if self.ui_lock.acquire(False):
                game.registerUI(self.ui, self.ui_lock.release)
            if self.max_threads == 1:
                game.beginGame(3)
            else:
                game.start()