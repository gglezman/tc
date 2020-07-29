#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
# This file contains a class that controls what goes in the RPI / Arduino test tab
#


import os
import tkinter as tk
import tkinter.ttk as ttk
#from I2C_Transport import I2C_Transport


class RaspArduinoTestTab(ttk.Frame):
    def __init__(self, master, notebook, **kwargs):
        """Run one or more tests against the given list of Arduinos

          :param master: top level object (i.e. TcGui)
          :param notebook: Notebook holding the RasArduinoTest frame (i.e. TcGui)
          :param kwargs:
          """

        
        ttk.Frame.__init__(self, notebook, style='DarkGray.TFrame', padding=(10, 40, 10, 10), **kwargs)
        self.master = master

        #self.i2c_bus = i2c_bus
        #self.arduino_list = arduino_list
        self.status_widgets = {}  # test result widgets
        self.test_running = False
        self.runButt = None
        self.iter_count = None
        self.exitButt = None

        # Create a frame to hold the test data
        self.arduino_frame = self.add_frame(self)
        row = 0
        col = 0

        ttk.Button(self.arduino_frame, text="Arduino Address", style='MultiLine.TLabel'). \
            grid(row=row, column=col, sticky='W')
        col += 1
        ttk.Button(self.arduino_frame, text="Total Transmissions", style='MultiLine.TLabel'). \
            grid(row=row, column=col, sticky='W')
        col += 1
        ttk.Button(self.arduino_frame, text="Read Exceptions", style='MultiLine.TLabel'). \
            grid(row=row, column=col, sticky='W')
        col += 1
        ttk.Button(self.arduino_frame, text="Write Exceptions", style='MultiLine.TLabel'). \
            grid(row=row, column=col, sticky='W')
        col += 1
        ttk.Button(self.arduino_frame, text="Data Mismatches", style='MultiLine.TLabel'). \
            grid(row=row, column=col, sticky='W')
        col += 1
        ttk.Button(self.arduino_frame, text="Uncorrected Errors", style='MultiLine.TLabel'). \
            grid(row=row, column=col, sticky='W')

    def update_inventory(self, inventory):
        pass
        # add a row to the frame for each Arduino found
        self.create_arduino_rows(self.arduino_frame, inventory)

        # Add buttons in bottom row
        # Create a frame to hold the test data
        self.button_frame = self.add_frame(self)
        self.add_control_buttons(self.button_frame)

        #self.win.mainloop()

    def run(self):
        """Start the test running"""

        self.test_running = True
        self.runButt.configure(text="Running")
        self.win.update_idletasks()

        # read the test selection combo box
        active_test = self.testSelect.get()
        iterations = int(self.iter_count.get())

        if active_test == "Read":
            self.read_test(iterations)
        elif active_test == "Write/Verify":
            self.write_verify_test(iterations)
        else:
            print("Unknown test requested: {}".format(active_test))

        self.test_running = False
        self.runButt.configure(text="Run Test")
        self.iter_count.delete(0, tk.END)
        self.iter_count.insert(0, iterations)

    def cancel_win(self):
        self.win.destroy()

    def create_arduino_rows(self, frame, inventory):
        """Create a row for each Arduino in the list."""
        col_width = 15
        row = 1
        col = 0

        for arduino in inventory:
            arduino_adr = arduino["i2cAddress"]
            col = 0
            ttk.Label(frame, text="0x{:02x}".format(arduino_adr)).grid(row=row, column=col)
            col += 1
            tot_transmit_box = ttk.Entry(frame, w=col_width)  # transmissions
            tot_transmit_box.insert(0, 0)
            tot_transmit_box.grid(row=row, column=col)
            col += 1
            read_exception_box = ttk.Entry(frame, w=col_width)  # errors
            read_exception_box.insert(0, 0)
            read_exception_box.grid(row=row, column=col)
            col += 1
            write_exception_box = ttk.Entry(frame, w=col_width)
            write_exception_box.insert(0, 0)
            write_exception_box.grid(row=row, column=col)
            col += 1
            data_mismatch_box = ttk.Entry(frame, w=col_width)
            data_mismatch_box.insert(0, 0)
            data_mismatch_box.grid(row=row, column=col)
            col += 1
            uncorrected_box = ttk.Entry(frame, w=col_width)
            uncorrected_box.insert(0, 0)
            uncorrected_box.grid(row=row, column=col)
            col += 1
            row += 1
            # capture the widgets. I'll update them when the test runs
            self.status_widgets[arduino_adr] = \
                (tot_transmit_box, read_exception_box, \
                 write_exception_box, data_mismatch_box, uncorrected_box)

    @staticmethod
    def add_frame(parent, x_padx=2, x_pady=2, i_pad=3,
                  fill=tk.BOTH, expand=1, side=tk.TOP):
        """Add a frame to the given window.

        The x_padx and x_pady values place spacers around the outside
        of the border.
        """

        # Frame padding is internal to the border
        frame = ttk.Frame(parent, padding=i_pad,
                          borderwidth=2,
                          relief=tk.RIDGE)
        if expand == 1:
            # Stretch on resize
            frame.pack(fill=fill, expand=1, padx=x_padx, pady=x_pady, side=side)
        else:
            frame.pack(fill=fill, padx=x_padx, pady=x_pady, side=side)

        return frame

    def add_control_buttons(self, frame):
        test_control_frame = ttk.Frame(frame)
        test_control_frame.pack(side=tk.LEFT)

        exit_butt_frame = ttk.Frame(frame)
        exit_butt_frame.pack(side=tk.RIGHT)

        row = 0
        col = 0

        self.runButt = ttk.Button(test_control_frame, text="Run Test", w=9,
                                  command=self.run)
        self.runButt.grid(row=row, column=col, sticky='W')
        col += 1
        test_label = ttk.Label(test_control_frame, text="  Test: ")
        test_label.grid(row=row, column=col, sticky='W')
        col += 1
        self.testSelect = ttk.Combobox(test_control_frame,
                                       style="Padded.TCombobox",
                                       values=["Read", "Write/Verify"],
                                       w=12)
        self.testSelect.grid(row=row, column=col, sticky='W')
        self.testSelect.current(0)
        col += 1
        label = ttk.Label(test_control_frame, text=" IterCount: ")
        label.grid(row=row, column=col, sticky='W')
        col += 1
        self.iter_count = ttk.Entry(test_control_frame, w=4,
                                    style="Padded.TEntry")
        self.iter_count.grid(row=row, column=col, sticky='W')
        self.iter_count.insert(0, 10)
        col += 1
        self.exitButt = ttk.Button(exit_butt_frame, text="Exit", w=4,
                                   command=quit).grid()

    def read_test(self, iterations):
        for i in range(iterations):
            for adr in self.arduino_list:
                result = self.i2c_bus.block_read_test(int(adr, base=16), 99)

                # Update the totals in the GUI with the new results
                (tot_transmit_box, read_exception_box, write_exception_box, \
                 data_mismatch_box, uncorrected_box) = self.status_widgets[adr]

                tt = int(tot_transmit_box.get()) + result[0]
                tot_transmit_box.delete(0, tk.END)
                tot_transmit_box.insert(0, tt)

                re = int(read_exception_box.get()) + result[1]
                read_exception_box.delete(0, tk.END)
                read_exception_box.insert(0, re)

                dm = int(data_mismatch_box.get()) + result[2]
                data_mismatch_box.delete(0, tk.END)
                data_mismatch_box.insert(0, dm)

                self.win.update_idletasks()
                self.iter_count.delete(0, tk.END)
                self.iter_count.insert(0, iterations - i - 1)

    def write_verify_test(self, iterations):
        for i in range(iterations):
            for adr in self.arduino_list:
                result = self.i2c_bus.block_write_test(int(adr, base=16), 100)

                # Update the totals in the GUI with the new results
                (tot_transmit_box, read_exception_box, write_exception_box, \
                 data_mismatch_box, uncorrected_box) = self.status_widgets[adr]
                ct = int(tot_transmit_box.get()) + result[0]
                re = int(read_exception_box.get()) + result[1]
                we = int(write_exception_box.get()) + result[2]
                dm = int(data_mismatch_box.get()) + result[3]
                uc = int(uncorrected_box.get()) + result[4]
                tot_transmit_box.delete(0, tk.END)
                tot_transmit_box.insert(0, ct)
                read_exception_box.delete(0, tk.END)
                read_exception_box.insert(0, re)
                write_exception_box.delete(0, tk.END)
                write_exception_box.insert(0, we)
                data_mismatch_box.delete(0, tk.END)
                data_mismatch_box.insert(0, dm)
                uncorrected_box.delete(0, tk.END)
                uncorrected_box.insert(0, uc)
                self.win.update_idletasks()
                self.iter_count.delete(0, tk.END)
                self.iter_count.insert(0, iterations - i - 1)



