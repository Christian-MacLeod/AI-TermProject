import tkinter as Tk
from PIL import Image

class Interface:

    @staticmethod
    def drawMaps(controllers):
        for controller in controllers:
            print("Drawing {0} agent's memory".format(controller["controller"].faction))
            loc_map = Image.fromarray(controller["controller"].visited.astype(int), "L")
            loc_map.show(controller["controller"].faction)
        return

