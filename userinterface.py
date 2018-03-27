import tkinter as Tk
from PIL import Image

class Interface:

    def __init__(self, game):
        self.agents = game.agents
        self.targets = game.targets

    @staticmethod
    def drawMaps(stat_sheet):
        #for sheet in stat_sheet:
        controller = stat_sheet[0]["controller"]
        #print("Drawing {0} agent's memory".format(controller["controller"].faction)) #NOTE: Diagnostic
        loc_map = Image.new("1", (100,100), 0x1)
        #loc_map = Image.fromarray(controller.visited, "1")
        for x in range(len(controller.visited)):
            for y in range(len(controller.visited[x])):
                loc_map.putpixel((x,y), controller.visited[x][y])
        loc_map.putpixel(controller.getPosition(), 0)
        #loc_map.putdata(controller.visited)
        #loc_map = Image.fromarray(controller["controller"].visited.astype(bool), "1")
        #print(controller["controller"].visited)
        #loc_map.putpixel((0,0),0x1)
        loc_map.load()
        loc_map.show(controller.faction)
        return

    def drawMap(self):


        return
