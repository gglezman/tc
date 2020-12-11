
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
import math as m
import tc_constants as tcc
import tc_styles as styles

class SwitchesTab(ttk.Frame):
    def __init__(self, master, i2c_comm, **kwargs):
        """Lights frame contains the light controls

        :param master: Notebook holding the Throttle frame
        :param i2c_comm - I2C_Comm object
        :param kwargs:
        """
        ttk.Frame.__init__(self, master, style='DarkGray.TFrame', **kwargs)

        self.i2c_comm = i2c_comm
        ###########################################################
        # Controls for the switches.
        # Each switch contained in the layout will be assigned
        # control buttons and have its name displayed.
        # Each entry in the list contains the following
        # sw              :  switch data from layout
        # mainline_butt   :  button to through switch to through
        # diversion_butt  :  button to move switch to diverting route
        # position        : thru / divert
        # name_butt       : button containing switch name
        # identify        : off/on - highlight switch
        #
        # This list is generated when the button frame is constructed
        ###########################################################
        self.switch_controls = []

        # Add the layout to the frame
        self.layout = self.add_layout_frame(self)

        # add the buttons to control the switches
        self.add_button_frame(self, self.switch_controls, self.layout.switch_list)

        # place all the switches in the mainline position
        for switch in self.layout.switch_list:
            self.configure_layout(switch, 'thru')

        self.pack()

    def update_inventory(self):
        pass

    def add_button_frame(self,top_frame, switch_controls, switch_list):
        frame = ttk.Frame(top_frame, style='DarkGray.TFrame')

        switch_count = len(switch_list)
        col = 0
        for switch in switch_list:
            switch_control = {'sw':switch, 'position':'thru'}
            col += 1
            row = 0
            mainline_button = ttk.Button(frame, text='MAINLINE', style='ThruActive.TButton')
            mainline_button.grid(row=row, column=col, padx=20, sticky='EW')
            switch_control['mainline_butt'] = mainline_button
            row += 1
            divert_button = ttk.Button(frame, text='DIVERSON', style='DivertInactive.TButton')
            divert_button.grid(row=row, column=col, padx=20, sticky='EW')
            switch_control['divert_butt'] = divert_button
            row += 1
            name_button = ttk.Button(frame, text=switch['name'], style='Name.TButton')
            name_button.grid(row=row, column=col, padx=20, sticky='EW')
            switch_control['name_butt'] = name_button
            switch_control['identify'] = 'off'

            mainline_button.config(command=lambda sw_ctrl=switch_control: self.mainline_button_pressed(sw_ctrl))
            divert_button.config(command=lambda sw_ctrl=switch_control: self.divert_button_pressed(sw_ctrl))
            name_button.config(command=lambda sw_ctrl=switch_control: self.identify_button_pressed(sw_ctrl))

        switch_controls.append(switch_control)
        frame.pack()

    def mainline_button_pressed(self, sw_ctrl):
        """
        note we don't test current position. This button will also switch from identify to thru
        """
        # Position
        sw_ctrl['position'] = 'thru'
        # Buttons
        sw_ctrl['mainline_butt'].config(style='ThruActive.TButton')
        sw_ctrl['divert_butt'].config(style='DivertInactive.TButton')
        # Layout
        self.configure_layout(sw_ctrl['sw'], sw_ctrl['position'])
        # Physical Switch - configure the switch - on the track via i2c

        # clean up the identify/name button
        if sw_ctrl['identify'] == 'on':
            self.reset_identify_button(sw_ctrl)

    def divert_button_pressed(self, sw_ctrl):
        """
        note we don't test current position. This button will also switch from identify to thru
        """
        # Position
        sw_ctrl['position'] = 'divert'
        # Buttons
        sw_ctrl['mainline_butt'].config(style='ThruInactive.TButton')
        sw_ctrl['divert_butt'].config(style='DivertActive.TButton')
        # Layout
        self.configure_layout(sw_ctrl['sw'], sw_ctrl['position'])
        # Physical Switch

        # clean up the identify/name button
        if sw_ctrl['identify'] == 'on':
            self.reset_identify_button(sw_ctrl)

    def reset_identify_button(self, sw_ctrl):
            sw_ctrl['identify'] = 'off'
            sw_ctrl['name_butt'].config(style='Name.TButton')

    def configure_layout(self, switch, position):
        print(switch)
        print(position)
        if position == 'thru':
            self.layout.canvas.itemconfig(switch['div_obj'], fill=styles.TRACK_COLOR)
            self.layout.canvas.itemconfig(switch['entry_obj'], fill=styles.THRU_ACTIVE_COLOR)
            self.layout.canvas.itemconfig(switch['thru_obj'], fill=styles.THRU_ACTIVE_COLOR)
            self.layout.canvas.lift(switch['thru_obj'])
            self.layout.canvas.lift(switch['entry_obj'])
        elif position == 'divert':
            self.layout.canvas.itemconfig(switch['thru_obj'], fill=styles.TRACK_COLOR)
            self.layout.canvas.itemconfig(switch['entry_obj'], fill=styles.DIV_ACTIVE_COLOR)
            self.layout.canvas.itemconfig(switch['div_obj'], fill=styles.DIV_ACTIVE_COLOR)
            self.layout.canvas.lift(switch['div_obj'])
            self.layout.canvas.lift(switch['entry_obj'])
        else:   # must be 'identify'
            self.layout.canvas.itemconfig(switch['entry_obj'], fill=styles.TRACK_IDENTIFY_COLOR)
            self.layout.canvas.itemconfig(switch['div_obj'], fill=styles.TRACK_IDENTIFY_COLOR)
            self.layout.canvas.itemconfig(switch['thru_obj'], fill=styles.TRACK_IDENTIFY_COLOR)

    def identify_button_pressed(self, sw_ctrl):
        switch = sw_ctrl['sw']
        if sw_ctrl['identify'] == 'on':
            sw_ctrl['identify'] = 'off'
            self.configure_layout(sw_ctrl['sw'],sw_ctrl['position'])
            sw_ctrl['name_butt'].config(style='Name.TButton')
        else:
            sw_ctrl['identify'] = 'on'
            self.configure_layout(sw_ctrl['sw'], 'identify')
            sw_ctrl['name_butt'].config(style='NameActive.TButton')

    def add_layout_frame(self, frame):
        """This is the Nantahala Layout
        """
        layout = TrackLayout(frame, 700, 550, thickness=12)

        # set the starting location
        layout.set_location(920, 500, 0)
        layout.set_scale_factor(11)
        layout.add_arc(18, 66+48.6+25.3+34.7+15.4)
        layout.add_arc(134.8, 3.2)
        layout.add_arc(21, 12.6)
        layout.add_arc(37.8, 19.2)
        layout.add_line(1.4)
        layout.add_line(2)  # this is the 577 90 deg crossover
        layout.add_arc(60.9, 5.2)
        layout.add_line(2.6 + 6.9 + 6.1)
        layout.add_arc(24, 9.9, dir='cw')
        layout.add_arc(18, 15.4, dir='cw')
        layout.add_arc(18, 114.6, dir='cw')
        layout.add_arc(31.9, 10, dir='cw')
        layout.add_line(8.7)
        layout.add_arc(13.8, 18.1 + 28.1 + 23.5, dir='cw')
        layout.add_arc(36.5, 16.6, dir='cw')
        layout.add_turnout('North West Siding', 6, 'R', connection='mainline')
        layout.add_arc(83.8, 4.7, dir='cw')
        layout.add_arc(16.5, 11.3)
        layout.add_arc(16.2, 10.2)
        layout.add_line(3.4 + 4.1)
        layout.add_arc(25.1, 10.8, dir='cw')
        layout.add_line(2.1)
        layout.add_turnout('North East Siding', 6, 'L', connection='through')
        layout.add_arc(18, 90, dir='cw')
        layout.add_arc(20, 135, dir='cw')
        layout.add_line(16)
        layout.add_line(2)  # this is the 577 90 deg crossover
        layout.add_line(1.9)
        layout.add_arc(97.3, 8)
        layout.add_arc(18, 30 + 30 + 21.2 + 24.6)
        layout.add_arc(15.8, 104)  # was 94.6
        layout.add_turnout('Station', 6, 'L', connection='mainline')
        layout.add_arc(13.4, 21., dir='cw')  # was 13.8,22.1
        layout.add_arc(13.4, 28.)  # was 13.8,30
        layout.add_line(19.8)  # was 18.7
        layout.add_turnout('Mainline Access', 6, 'R', connection='through')

        # Add the sidings
        switch = layout.get_switch('North West Siding')
        layout.set_location(switch['div_x'], switch['div_y'], switch['div_heading'])
        print(switch)
        print("({}, {}) heading {})".format(switch['div_x'], 0, 0))
        print( "({}, {}) heading {})".format(0, switch['div_y'], 0))
        print( "({}, {}) heading {})".format(0,0, switch['div_heading']))
        layout.add_arc(86.1, 5.2, dir='cw')
        layout.add_arc(13.8, 24.3)
        layout.add_arc(27, 13.2)
        layout.add_arc(87.1, 7.3, dir='cw')
        layout.add_line(1)  # hack

        switch = layout.get_switch('Station')
        layout.set_location(switch['div_x'], switch['div_y'], switch['div_heading'])
        layout.add_turnout('Yard Siding', 4, 'L', connection='mainline')
        layout.add_arc(20.4, 5, dir='cw')
        layout.add_turnout('Boro Siding', 4, 'R', connection='through')
        layout.add_turnout('Station Exit', 6, 'R', connection='mainline')
        layout.add_arc(135.5, 4.8, dir='cw')
        layout.add_arc(16.2, 36)

        switch = layout.get_switch('Station Exit')
        layout.set_location(switch['div_x'], switch['div_y'], switch['div_heading'])
        layout.add_arc(8, 18, dir='cw')
        layout.add_arc(8, 15, )

        switch = layout.get_switch('Yard Siding')
        layout.set_location(switch['div_x'], switch['div_y'], switch['div_heading'])
        layout.add_line(3)
        layout.add_arc(12, 30)
        layout.add_arc(8, 50, dir='cw')

        switch = layout.get_switch('Boro Siding')
        layout.set_location(switch['div_x'], switch['div_y'], switch['div_heading'])
        layout.add_line(3)
        layout.add_arc(14.6, 63.2, dir='cw')
        layout.add_arc(13.8, 35.3)
        layout.add_arc(108, 2.4)
        layout.add_arc(81.6, 14.8)

        #layout.print_switch_list()

        return layout

class TrackLayout(ttk.Frame):
    """Construct a track layout on a canvas in a frame

    w     : width of frame
    h     : height of frame
    """
    def __init__(self, frame, w, h, thickness=7, canvas_bg=styles.ACTIVE_COLOR, bg='tan', **kwargs):

        ttk.Frame.__init__(self, frame, **kwargs)

        self.thickness = thickness

        ##########################################################################
        # List of switches (turnouts) in the layout.  The switch items in the list
        # contain the following:
        # name:         : text string associated with the switch
        # div_x, div_y div_heading  : diversion track x,y and heading (at the outer
        #                             edge as it leaves the switch)
        #  entry_obj    : canvas object at mainline entry of switch
        #  div_obj      : canvas object representing the diversion path
        #  thru_obj     : canvas object representing the through path of the switch
        ##########################################################################
        self.switch_list = []

        ######################################
        # specify the start point and heading
        ######################################
        self.x = 0
        self.y = 0
        self.heading = 0

        self.scale_factor = 1

        ######################################
        # Here is the drawing canvas
        ######################################
        self.canvas = tk.Canvas(self, width=w-10, height=h-10, bg=canvas_bg)
        self.canvas.pack(fill=tk.X)

        self.pack(fill=tk.BOTH)

    def set_location(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading

    def set_scale_factor(self, scale_factor):
        self.scale_factor = scale_factor

    def add_line(self, d, fill='green'):
        print("Line start ({:.2f},{:.2f}), {:.2f} +  {}".format(
            self.x, self.y, self.heading, d))

        # scale the length here so the caller doesn't have to do it n times
        print(" d {} and scale {}".format(d, self.scale_factor))
        d = self.scale_factor * d

        # Calculate new position based on the heading and magnitude of change
        x1 = self.x + d * m.cos(m.radians(self.heading))
        y1 = self.y - d * m.sin(m.radians(self.heading))
        # Add it to the display
        line_obj = self.canvas.create_line(self.x, self.y, x1, y1,
                              fill=fill, width=self.thickness, capstyle='projecting')
        # We have a new position but heading remains the same
        self.x = x1
        self.y = y1
        print("Line done ({:.2f},{:.2f}), {:.2f}".format(
            self.x, self.y, self.heading))
        return line_obj

    def add_arc(self, r, extent, dir='ccw', fill='green'):
        """Add an arc to the given starting (x,y) location and heading.

        Arcs are drawn by specifying the containing box, start angle and extent.

        The arc is always tangent to the heading at the start angle. Therefore
        the start angle is derived from the heading (90 degrees to the heading).

        Given a location, radius and an starting angle, calculate the center
        (cx, cy) of the box containing the arc. Then use the radius to define
        the box.

        self   : use this to extract loation and heading
        r        : radius of arc
        entent   : extent in degress of the arc
        dir      : 'cw' or 'ccw'

        """
        print("Arc start ({:.2f}, {:.2f}), {:.2f}".format(self.x, self.y, self.heading))

        # scale the radius here so the caller doesn't have to do it n times
        r = self.scale_factor * r

        # we can handle turns in and turns out
        if dir == 'ccw':
            start_angle = self.heading - 90
        else:
            start_angle = self.heading + 90
            extent = -extent

        xc = self.x - m.cos(m.radians(start_angle)) * r
        yc = self.y + m.sin(m.radians(start_angle)) * r
        # print("center ({},{})".format(xc,yc))
        x0 = xc - r
        y0 = yc - r
        x1 = xc + r
        y1 = yc + r
        coords = (x0, y0, x1, y1)
        arc_obj = self.canvas.create_arc(coords, start=start_angle, extent=extent,
                             outline=fill, width=self.thickness, style=tk.ARC)

        # new vector
        self.x = xc + m.cos(m.radians(start_angle + extent)) * r
        self.y = yc - m.sin(m.radians(start_angle + extent)) * r
        self.heading += extent
        self.heading %= 360
        print("Arc end ({:.2f},{:.2f}), {:.2f}".format(
         self.x, self.y, self.heading))
        return arc_obj

    def add_turnout(self, name, number, dir, connection='mainline', fill='green'):
        """Add a turnout at the current location.

        self      : drawingt context
        number      : #4 or #6 turnouts are currently supported
        dir         : 'R', 'L'
        connection  : 'mainline', 'through', or 'diversion'

        We also generate a switch object and put it on the swicth list. The switch object is
        use to add the siding track. It includes the name, location, object references to the pieces,...
        """
        print("Turnout start ({:.2f}, {:.2f}), {:.2f}".format(
            self.x, self.y, self.heading))

        self.error_check_turnout(number, dir, connection)

        switch_obj = {'name':name}

        if number == 4:
            entry_len = 3.5  # entry to frog
            thru_len = 5.5  # from frog to exit on through path
            through_len = entry_len + thru_len
            diversion_len = 4.65  # from frog to end of diversion path
            diversion_angle = 14.25

        else:
            entry_len = 3.35  # entry to frog
            thru_len = 8.65  # from frog to exit on through path - was 8.65
            through_len = entry_len + thru_len
            diversion_len = 7  # from frog to end of diversion path - was 6.77
            diversion_angle = 9.53

        if dir == 'R':
            diversion_angle = -diversion_angle

        if connection == 'mainline':
            # add the entry piece
            print(entry_len)
            switch_obj['entry_obj'] = self.add_line(entry_len, fill=fill)

            # save the heading and location
            through_heading = self.heading  # save the heading
            through_x = self.x
            through_y = self.y
            self.heading += diversion_angle

            # add the diversion
            switch_obj['div_obj'] = self.add_line(diversion_len, fill=fill)
            switch_obj['div_x'] = self.x
            switch_obj['div_y'] = self.y
            switch_obj['div_heading'] = self.heading

            # restore the heading and location
            self.heading = through_heading
            self.x = through_x
            self.y = through_y

            # add the exit
            switch_obj['thru_obj'] = self.add_line(thru_len)

        elif connection == 'through':
            # add the thru
            switch_obj['thru_obj'] = self.add_line(thru_len, fill=fill)

            # save the location/heading
            through_heading = self.heading  # save the heading
            through_x = self.x
            through_y = self.y

            # reverse the heading adjust for the diversion angle
            # (reverse becasue the angle is given of mainline entry, not through)
            self.heading += 180 + diversion_angle

            # add the diversion
            switch_obj['div_obj'] = self.add_line(diversion_len)
            switch_obj['div_x'] = self.x
            switch_obj['div_y'] = self.y
            switch_obj['div_heading'] = self.heading

            # restore the heading and add the final section
            self.heading = through_heading
            self.x = through_x
            self.y = through_y

            # add_line(self, entry_len, fill='white')
            switch_obj['entry_obj'] = self.add_line(entry_len, fill=fill)

        print("Turnout end ({:.2f}, {:.2f}), {:.2f}".format(
            self.x, self.y, self.heading))

        self.switch_list.append(switch_obj)
        print(switch_obj)

    def error_check_turnout(self, number, dir, connection):
        if number != 4 and number != 6:
            error
        if connection != 'mainline' and \
            connection != 'through' and \
            connection != 'diversion':
            error
        if dir != 'R' and dir != 'L':
            error

    def get_switch(self, name):
        for switch in self.switch_list:
            if switch['name'] == name:
                return switch
        return None

    def print_switch_list(self):
        for entry in self.switch_list:
            print("{}: divX:{:.2f} divY:{:.2f} divH:{:.2f} entry_o:{} div_o:{} thru_o:{}".format(
                entry['name'],
                entry['div_x'],
                entry['div_y'],
                entry['div_heading'],
                entry['entry_obj'],
                entry['div_obj'],
                entry['thru_obj'],
            ))

