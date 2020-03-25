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
import tc_styles


class ThrottleTab(ttk.Frame):
    def __init__(self, master, **kwargs):
        """Throttle Frame contains Throttles for 2 locomotive

        :param master: Notebook holding the Throttle frame
        :param kwargs:
        """
        ttk.Frame.__init__(self, master, style='DarkGray.TFrame', **kwargs)
        self.throttle_A = Throttle(self, 'Locomotive A')
        self.throttle_A.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.throttle_B = Throttle(self, 'Locomotive B')
        self.throttle_B.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        # the following ensure equal split of the frame
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        self.grid_rowconfigure(0, weight=1)


class Throttle(ttk.Frame):
    def __init__(self, throttle_tab, title, **kwargs):
        """

        :param throttle_tab:
        :param title:
        """
        ttk.Frame.__init__(self, throttle_tab,
                           style='MediumGray.TFrame',
                           **kwargs)

        # Title Label
        self.label = ttk.Label(self, text=title, anchor='center',
                               font=("TkDefaultFont", tcc.large_text, "bold"),
                               style='MediumGray.TLabel',
                               padding=tcc.title_padding)
        self.label.grid(sticky='nswe', row=0, column=0, columnspan=3)

        # Power Control Slider
        self.power_control = ScaledSlider(self, 'Power Control')
        self.power_control.grid(row=1, column=0, rowspan=40, sticky='nsew')

        # Button Panel
        self.button_panel = ButtonPanel(self, self)   # fixme3 self, self ?
        self.button_panel.grid(row=1, column=1, sticky='nwe')

        # Speedometer Slider
        self.speedometer = ScaledSlider(self, '   Train Speed', tracking_only=True)
        self.speedometer.grid(row=1, column=2, rowspan=40, sticky='nsew')

        # the following ensure equal split of the frame
        self.grid_columnconfigure(0, weight=1, uniform="group2")
        self.grid_columnconfigure(1, weight=1, uniform="group2")
        self.grid_columnconfigure(2, weight=1, uniform="group2")

    def power_setting(self, value):
        """Power setting gets reported by power control

        :param value: current value
        :return: None
        """
        self.speedometer.set_reading(value)  # fixme - remove and send

    def power_state(self, state):
        """Power state of Throttle has changed

        :param state: on/off
        :return:
        """
        if state == 'on':
            self.power_control.config_scale('active')
            self.speedometer.config_scale('active')
        else:
            self.power_control.config_scale('disabled')
            self.speedometer.config_scale('disabled')


class ButtonPanel(ttk.Frame):
    def __init__(self, parent, locomotive_frame, **kwargs):
        """Panel to hold control buttons (power, direction, momentum)

        :param parent: invoking object (ie Throttle class)
        :param locomotive_frame:
        :param kwargs:
        """
        ttk.Frame.__init__(self, locomotive_frame,
                           style='MediumGray.TFrame',
                           **kwargs)
        self.parent = parent
        self.power_on = False
        self.momentum = False
        self.direction = 'forward'     # or reverse

        col = 0
        row = 0
        # Spacer
        ttk.Label(self, text="", width=18, style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1

        ttk.Label(self, text="Master Power",
                  style='MediumGray.TLabel',
                  anchor=tk.CENTER,
                  width=18).grid(row=row, column=col)
        row += 1
        self.master_power_but = ttk.Button(self,
                                           text="ON",
                                           style='Yellow.TButton',
                                           command=self.master_power_but_pressed)
        self.config_master_power('off')
        self.master_power_but.grid(row=row, column=col)
        row += 1

        # Spacer
        ttk.Label(self, text="", width=18, style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1

        # Button - Momentum
        ttk.Label(self, text="Momentum", style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1
        self.momentum_but = ttk.Button(self,
                                       command=self.momentum_but_pressed)
        self.config_momentum('disabled')
        self.momentum_but.grid(row=row, column=col)
        row += 1

        # Spacer
        ttk.Label(self, text="", width=18, style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1

        # Button - direction
        ttk.Label(self, text="Direction", style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1
        self.direction_but = ttk.Button(self,
                                        command=self.direction_but_pressed)
        self.config_direction('disabled')
        self.direction_but.grid(row=row, column=col)

    def master_power_but_pressed(self):
        if self.power_on:
            self.power_on = False
            self.config_master_power('off')
            self.config_momentum('disabled')
            self.config_direction('disabled')
            # tell Throttle the power is off
            self.parent.power_state('off')
        else:
            self.power_on = True
            self.config_master_power('on')
            self.config_momentum('off')
            self.config_direction('forward')
            # Tell Throttle the power is on
            self.parent.power_state('on')

    def config_master_power(self, state):
        if state == 'on':
            self.master_power_but.config(style='Red.TButton')
            self.master_power_but.config(text='ON')
        else:
            self.master_power_but.config(style='Yellow.TButton')
            self.master_power_but.config(text='OFF')

    def momentum_but_pressed(self):
        if self.power_on:
            if self.momentum:
                self.config_momentum('off')
            else:
                self.config_momentum('on')

    def config_momentum(self, state):
        """States are : disabled, on, off"""
        if state == 'disabled':
            self.momentum = False
            self.momentum_but.config(style='Gray.TButton')
            self.momentum_but.config(text='OFF')
            self.momentum_but.config(state='disabled')
        elif state == 'on':
            self.momentum = True
            self.momentum_but.config(style='Red.TButton')
            self.momentum_but.config(text='ON')
            self.momentum_but.config(state='normal')
        else:
            self.momentum = False
            self.momentum_but.config(style='LimeGreen.TButton')
            self.momentum_but.config(text='OFF')
            self.momentum_but.config(state='normal')

    def direction_but_pressed(self):
        """

        :return:
        """
        if self.power_on:
            if self.direction == 'forward':
                self.config_direction('reverse')
            else:
                self.config_direction('forward')

    def config_direction(self, state):
        """States are : disabled, forward, reverse"""
        if state == 'disabled':
            self.direction = 'forward'
            self.direction_but.config(style='Gray.TButton')
            self.direction_but.config(text='FWD')
            self.direction_but.config(state='disabled')
        elif state == 'forward':
            self.direction = 'forward'
            self.direction_but.config(style='Wheat1.TButton')
            self.direction_but.config(text='FWD')
            self.direction_but.config(state='normal')
        else:
            self.direction = 'reverse'
            self.direction_but.config(style='Wheat3.TButton')
            self.direction_but.config(text='REV')
            self.direction_but.config(state='normal')


class ScaledSlider(ttk.Frame):
    def __init__(self, master, title, tracking_only=False, **kwargs):
        """ Calibrated slider

        :param master: Locomotive Frame
        :param title:  Title over slider
        :param tracking_only: user can not move this slider
        :param kwargs:

        The frame is padded to give a background to the labels/slider
        """
        ttk.Frame.__init__(self,
                           master,
                           style='Disabled.TFrame',
                           # padding=('1m','2m','3m','1m'),
                           **kwargs)
        self.master = master
        self.tracking_only = tracking_only
        self.scale_value = tk.DoubleVar(self)

        row = 0
        self.title = ttk.Label(self,
                               text=title,
                               font=("TkDefaultFont", tcc.med_large_text, "bold"),
                               padding=('1m', '1m', '1m', '3m'))  # below text
        self.title.grid(row=row, column=0, columnspan=2)
        row += 1

        #  Scale
        self.labels = []
        for i in range(11):
            label = ttk.Label(self, text=str((10 - i) * 10) + ' -',
                              padding=(8, 3, 10))
            label.grid(row=i + 2 + row, column=0, stick='e')
            self.labels.append(label)

        self.scale = ttk.Scale(self,
                               from_=100,
                               to=0,
                               orient=tk.VERTICAL,
                               value=0,
                               length=int(tcc.SCREEN_HEIGHT*tcc.slider_proportion),
                               style='Tc.Vertical.TScale',
                               variable=self.scale_value
                               )
        self.config_scale('disabled')
        if not self.tracking_only:
            self.scale.config(command=self.scale_updated)

        self.scale.grid(row=row+2, column=1, rowspan=11)

    def scale_updated(self, event):
        """User has moved slider

        :param event:
        :return:
        """
        self.master.power_setting(self.scale.get())

    def set_reading(self, value):
        """USed to set current value for tracking_only

        :param value:
        :return:
        """
        if self.tracking_only:
            self.scale.state(['!disabled'])
            self.scale.set(value)
            self.scale.state(['disabled'])

    def config_scale(self, state):
        """States: active, disabled

        For some reason config(state='') doesn't work on Scale!!!!!

        """
        if state == 'active':
            self.config(style='Active.TFrame')
            if self.tracking_only:
                self.scale.state(['readonly'])
            else:
                self.scale.state(['!disabled'])
            self.title.config(style='Active.TLabel')
            for label in self.labels:
                label.config(style='Active.TLabel')

        else:
            self.config(style='Disabled.TFrame')
            # set the value before disabling
            self.scale.set(0)
            self.scale.state(['disabled'])
            self.title.config(style='Disabled.TLabel')
            for label in self.labels:
                label.config(style='Disabled.TLabel')
