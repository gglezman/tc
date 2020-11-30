
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
# This file contains classes that are used by the train control python script.
# They implement the GUI to the Track Switch control.
#

import tkinter as tk
import tkinter.ttk as ttk
import threading
import tc_constants as tcc

class SwitchesTab(ttk.Frame):
    def __init__(self, master, i2c_comm, **kwargs):
        """Lights frame contains the light controls

        :param master: Notebook holding the Throttle frame
        :param i2c_comm - I2C_Comm object
        :param kwargs:
        """
        self.i2c_comm = i2c_comm

        ttk.Frame.__init__(self, master, style='DarkGray.TFrame', **kwargs)

    def update_inventory(self):
        pass