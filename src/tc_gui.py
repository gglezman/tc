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

import tkinter as tk
import tkinter.ttk as ttk
import tc_constants as tcc
from throttle import ThrottleTab
from inventory import InventoryTab
import tc_styles


class TcGui:
    def __init__(self):
        """Create the Train control GUI

        The init method creates the user frame and related objects.
        The run() function puts it up on the screen.
        """

        self.i2c_comm = None

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

        # create the tabs
        self.frameS = ttk.Frame(self.notebook, relief=tk.RIDGE)   # TODO These two will go away when I write
        self.frameL = ttk.Frame(self.notebook, relief=tk.RIDGE)   # classes for their respective pages

        # padding -> around the frame when the tab is selected
        self.notebook.add(ThrottleTab(self.notebook, relief=tk.RIDGE), text="Throttle", padding=tcc.tab_padding)
        self.notebook.add(self.frameS, text="Switches", padding=tcc.tab_padding)
        self.notebook.add(self.frameL, text="Lights", padding=tcc.tab_padding)

        self.inventoryTab = InventoryTab(self.notebook, relief=tk.RIDGE)
        self.notebook.add(self.inventoryTab, text="Inventory", padding=tcc.tab_padding)

        self.fill_switches_frame(self.frameS)
        self.fill_lights_frame(self.frameL)

    def run(self, i2c_comm):
        """Run the GUI

        :param i2c_comm: class to communicate over the IC bus to controllers
        :return: None
        """
        self.i2c_comm = i2c_comm

        # get screen width and height
        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = int((ws / 2) - (tcc.SCREEN_WIDTH / 2))
        y = int((hs / 2) - (tcc.SCREEN_HEIGHT / 2))

        # set the dimensions of the screen and where it is placed

        self.root.geometry('{}x{}+{}+{}'.format(tcc.SCREEN_WIDTH, tcc.SCREEN_HEIGHT, x, y))

        self.update_inventory()

        self.root.mainloop()

    def fill_switches_frame(self, switches_frame):
        None

    def fill_lights_frame(self, lights_frame):
        None

    def update_inventory(self):
        """USe the I2C_Comm services to collwect inventory information then feed it to the InventoryTab for display.

        This function runs periodically in case a new device is plugged in.

        :return: None
        """
        dev_list = self.i2c_comm.get_controller_list()

        board_info = []
        for dev in dev_list:
            adr = int(dev, base=16)
            board_info.append(self.i2c_comm.get_device_info(adr))

        self.inventoryTab.update_inventory(board_info)

        self.root.after(10000, self.update_inventory)

    def tc_exit(self):
        self.root.destroy()
        exit()
