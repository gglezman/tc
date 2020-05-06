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
import tc_styles


class InventoryTab(ttk.Frame):
    def __init__(self, master, notebook, **kwargs):
        """The inventory tab show information on all the sub-ordinante controllers in the system.

        :param master: Notebook holding the Inventory frame (i.e. TcGui)
        :param kwargs:
        """
        ttk.Frame.__init__(self, notebook, style='DarkGray.TFrame', padding=(10,40,10,10), **kwargs)
        self.master = master

        row = 0
        refreshButt = ttk.Button(self, text="Refresh Inventory", style="BiggerText.TButton", command=self.trigger_update)
        refreshButt.grid(row=row, column=0, sticky=tk.W)

        row += 1
        ttk.Label(self, text="Board Description", style="RidgeReliefML.TLabel",width=16)\
            .grid(row=row, column=0, sticky="nsew")
        ttk.Label(self, text="I2C Address", style="RidgeReliefML.TLabel", width=10)\
            .grid(row=row, column=1, sticky="nsew")
        ttk.Label(self, text="Board Type", style="RidgeReliefML.TLabel").grid(row=row, column=2, sticky="nsew")
        ttk.Label(self, text="Board Version", style="RidgeReliefML.TLabel").grid(row=row, column=3, sticky="nsew")
        ttk.Label(self, text="Inventory Version", style="RidgeReliefML.TLabel").grid(row=row, column=4, sticky="nsew")
        ttk.Label(self, text="I2C_Comm Sw Version", style="RidgeReliefML.TLabel").grid(row=row, column=5, sticky="nsew")
        ttk.Label(self, text="Inventory Sw Version", style="RidgeReliefML.TLabel").grid(row=row, column=6, sticky="nsew")
        ttk.Label(self, text="Application Version", style="RidgeReliefML.TLabel").grid(row=row, column=7, sticky="nsew")

    def trigger_update(self):
        self.master.update_inventory()

    def update_inventory(self, inventory):
        # find some way to clear out rows 1 - n

        row = 2
        for entry in inventory:
            e1 = ttk.Entry(self, width=16,font=("TkDefaultFont",12,"normal"))
            e1.grid(row=row, column=0, sticky="ew")
            e1.insert(0, entry["boardDescription"])

            e2 = ttk.Entry(self, width=10, justify=tk.CENTER,font=("TkDefaultFont",12,"normal"))
            e2.grid(row=row, column=1, sticky="ew")
            e2.insert(0, "0x{:02x}".format(entry["i2cAddress"]))

            e3 = ttk.Entry(self, width=8, justify=tk.CENTER,font=("TkDefaultFont",12,"normal"))
            e3.grid(row=row, column=2, sticky="ew")
            e3.insert(0, entry["boardType"])

            e4 = ttk.Entry(self, width=8, justify=tk.CENTER, font=("TkDefaultFont",12,"normal"))
            e4.grid(row=row, column=3, sticky="ew")
            e4.insert(0, entry["boardVersion"])

            e5 = ttk.Entry(self, width=8, justify=tk.CENTER, font=("TkDefaultFont",12,"normal"))
            e5.grid(row=row, column=4, sticky="ew")
            e5.insert(0, entry["inventoryVersion"])

            e6 = ttk.Entry(self, width=8, justify=tk.CENTER, font=("TkDefaultFont",12,"normal"))
            e6.grid(row=row, column=5, sticky="ew")
            e6.insert(0, entry["i2cCommSwVersion"])

            e7 = ttk.Entry(self, width=8, justify=tk.CENTER, font=("TkDefaultFont",12,"normal"))
            e7.grid(row=row, column=6, sticky="ew")
            e7.insert(0, entry["inventorySwVersion"])

            e8 = ttk.Entry(self, width=8, justify=tk.CENTER, font=("TkDefaultFont",12,"normal"))
            e8.grid(row=row, column=7, sticky="ew")
            e8.insert(0, entry["applicationSwVersion"])

            row +=1

