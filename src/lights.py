#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
# This file contains classes that are used by the train control python script.
# They implement the GUI to the Lights control.
#

import tkinter as tk
import tkinter.ttk as ttk
import csv
from time import sleep
import tc_constants as tcc

INVALID_PIN = "99"
ALL_PIN = INVALID_PIN

class LightsTab(ttk.Frame):
    def __init__(self, master, lights_file, i2c_comm, **kwargs):
        """Lights frame contains the light controls

        :param master: Notebook holding the Throttle frame
        :param i2c_comm - I2C_Comm object
        :param kwargs:
        """
        self.i2c_comm = i2c_comm
        self.lights_control_address = 0

        # ##################################################################
        # open the Lights config file to determine what the user wants
        # ##################################################################
        light_switches = []
        with open(lights_file, 'r', newline='') as file_handle:
            reader = csv.DictReader(file_handle)
            for rec in reader:
                light_switches.append(rec)
        light_switch_count = len(light_switches)

        # ##################################################
        # Create the frame and add the header
        # ##################################################
        ttk.Frame.__init__(self, master, style='DarkGray.TFrame', padding=(80, 1), **kwargs)
        self.pack()

        heading = ttk.Label(self,text="Lighting Control Panel",style="DarkGray.TLabel",
                  font=("TkDefaultFont", tcc.extra_large, "bold"),
                  anchor='center')
        heading.grid(row=1, column=0, sticky='nsew',columnspan=6, pady=20)
        row_offset=1

        max_row = int((light_switch_count+1) / 2)    # the +1 ensures the odd switch is in the 1st column
        instance = 0

        # ##################################################
        # Add a switch for each entry in the config file
        # ##################################################
        switch_objects = []
        for light_switch in light_switches:
            row = int(instance % max_row) + 1  + row_offset         # +1 since row numbering starts with 1,
            col = (int(instance / max_row) *3) + 1                  # *3 since each switch gets 3 columns

            if light_switch['type'] == 'simple':
                switch_objects.append(SimpleLight(self, row, col, light_switch))
            elif light_switch['type'] == 'fourway':
                switch_objects.append(FourWayLight(self, row, col, light_switch))
            elif light_switch['type'] == 'slider':
                switch_objects.append(SliderLight(self, row, col, light_switch))
            else:
                print("Unknown switch type '{}' in file: {}".format(light_switch['type'],lights_file))
            instance += 1

        # ##################################################
        # Add the "All On/Off" Button - center it
        # ##################################################
        all_frame = ttk.Frame(self,style='DarkGray.TFrame',padding=(60,20))

        all_frame.grid(row=max_row+2,column=3,columnspan=4, sticky='w')
        AllLightsButton(all_frame, 1, 1, switch_objects)

    def update_inventory(self, inventory):
        for entry in inventory:
            if entry['boardType'] == tcc.BOARD_TYPE_LIGHTS:
                self.lights_control_address = entry['i2cAddress']

    def button_pressed(self, pins, power_level):
        """One of the switches has been depressed. Communicate it to the board controller.
        Sed the pin number and the new power level.
        """
        for pin in pins:
            if pin != INVALID_PIN:
                print("Pin {} to power level {}".format(pin,power_level))
                self.i2c_comm.write_register_verify(self.lights_control_address,
                                                     tcc.I2C_REG_LIGHT_POWER_LEVEL,
                                                     [int(pin), int(power_level)])
            else:
                print("Invalid pin number detected in button_pressed")


class SimpleLight:
    def __init__(self, frame, row, col, light_switch, **kwargs ):

        self.frame = frame
        self.instance = row*col
        self.off_level = int(light_switch['off_setting'])
        self.full_level = int(light_switch['full_setting'])
        self.pins = light_switch['pins'].split(',')

        self.state = 'off'

        col = col
        self.off_button = ttk.Button(frame, text='OFF', style='LightsOff.TButton', command=self.off_button_pressed)
        self.off_button.grid(row=row, column=col, sticky=('W'), pady=3)

        col +=1
        self.on_button = ttk.Button(frame, text='ON', style='LightsReady.TButton', command=self.on_button_pressed)
        self.on_button.grid(row=row, column=col, sticky=('W'), pady=3)

        col += 1
        label = ttk.Label(frame, text=light_switch['text'],
                  style='DarkGray.TLabel',
                  width=30,
                  anchor=tk.W)
        label.grid(row=row, column=col, sticky=('W'), padx=6)

    def off_button_pressed(self):
        if self.state == 'on':
            self.state = 'off'
            self.off_button.config(style='LightsOff.TButton')
            self.on_button.config(style='LightsReady.TButton')

            self.frame.button_pressed(self.pins, self.off_level)

    def on_button_pressed(self):
        if self.state == 'off':
            self.state = 'on'
            self.off_button.config(style='LightsReady.TButton')
            self.on_button.config(style='LightsOnFull.TButton', text='ON')

            self.frame.button_pressed(self.pins, self.full_level)

class FourWayLight:
    def __init__(self, frame, row, col, light_switch, **kwargs ):

        self.frame = frame
        self.instance = row*col
        self.off_level = int(light_switch['off_setting'])
        self.low_level = int(light_switch['low_setting'])
        self.med_level = int(light_switch['medium_setting'])
        self.full_level = int(light_switch['full_setting'])
        self.pins = light_switch['pins'].split(',')

        self.state = 'off'
        self.direction = 'up'

        col = col
        self.off_button = ttk.Button(frame, text='OFF', style='LightsOff.TButton', command=self.off_button_pressed)
        self.off_button.grid(row=row, column=col, sticky=('W'),pady=3)

        col += 1
        self.on_button = ttk.Button(frame, text='ON', style='LightsReady.TButton', command=self.on_button_pressed)
        self.on_button.grid(row=row, column=col, sticky=('W'), pady=3)

        col += 1
        label = ttk.Label(frame, text=light_switch['text'],
                  style='DarkGray.TLabel',
                  anchor=tk.W)
        label.grid(row=row, column=col, sticky=('W'), padx=6)

    def off_button_pressed(self):
        if self.state != 'off':
            self.state = 'off'
            self.direction = 'up'
            self.off_button.config(style='LightsOff.TButton', text='OFF')
            self.on_button.config(style='LightsReady.TButton', text='ON')

            self.frame.button_pressed(self.pins, self.off_level)

    def on_button_pressed(self):
        if self.state == 'off':
            self.state = 'low'
            self.on_button.config(style='LightsOnLow.TButton', text='LOW')
            self.off_button.config(style='LightsReady.TButton', text='OFF')
            self.frame.button_pressed(self.pins, self.low_level)
        elif self.state == 'low':
            self.direction = 'up'
            self.state = 'medium'
            self.on_button.config(style='LightsOnMed.TButton', text='MED')
            self.frame.button_pressed(self.pins, self.med_level)
        elif self.state == 'medium':
            if self.direction == 'up':
                self.state = 'high'
                self.on_button.config(style='LightsOnFull.TButton', text='FULL')
                self.frame.button_pressed(self.pins, self.full_level)
            else:
                self.state = 'low'
                self.on_button.config(style='LightsOnLow.TButton', text='LOW')
                self.frame.button_pressed(self.pins, self.low_level)
        elif self.state == 'high':
            self.state = 'medium'
            self.direction = 'down'
            self.on_button.config(style='LightsOnMed.TButton', text='MED')
            self.frame.button_pressed(self.pins, self.med_level)

class SliderLight:
    def __init__(self,frame, row, col, light_switch, **kwargs ):

        self.frame = frame
        self.instance = row*col
        self.off_level = int(light_switch['off_setting'])
        self.low_level = int(light_switch['low_setting'])
        self.med_level = int(light_switch['medium_setting'])
        self.full_level = int(light_switch['full_setting'])
        self.pins = light_switch['pins'].split(',')

        col = col
        self.level = ttk.Scale(frame,
                               value=0,
                               from_=0,
                               to=100,
                               style='LightsOff.Horizontal.TScale',
                               orient=tk.HORIZONTAL,
                               command=self.scale_updated)
        self.level.grid(row=row, column=col, columnspan=2, sticky=("NSEW"), pady=3)

        col += 2
        label = ttk.Label(frame, text=light_switch['text'],
                          style='DarkGray.TLabel',
                          anchor=tk.W)
        label.grid(row=row, column=col, sticky=('W'), padx=6)

    def scale_updated(self, event):
        new_level = int(self.level.get())
        if new_level <= self.off_level:
            self.level.config(style='LightsOff.Horizontal.TScale')
            self.frame.button_pressed(self.pins, new_level)
        elif new_level <= self.low_level:
            self.level.config(style='LightsLow.Horizontal.TScale')
            self.frame.button_pressed(self.pins, new_level)
        elif new_level <= self.med_level:
            self.level.config(style='LightsMed.Horizontal.TScale')
            self.frame.button_pressed(self.pins, new_level)
        else:
            self.level.config(style='LightsFull.Horizontal.TScale')
            self.frame.button_pressed(self.pins, new_level)

    def on_button_pressed(self):
        """This is activated when the ALL ON button is pressed"""
        current_level = int(self.level.get())
        if current_level <= self.off_level:
            self.level.set(self.low_level)
        elif current_level <= self.low_level:
            self.level.set(self.med_level)
        elif current_level <= self.med_level:
            self.level.set(self.full_level)
        self.scale_updated(0)

    def off_button_pressed(self):
            """This is activated when the ALL OFF button is pressed"""
            self.level.set(0)
            self.scale_updated(0)


class AllLightsButton:
    def __init__(self, frame, row, col, switch_objects, **kwargs ):

        self.frame = frame
        self.instance = row*col
        self.switch_objects = switch_objects

        self.state = 'off'

        col = col
        self.off_button = ttk.Button(frame, text='OFF', style='LightsOff.TButton', command=self.off_button_pressed)
        self.off_button.grid(row=row, column=col, sticky=('W'), pady=3)

        col +=1
        self.on_button = ttk.Button(frame, text='ON', style='LightsReady.TButton', command=self.on_button_pressed)
        self.on_button.grid(row=row, column=col, sticky=('W'), pady=3)

        col += 1
        label = ttk.Label(frame, text="All Lights",
                  style='DarkGray.TLabel',
                  width=30,
                  anchor=tk.W)
        label.grid(row=row, column=col, sticky=('W'), padx=6)

    def off_button_pressed(self):
        #if self.state == 'on':
        #    self.state = 'off'
        self.off_button.config(style='LightsOff.TButton')
        self.on_button.config(style='LightsReady.TButton')

        for object in self.switch_objects:
            object.off_button_pressed()
            # avoid overrunning buffers in the board controller
            sleep(.004)


    def on_button_pressed(self):
        #if self.state == 'off':
        #    self.state = 'on'
        self.off_button.config(style='LightsReady.TButton')
        self.on_button.config(style='LightsOnFull.TButton', text='ON')

        for object in self.switch_objects:
            object.on_button_pressed()
            # avoid overrunning buffers in the board controller
            sleep(.004)
