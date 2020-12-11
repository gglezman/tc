#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
# This file contains classes that are used by the cash flow python script
# to present a GUI to the cash flow report.
#

from time import sleep
import tkinter as tk
import tkinter.ttk as ttk
import tc_constants as tcc
from throttle import ThrottleTab
from lights import LightsTab
from switches import SwitchesTab
from inventory import InventoryTab
from raspArduinoTest import RaspArduinoTestTab
import tc_styles

LIGHTS_FILE="lights.csv"

class TcGui:
    def __init__(self, i2c_comm):
        """Create the Train control GUI

        The init method creates the user frame and related objects.
        The run() function puts it up on the screen.
        """

        self.i2c_comm = i2c_comm
        self.board_inventory = []

        self.root = tk.Tk()
        self.root.title("Train Control Platform")
        self.root.protocol("WM_DELETE_WINDOW", self.tc_exit)

        tc_styles.set_styles()

        # option: height and width of the notebook in the frame
        # option: padding - space around notebook pane
        # self.notebook = ttk.Notebook(self.root, width=600, height=200, padding=(W, N, E, S))
        self.notebook = ttk.Notebook(self.root)
        # file the entire window
        self.notebook.pack(fill=tk.BOTH, expand=1)

        # padding -> around the frame when the tab is selected
        self.throttleTab = ThrottleTab(self.notebook, i2c_comm, relief=tk.RIDGE)
        self.notebook.add(self.throttleTab, text="Throttle", padding=tcc.tab_padding)

        self.switchesTab = SwitchesTab(self.notebook, i2c_comm, relief=tk.RIDGE)
        self.notebook.add(self.switchesTab, text="Switches", padding=tcc.tab_padding)

        self.lightsTab = LightsTab(self.notebook, LIGHTS_FILE, i2c_comm, relief=tk.RIDGE)
        self.notebook.add(self.lightsTab, text="Lights", padding=tcc.tab_padding)

        self.inventoryTab = InventoryTab(self, self.notebook, relief=tk.RIDGE)
        self.notebook.add(self.inventoryTab, text="Inventory", padding=tcc.tab_padding)

        self.raspArduinoTestTab = RaspArduinoTestTab(self, self.notebook, self.root, self.i2c_comm, relief=tk.RIDGE)
        self.notebook.add(self.raspArduinoTestTab, text="Test", padding=tcc.tab_padding)

    def run(self):
        """Run the GUI
        :return: None
        """
        self.board_inventory = self.collect_inventory()
        self.throttleTab.update_inventory(self.board_inventory)
        self.lightsTab.update_inventory(self.board_inventory)
        self.inventoryTab.update_inventory(self.board_inventory)
        self.raspArduinoTestTab.update_inventory(self.board_inventory)

        # get screen width and height
        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        #x = int((ws / 2) - (tcc.SCREEN_WIDTH / 2))
        #y = int((hs / 2) - (tcc.SCREEN_HEIGHT / 2))
        x = 1   # if I use (0,0) I end up in the middle of the display !!
        y = 1
        # set the dimensions of the screen and where it is placed

        #self.root.geometry('{}x{}+{}+{}'.format(tcc.SCREEN_WIDTH, tcc.SCREEN_HEIGHT, x, y))
        # todo - should I define the width of the screen or use what the actual size is ??
        #        how does this effect all my other size selections
        print('{}x{}+{}+{}'.format(ws, hs, x, y))
        self.root.geometry('{}x{}+{}+{}'.format(ws, hs, x, y))

        self.root.mainloop()

    def collect_inventory(self):
        """Use the I2C_Comm services to collect inventory information.

        This function uses the I2C bus to collect inventory information from all connect
        board controllers.

        :return: board_inventory - a list of dictionary entries describing each board in the system.
        """
        dev_list = self.i2c_comm.get_controller_list()

        board_inventory = []
        for dev in dev_list:
            adr = int(dev, base=16)
            board_inventory.append(self.i2c_comm.get_device_info(adr))

        return board_inventory

    def tc_exit(self):
        self.throttleTab.shutDown()
        sleep(.5)
        exit()
