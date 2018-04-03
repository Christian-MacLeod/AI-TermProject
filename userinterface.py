import tkinter as Tk
from PIL import Image
from PIL import ImageTk as pilImageTk
from PIL import ImageColor
import numpy

class Interface:
    #Aquired from memory snapshot at first step
    ten_radius_circle = Image.fromarray(numpy.uint8(255*numpy.array([[0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,  0],
        [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,  0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,  0],
        [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,  0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,  0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,  0],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,  0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,  0],
        [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,  0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,  0],
        [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,  0],
        [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,  0]])))

    def __init__(self):
        self.agents = []
        self.targets = []
        self.root_ui = Tk.Tk()
        self.current_frame = pilImageTk.PhotoImage(Image.new("RGBA", (100, 100), 0).resize((400,400)))
        self.image_holder = Tk.Label(self.root_ui, image=self.current_frame)
        self.image_holder.pack()
        self.root_ui.update_idletasks()
        self.root_ui.update()
        #self.ten_radius_circle.show()
        #self.new_ten_rad.show()

        #self.map.paste(Image.new("RGBA",(21,21), 0xffffff), (-10,-10), self.ten_radius_circle)
        #self.map.load()
        #self.map.show()
        #self.ten_radius_circle.show() ImageColor.getrgb("Blue")
        #self.ten_radius_circle_1bit.show()

    def registerGame(self, game, title):
        self.agents = game.agents
        self.targets = game.targets
        self.root_ui.title = title


    @staticmethod
    def drawMaps(stat_sheet):
        for sheet in stat_sheet:
            controller = sheet["controller"]
            #print("Drawing {0} agent's memory".format(controller["controller"].faction)) #NOTE: Diagnostic
            loc_map = Image.new("1", (100,100), 0x1)
            #loc_map = Image.fromarray(controller.visited, "1")
            for x in range(len(controller.visited)):
                for y in range(len(controller.visited[x])):
                    loc_map.putpixel((x,y), controller.visited[x][y])
            #print(controller.getPosition())
            loc_map.putpixel(controller.getPosition(), 0)
            #loc_map.putdata(controller.visited)
            #loc_map = Image.fromarray(controller["controller"].visited.astype(bool), "1")
            #print(controller["controller"].visited)
            #loc_map.putpixel((0,0),0x1)
            loc_map.load()
            loc_map.show(controller.faction)


            return

    def updateDisplay(self):
        frame = Image.new("RGBA", (100,100), 0)
        for agent in self.agents:
            pos_x, pos_y = agent["controller"].getPosition()
            frame.paste(agent["controller"].getFaction(), (pos_x - 10, pos_y - 10), self.ten_radius_circle)
        for target in self.targets:
            frame.putpixel(target.getPosition(), ImageColor.getrgb(target.getFaction()))
        #self.current_frame = pilImageTk.PhotoImage(frame)
        x = None
        self.current_frame.paste(frame.resize((400,400)))
        #self.image_holder = Tk.Label(self.root_ui, image=self.current_frame)
        #self.image_holder.pack()
        self.root_ui.update_idletasks()
        self.root_ui.update()

