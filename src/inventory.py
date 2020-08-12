#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
# This file contains a class that controls what goes in the Inventory Tab of the train Control notebook
#


import tkinter as tk
import tkinter.ttk as ttk
import tc_constants as tcc
from tkinter.font import Font

class InventoryTab(ttk.Frame):
    def __init__(self, master, notebook, **kwargs):
        """The inventory tab show information on all the sub-ordinante controllers in the system.

        :param master: top level object (i.e. TcGui)
        :param notebook: Notebook holding the Inventory frame (i.e. TcGui)
        :param kwargs:
        """
        ttk.Frame.__init__(self, notebook, style='DarkGray.TFrame', padding=(10,40,10,10), **kwargs)
        self.master = master

        self.textFont = Font(family="Helvetica", size=12)

        row  = 0
        ttk.Label(self, text="Board\nDescription", style="RidgeReliefML.TLabel",width=16)\
            .grid(row=row, column=0, sticky="nsew")
        ttk.Label(self, text="I2C\nAddress", style="RidgeReliefML.TLabel", width=10)\
            .grid(row=row, column=1, sticky="nsew")
        ttk.Label(self, text="Board\nType", style="RidgeReliefML.TLabel").grid(row=row, column=2, sticky="nsew")
        ttk.Label(self, text="Board\nVersion", style="RidgeReliefML.TLabel").grid(row=row, column=3, sticky="nsew")
        ttk.Label(self, text="Inventory\nVersion", style="RidgeReliefML.TLabel").grid(row=row, column=4, sticky="nsew")
        ttk.Label(self, text="I2C_Comm\nSw Version", style="RidgeReliefML.TLabel").grid(row=row, column=5, sticky="nsew")
        ttk.Label(self, text="Inventory\nSw Version", style="RidgeReliefML.TLabel").grid(row=row, column=6, sticky="nsew")
        ttk.Label(self, text="Application\nVersion", style="RidgeReliefML.TLabel").grid(row=row, column=7, sticky="nsew")

    def update_inventory(self, inventory):
        # find some way to clear out rows 1 - n

        row = 2
        for entry in inventory:
            e1 = ttk.Entry(self, width=16, font=self.textFont)
            e1.grid(row=row, column=0, sticky="ew")
            e1.insert(0, entry["boardDescription"])

            e2 = ttk.Entry(self, width=10, justify=tk.CENTER,font=self.textFont)
            e2.grid(row=row, column=1, sticky="ew")
            e2.insert(0, "0x{:02x}".format(entry["i2cAddress"]))

            e3 = ttk.Entry(self, width=8, justify=tk.CENTER,font=self.textFont)
            e3.grid(row=row, column=2, sticky="ew")
            e3.insert(0, entry["boardType"])

            e4 = ttk.Entry(self, width=8, justify=tk.CENTER, font=self.textFont)
            e4.grid(row=row, column=3, sticky="ew")
            e4.insert(0, entry["boardVersion"])

            e5 = ttk.Entry(self, width=8, justify=tk.CENTER, font=self.textFont)
            e5.grid(row=row, column=4, sticky="ew")
            e5.insert(0, entry["inventoryVersion"])

            e6 = ttk.Entry(self, width=8, justify=tk.CENTER, font=self.textFont)
            e6.grid(row=row, column=5, sticky="ew")
            e6.insert(0, entry["i2cCommSwVersion"])

            e7 = ttk.Entry(self, width=8, justify=tk.CENTER, font=self.textFont)
            e7.grid(row=row, column=6, sticky="ew")
            e7.insert(0, entry["inventorySwVersion"])

            e8 = ttk.Entry(self, width=8, justify=tk.CENTER, font=self.textFont)
            e8.grid(row=row, column=7, sticky="ew")
            e8.insert(0, entry["applicationSwVersion"])

            row +=1

