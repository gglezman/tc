#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
# This file contains classes that are used by the train control python script.
# They implement the GUI to the Throttle mechanism.
#

import tkinter as tk
import tkinter.ttk as ttk
import threading
import tc_constants as tcc
# import tc_styles
from time import sleep

throttle_a_instance = 0
throttle_b_instance = 1

class ThrottleTab(ttk.Frame):
    def __init__(self, master, i2c_comm, **kwargs):
        """Throttle Frame contains Throttles for 2 locomotive

        :param master: Notebook holding the Throttle frame
        :param i2c_comm - I2C_Comm object
        :param kwargs:
        """
        self.i2c_comm = i2c_comm

        ttk.Frame.__init__(self, master, style='DarkGray.TFrame', **kwargs)
        self.throttle_A = Throttle(self, 'Locomotive A', throttle_a_instance)
        self.throttle_A.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.throttle_B = Throttle(self, 'Locomotive B', throttle_b_instance)
        self.throttle_B.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        # the following ensure equal split of the frame
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        self.grid_rowconfigure(0, weight=1)

    def update_inventory(self, inventory):
        for entry in inventory:
            if entry['boardType'] == tcc.BOARD_TYPE_THROTTLE:
                self.throttle_A.set_i2c_address(entry['i2cAddress'])
                self.throttle_B.set_i2c_address(entry['i2cAddress'])

    def shutDown(self):
        self.throttle_A.shutDown()
        self.throttle_B.shutDown()


class Throttle(ttk.Frame):
    def __init__(self, throttle_tab, title, throttle_instance, **kwargs):
        """

        :param throttle_tab:
        :param title:
        """
        self.parent = throttle_tab
        self.throttle_address = 0
        self.throttle_instance = throttle_instance

        ttk.Frame.__init__(self, throttle_tab,
                           style='MediumGray.TFrame',
                           **kwargs)
        # Title Label
        self.label = ttk.Label(self, text=title, anchor='center',
                               font=("TkDefaultFont", tcc.extra_large, "bold"),
                               style='MediumGray.TLabel',
                               padding=tcc.title_padding)
        self.label.grid(sticky='nswe', row=0, column=0, columnspan=3)

        # Power Control Slider
        self.power_control = ScaledSlider(self, ' Power Control')
        self.power_control.grid(row=1, column=0, rowspan=40, sticky='nsew')

        # Button Panel
        self.button_panel = ButtonPanel(self)
        self.button_panel.grid(row=1, column=1, sticky='nwe')

        # Speedometer Slider
        self.speedometer = ScaledSlider(self, '   Train Speed', tracking_only=True)
        self.speedometer.grid(row=1, column=2, rowspan=40, sticky='nsew')

        # the following ensure equal split of the frame
        self.grid_columnconfigure(0, weight=1, uniform="group2")
        self.grid_columnconfigure(1, weight=1, uniform="group2")
        self.grid_columnconfigure(2, weight=1, uniform="group2")

    def set_i2c_address(self, adr):
        self.throttle_address = adr

        # Configure the board
        self.power_state('off')
        self.power_level(0)
        self.set_direction('forward')
        self.set_momentum('off')

        self.start_daemon();

    def start_daemon(self):
        """This daemon will collect speed information from the throttle board."""
        x = threading.Thread(target=self.poll_speed, daemon=True)
        x.start()

    def poll_speed(self):
        """This function regularly polls the board for current speed setting.

        Note that internally we use 0-200 but the scale slider uses 0-100, hence the divide by 2."""

        speed_reg = tcc.I2C_REG_DT_SPEED + (tcc.DT_THROTTLE_ALLOCATION * self.throttle_instance)
        while (1):
            sleep(0.1)
            reg, speed = self.parent.i2c_comm.read_register(self.throttle_address, speed_reg, tcc.I2C_REG_ID_LEN + tcc.I2C_DT_SPEED_LEN)
            if reg > 0:
                self.speed_setting(speed[0]/2)

    def speed_setting(self, value):
        """Speed setting has changed. This change was reported by poll_speed() running on a different thread.

        :param value: current value (0-100)
        :return: None
        """
        self.speedometer.set_reading(value)

    def power_state(self, state):
        """Power state of Throttle has changed. The user pressed the button

        :param state: 'on'/'off'
        :return: None
        """
        power_status_reg = tcc.I2C_REG_DT_POWER_STATUS + (tcc.DT_THROTTLE_ALLOCATION * self.throttle_instance)

        if state == 'on':
            self.power_control.config_scale('active')
            self.speedometer.config_scale('active')

            self.parent.i2c_comm.write_register_verify(self.throttle_address, power_status_reg, [tcc.POWER_ENABLED])
        else:
            self.power_control.config_scale('disabled')
            self.speedometer.config_scale('disabled')

            self.parent.i2c_comm.write_register_verify(self.throttle_address, power_status_reg, [tcc.POWER_DISABLED])

    def power_level(self, new_power_level):
        """User has changed the power level. Send it to the board

        Note that the range from the scale is 0-100 but internally, we use 0-200.
        """
        power_level_reg = tcc.I2C_REG_DT_POWER_LEVEL + (tcc.DT_THROTTLE_ALLOCATION * self.throttle_instance)

        self.parent.i2c_comm.write_register_verify(self.throttle_address, power_level_reg, [new_power_level])

    def set_direction(self, new_direction):
        """User has pressed the direction button. Send it to the throttle board.

        :param new_direction: 'forward'/'reverse'
        :return: None
        """
        direction_reg = tcc.I2C_REG_DT_DIRECTION + (tcc.DT_THROTTLE_ALLOCATION * self.throttle_instance)

        if new_direction == 'forward':
            self.parent.i2c_comm.write_register_verify(self.throttle_address, direction_reg, [tcc.DIR_FORWARD])
        else:
            self.parent.i2c_comm.write_register_verify(self.throttle_address, direction_reg, [tcc.DIR_REVERSE])

    def set_momentum(self, new_momentum):
        """User has pressed the momentum button. Send it to the throttle board

        :param new_momentun: 'on'/off'
        :return: None
        """
        momentum_reg = tcc.I2C_REG_DT_MOMENTUM + (tcc.DT_THROTTLE_ALLOCATION * self.throttle_instance)

        if new_momentum == 'on':
            self.parent.i2c_comm.write_register_verify(self.throttle_address, momentum_reg, [tcc.MOMENTUM_ENABLED])
        else:
            self.parent.i2c_comm.write_register_verify(self.throttle_address, momentum_reg, [tcc.MOMENTUM_DISABLED])

    def execute_stop(self):
        # update the power control so it doesn't jack the power back up
        self.power_control.set_scale(0)

        emergency_stop_reg = tcc.I2C_REG_DT_EMERGENCY_STOP + (tcc.DT_THROTTLE_ALLOCATION * self.throttle_instance)

        self.parent.i2c_comm.write_register_verify(self.throttle_address, emergency_stop_reg, [tcc.STOP_ACTIVATED])

    def shutDown(self):
        self.power_state('off')

class ButtonPanel(ttk.Frame):
    def __init__(self, throttle_frame, **kwargs):
        """Panel to hold control buttons (power, direction, momentum)

        :param throttle_frame:
        :param kwargs:
        """
        ttk.Frame.__init__(self, throttle_frame,
                           style='MediumGray.TFrame',
                           **kwargs)
        self.throttle_frame = throttle_frame
        self.power_on = False
        self.momentum = 'disabled'     # disabled, on, off
        self.direction = 'forward'     # disabled, on, off

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
        self.momentum_but = ttk.Button(self, command=self.momentum_but_pressed)
        self.config_momentum('disabled')
        self.momentum_but.grid(row=row, column=col)
        row += 1

        # Spacer
        ttk.Label(self, text="", width=18, style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1

        # Button - direction
        ttk.Label(self, text="Direction", style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1
        self.direction_but = ttk.Button(self, command=self.direction_but_pressed)
        self.config_direction('disabled')
        self.direction_but.grid(row=row, column=col)
        row += 1

        # Spacer - Todo - clean this up
        ttk.Label(self, text="", width=18, style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1
        ttk.Label(self, text="", width=18, style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1
        ttk.Label(self, text="", width=18, style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1
        ttk.Label(self, text="", width=18, style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1
        ttk.Label(self, text="", width=18, style='MediumGray.TLabel').grid(row=row, column=col)
        row += 1

        # Button - Stop Sign
        self.stop_button = ttk.Button(self, command=self.stop_but_pressed)
        self.stop_button.image = tk.PhotoImage(file=tcc.stop_sign_file)
        self.stop_button["image"] = self.stop_button.image
        self.config_stop('disabled')
        self.stop_button.grid(row=row, column=col)


    def master_power_but_pressed(self):
        if self.power_on:
            self.power_on = False
            self.config_master_power('off')
            self.config_momentum('disabled')
            self.config_direction('disabled')
            # tell Throttle the power is off
            self.throttle_frame.power_state('off')
        else:
            self.power_on = True
            self.config_master_power('on')
            self.config_momentum('off')
            self.config_direction('forward')
            # Tell Throttle the power is on
            self.throttle_frame.power_state('on')

    def config_master_power(self, state):
        if state == 'on':
            self.master_power_but.config(style='Red.TButton')
            self.master_power_but.config(text='ON')
        else:
            self.master_power_but.config(style='Yellow.TButton')
            self.master_power_but.config(text='OFF')

    def momentum_but_pressed(self):
        if self.power_on:
            if self.momentum == 'on':
                self.config_momentum('off')
            else:
                self.config_momentum('on')

            self.throttle_frame.set_momentum(self.momentum )

    def config_momentum(self, new_momentum):
        """States are : disabled, on, off"""
        self.momentum = new_momentum
        if self.momentum == 'disabled':
            self.momentum_but.config(style='Gray.TButton')
            self.momentum_but.config(text='OFF')
            self.momentum_but.config(state='disabled')
        elif self.momentum == 'on':
            self.momentum_but.config(style='Red.TButton')
            self.momentum_but.config(text='ON')
            self.momentum_but.config(state='normal')
        else:
            self.momentum_but.config(style='LimeGreen.TButton')
            self.momentum_but.config(text='OFF')
            self.momentum_but.config(state='normal')

    def direction_but_pressed(self):
        """User has pressed the direction button
        :return:
        """
        if self.power_on:
            if self.direction == 'forward':
                self.config_direction('reverse')
            else:
                self.config_direction('forward')

            self.throttle_frame.set_direction(self.direction )

    def config_direction(self, new_direction):
        """States are : disabled, forward, reverse"""
        self.direction = new_direction

        if self.direction== 'disabled':
            self.direction_but.config(style='Gray.TButton')
            self.direction_but.config(text='FWD')
            self.direction_but.config(state='disabled')
        elif self.direction == 'forward':
            self.direction_but.config(style='Wheat1.TButton')
            self.direction_but.config(text='FWD')
            self.direction_but.config(state='normal')
        else:
            self.direction_but.config(style='Wheat3.TButton')
            self.direction_but.config(text='REV')
            self.direction_but.config(state='normal')

    def stop_but_pressed(self):
        self.throttle_frame.execute_stop()

    def config_stop(self, state):
        """Stop button states are 'enabled' and 'disabled'

        Todo - try to make the image look diffent when disabled
        """
        pass

class ScaledSlider(ttk.Frame):
    def __init__(self, throttle_frame, title, tracking_only=False, **kwargs):
        """ Calibrated slider

        :param throttle: frame to place the slider in
        :param title:  Title over slider
        :param tracking_only: user can not move this slider
        :param kwargs:

        The frame is padded to give a background to the labels/slider
        """
        ttk.Frame.__init__(self,
                           throttle_frame,
                           style='Disabled.TFrame',
                           # padding=('1m','2m','3m','1m'),
                           **kwargs)
        self.throttle_frame = throttle_frame
        self.tracking_only = tracking_only
        self.scale_value = tk.DoubleVar(self)

        row = 0
        self.title = ttk.Label(self,
                               text=title,
                               font=("TkDefaultFont", tcc.large_text, "bold"),
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

    def set_scale(self, new_setting):
        """Used to force the scale value"""
        self.scale.set(new_setting)

    def scale_updated(self, event):
        """User has moved slider. Get the value and send it up.

        Note that the scale slider uses 0-100 but internally we use 0-200

        :param event:
        :return:
        """
        self.throttle_frame.power_level(int(self.scale.get()*2))

    def set_reading(self, value):
        """Used to set current value for tracking_only

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
