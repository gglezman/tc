
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

class SwitchesTab(ttk.Frame):
    def __init__(self, master, i2c_comm, **kwargs):
        """Lights frame contains the light controls

        :param master: Notebook holding the Throttle frame
        :param i2c_comm - I2C_Comm object
        :param kwargs:
        """
        ttk.Frame.__init__(self, master, style='DarkGray.TFrame', **kwargs)

        self.i2c_comm = i2c_comm

        # Add the layout to the frame

        self.add_layout_frame(self)

        self.add_button_frame(self)

        self.pack()

    def update_inventory(self):
        pass

    def add_button_frame(self,top_frame):
        frame = ttk.Frame(top_frame)
        ttk.Button(frame, text='Button 1').pack()
        ttk.Button(frame, text='Button 2').pack()
        ttk.Button(frame, text='Button 3').pack()
        ttk.Button(frame, text='Button 4').pack()

    def add_layout_frame(self, frame):
        layout = TrackLayout(frame, 700, 550, bg='blue')

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

        layout.add_turnout('sw_1', 6, 'R', connection='mainline')

        layout.add_arc(83.8, 4.7, dir='cw')

        layout.add_arc(16.5, 11.3)

        layout.add_arc(16.2, 10.2)

        layout.add_line(3.4 + 4.1)

        layout.add_arc(25.1, 10.8, dir='cw')

        layout.add_line(2.1)

        layout.add_turnout('sw_2', 6, 'L', connection='through')

        layout.add_arc(18, 90, dir='cw')

        layout.add_arc(20, 135, dir='cw')

        layout.add_line(16)

        layout.add_line(2)  # this is the 577 90 deg crossover

        layout.add_line(1.9)

        layout.add_arc(97.3, 8)

        layout.add_arc(18, 30 + 30 + 21.2 + 24.6)

        layout.add_arc(15.8, 104)  # was 94.6
        
        layout.add_turnout('sw_3', 6, 'L', connection='mainline')

        layout.add_arc(13.4, 21., dir='cw')  # was 13.8,22.1

        layout.add_arc(13.4, 28.)  # was 13.8,30
        # layout.add_arc(23.3, 9.6)
        # layout.add_line(self,2.9)

        # layout.add_arc(20,16.6)

        layout.add_line(19.8)  # was 18.7

        layout.add_turnout('sw_4', 6, 'R', connection='through')

        # add the sidings
        switch = layout.get_switch('sw_1')
        layout.set_location(switch['div_x'], switch['div_y'], switch['div_heading'])
        layout.add_arc(86.1, 5.2, dir='cw')
        layout.add_arc(13.8, 24.3)
        layout.add_arc(27, 13.2)
        layout.add_arc(87.1, 7.3, dir='cw')
        layout.add_line(1)  # hack

        switch = layout.get_switch('sw_3')
        layout.set_location(switch['div_x'], switch['div_y'], switch['div_heading'])
        layout.add_turnout('sw_5', 4, 'L', connection='mainline')
        layout.add_arc(20.4, 5, dir='cw')
        layout.add_turnout('sw_6', 4, 'R', connection='through')
        layout.add_turnout('sw_7', 6, 'R', connection='mainline')
        layout.add_arc(135.5, 4.8, dir='cw')
        layout.add_arc(16.2, 36)

        switch = layout.get_switch('sw_7')
        layout.set_location(switch['div_x'], switch['div_y'], switch['div_heading'])
        layout.add_arc(8, 18, dir='cw')
        layout.add_arc(8, 15, )

        switch = layout.get_switch('sw_5')
        layout.set_location(switch['div_x'], switch['div_y'], switch['div_heading'])
        layout.add_line(3)
        layout.add_arc(12, 30)
        layout.add_arc(8, 50, dir='cw')

        switch = layout.get_switch('sw_6')
        layout.set_location(switch['div_x'], switch['div_y'], switch['div_heading'])
        layout.add_line(3)
        layout.add_arc(14.6, 63.2, dir='cw')
        layout.add_arc(13.8, 35.3)
        layout.add_arc(108, 2.4)
        layout.add_arc(81.6, 14.8)

        layout.print_switch_list()

thickness = 7
class TrackLayout(ttk.Frame):
    """Construct a track layout on a canvas in a frame

    w     : width of frame
    h     : height of frame
    """
    def __init__(self, frame, w, h, thickness=7, bg='tan', **kwargs):

        ttk.Frame.__init__(self, frame, **kwargs)

        self.thickness = thickness

        ###############################################
        # List of switches (turnouts) in the layout
        ###############################################
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
        self.canvas = tk.Canvas(self, width=w-10, height=h-10, bg=bg)
        self.canvas.pack(fill=tk.X)

        self.pack(fill=tk.BOTH)

    def set_location(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading

    def set_scale_factor(self, scale_factor):
        self.scale_factor = scale_factor

    def add_line(self, d, fill='green', width=thickness):
        print("Line start ({:.2f},{:.2f}), {:.2f} +  {}".format(
            self.x, self.y, self.heading, d))

        # scale the length here so the caller doesn't have to do it n times
        print(" d {} and scale {}".format(d, self.scale_factor))
        d = self.scale_factor * d

        # Calculate new position based on the heading and magnitude of change
        x1 = self.x + d * m.cos(m.radians(self.heading))
        y1 = self.y - d * m.sin(m.radians(self.heading))
        # Add it to the display
        self.canvas.create_line(self.x, self.y, x1, y1,
                              fill=fill, width=width)
        # We have a new position but heading remains the same
        self.x = x1
        self.y = y1
        print("Line done ({:.2f},{:.2f}), {:.2f}".format(
            self.x, self.y, self.heading))


    def add_arc(self, r, extent, dir='ccw', fill='green', width=thickness):
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
        self.canvas.create_arc(coords, start=start_angle, extent=extent,
                             outline=fill, width=width, style=tk.ARC)

        # new vector
        self.x = xc + m.cos(m.radians(start_angle + extent)) * r
        self.y = yc - m.sin(m.radians(start_angle + extent)) * r
        self.heading += extent
        self.heading %= 360
        print("Arc end ({:.2f},{:.2f}), {:.2f}".format(
         self.x, self.y, self.heading))


    def add_turnout(self, name, number, dir, connection='mainline', fill='green'):
        """Add a turnout at the current location.

        self      : drawingt context
        number      : #4 or #6 turnouts are currently supported
        dir         : 'R', 'L'
        conenction  : 'mainline', 'through', or 'diversion'

        """
        print("Turnout start ({:.2f}, {:.2f}), {:.2f}".format(
            self.x, self.y, self.heading))

        self.error_check_turnout(number, dir, connection)

        if number == 4:
            entry_len = 3.5  # entry to frog
            trail_len = 5.5  # from frog to exit on through path
            through_len = entry_len + trail_len
            diversion_len = 4.65  # from frog to end of diversion path
            diversion_angle = 14.25

        else:
            entry_len = 3.35  # entry to frog
            trail_len = 8.65  # from frog to exit on through path - was 8.65
            through_len = entry_len + trail_len
            diversion_len = 7  # from frog to end of diversion path - was 6.77
            diversion_angle = 9.53

        if dir == 'R':
            diversion_angle = -diversion_angle

        if connection == 'mainline':
            # add the entry piece
            # add_line(self, entry_len, fill='white')
            print(entry_len)
            self.add_line(entry_len, fill='tan')

            # save the heading and location
            through_heading = self.heading  # save the heading
            through_x = self.x
            through_y = self.y
            self.heading += diversion_angle

            # add the diversion
            self.add_line(diversion_len, fill='tan')
            self.switch_list.append({'name': name,
                                   'div_x': self.x,
                                   'div_y': self.y,
                                   'div_heading': self.heading})

            # restore the heading and location
            self.heading = through_heading
            self.x = through_x
            self.y = through_y

            # add the exit
            # add_line(self, trail_len, fill='tan')
            self.add_line(trail_len)


        elif connection == 'through':
            # add the trail
            # add_line(self, trail_len, fill='tan')
            self.add_line(trail_len, fill='pink')

            # save the location/heading
            through_heading = self.heading  # save the heading
            through_x = self.x
            through_y = self.y

            # reverse the heading adjust for the diversion angle
            # (reverse becasue the angle is given of mainline entry, not through)
            self.heading += 180 + diversion_angle

            # add the diversion
            # add_line(self, diversion_len, fill='orange')
            self.add_line(diversion_len)
            self.switch_list.append({'name': name,
                                   'div_x': self.x,
                                   'div_y': self.y,
                                   'div_heading': self.heading})

            # restore the heading and add the final section
            self.heading = through_heading
            self.x = through_x
            self.y = through_y

            # add_line(self, entry_len, fill='white')
            self.add_line(entry_len, fill='pink')

        print("Turnout end ({:.2f}, {:.2f}), {:.2f}".format(
            self.x, self.y, self.heading))


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
            print("{}: divX:{:.2f} divY:{:.2f} divH:{:.2f}".format(
                entry['name'],
                entry['div_x'],
                entry['div_y'],
                entry['div_heading']))

