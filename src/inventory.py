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
    def __init__(self, master, **kwargs):
        """The inventory tab show information on all the sub-ordinante controllers in the system.

        :param master: Notebook holding the Inventory frame
        :param kwargs:
        """
        ttk.Frame.__init__(self, master, style='DarkGray.TFrame', padding=(40,40,10,10), **kwargs)

        row = 0
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


    def update_inventory(self, inventory):
        # find some way to clear out rows 1 - n

        row = 1
        for entry in inventory:
            e1 = ttk.Entry(self, width=16)
            e1.grid(row=row, column=0, sticky="ew")
            e1.insert(0, entry["boardDescription"])

            e2 = ttk.Entry(self, width=10, justify=tk.CENTER)
            e2.grid(row=row, column=1, sticky="ew")
            e2.insert(0, "0x{:02x}".format(entry["i2cAddress"]))

            e3 = ttk.Entry(self, width=8, justify=tk.CENTER)
            e3.grid(row=row, column=2, sticky="ew")
            e3.insert(0, entry["boardType"])

            e4 = ttk.Entry(self, width=8, justify=tk.CENTER)
            e4.grid(row=row, column=3, sticky="ew")
            e4.insert(0, entry["boardVersion"])

            e5 = ttk.Entry(self, width=8, justify=tk.CENTER)
            e5.grid(row=row, column=4, sticky="ew")
            e5.insert(0, entry["inventoryVersion"])

            e6 = ttk.Entry(self, width=8, justify=tk.CENTER)
            e6.grid(row=row, column=5, sticky="ew")
            e6.insert(0, entry["i2cCommSwVersion"])

            e7 = ttk.Entry(self, width=8, justify=tk.CENTER)
            e7.grid(row=row, column=6, sticky="ew")
            e7.insert(0, entry["inventorySwVersion"])

            e8 = ttk.Entry(self, width=8, justify=tk.CENTER)
            e8.grid(row=row, column=7, sticky="ew")
            e8.insert(0, entry["applicationSwVersion"])

            row +=1

