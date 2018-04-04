import tkinter as Tk
from PIL import Image
from PIL import ImageTk as pilImageTk
from PIL import ImageColor
import numpy

class Interface:
    #Aquired from memory snapshot at first step
    ten_radius_circle = Image.fromarray(numpy.uint8(255*numpy.array([
        [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
        [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0]
    ])))

    def __init__(self, dimensions, scaled=False):
        self.agents = []
        self.targets = []
        self.image_dimensions = dimensions
        self.image_scaled = scaled
        if not self.image_scaled:
            self.image_scaled = self.image_dimensions
        self.root_ui = Tk.Tk()
        self.current_frame = pilImageTk.PhotoImage(Image.new("RGBA", dimensions, 0).resize(self.image_scaled))
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

    def updateDisplay(self):
        frame = Image.new("RGBA", self.image_dimensions, ImageColor.getrgb("black"))
        for agent in self.agents:
            pos_x, pos_y = agent["controller"].getPosition()
            frame.paste(agent["controller"].getFaction(), (pos_x - 10, pos_y - 10), self.ten_radius_circle)
        for target in self.targets:
            if target.perceiveCollected():
                colour = "grey"
            else:
                colour = target.getFaction()

            frame.putpixel(target.getPosition(), ImageColor.getrgb(colour))
        #self.current_frame = pilImageTk.PhotoImage(frame)
        self.current_frame.paste(frame.resize(self.image_scaled))
        #self.image_holder = Tk.Label(self.root_ui, image=self.current_frame)
        #self.image_holder.pack()
        self.root_ui.update_idletasks()
        self.root_ui.update()

