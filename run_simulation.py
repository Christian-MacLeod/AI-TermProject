from grandmaster import GrandMaster
#Christian MacLeod AI Term Project

print("Runs specified amount of games, outputs results as G21_*.csv")
threads = input("How many games to run concurrently? (Visualization only possible with value 1)")
if str.isdigit(threads) and int (threads) < 1:
    threads = 1
grandmaster = GrandMaster(int(threads))

competitive = input("How many competitive (t1) games to run?")
if str.isdigit(competitive) and int(competitive) < 0:
    competitive = 0

collaborative = input("How many collaborative (t2) games to run?")
if str.isdigit(collaborative) and int(collaborative) < 0:
    collaborative = 0

compassionate = input("How many competitive (t3) games to run?")
if str.isdigit(compassionate) and int(compassionate) < 0:
    compassionate = 0

grandmaster.iterateSimulation([int(competitive), int(collaborative), int(compassionate)])
