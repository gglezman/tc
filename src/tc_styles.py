#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
# This file contains classes that are used by the train control python script
# to initialize ttk styles used.
#

import tkinter as tk
import tkinter.ttk as ttk
import tc_constants as tcc
# from tkinter.font import Font

ACTIVE_COLOR = 'DeepSkyBlue2'
DISABLED_COLOR = 'gray75'
GRAY_BACKGROUND = 'gray75'
GRAY_BORDER = 'gray72'
MYLIMEGREEN = '#32c032'
TRACK_COLOR = 'green'
TRACK_IDENTIFY_COLOR = 'white'
THRU_ACTIVE_COLOR = MYLIMEGREEN
DIV_ACTIVE_COLOR = MYLIMEGREEN
DIV_INACTIVE_COLOR = 'gray'

def set_styles():

    s = ttk.Style()

    ##############################
    # Notebook Styles
    ##############################
    #s.configure('TNotebook.Tab', justify='center')  # no effect
    #s.configure('TNotebook.Tab', relief=tk.SUNKEN)  # no effect
    ## s.configure('TNotebook.Frame', padding=3)     # no effect
    #s.configure('TNotebook.Tab', underline=3)       # no effect
    ## s.theme_settings("default", {"TNotebook.Tab": {"configure": {"padding": [5, 5]}}})
    #s.configure('TNotebook.Tab', padding=(5, 5))
    #s.configure('TNotebook.Tab', width=20)

    ###########################################
    # Scale Styles
    ###########################################

    s.configure('Tc.Vertical.TScale',
                borderwidth=int(tcc.SCREEN_WIDTH/130),
                troughcolor='black',
                troughrelief=tk.SUNKEN,
                sliderlength=int(tcc.SCREEN_HEIGHT/16),
                sliderthickness=int(tcc.SCREEN_WIDTH/20),   # 40
                sliderrelief=tk.RIDGE,
                background='gray',
                )
    s.map('Tc.Vertical.TScale',
          background=[('!disabled', 'brown')],
          troughcolor=[('!disabled', ACTIVE_COLOR)])

    s.configure('LightsOff.Horizontal.TScale',
                borderwidth=5,  # works - trough border
                troughcolor=MYLIMEGREEN,  # works
                #troughcolor='lime green',  # works
                sliderthickness=40,  # thickness of horizontal slider
                sliderrelief=tk.RAISED,  # works
                background='green',  # works - slider color
                )
    s.configure('LightsLow.Horizontal.TScale',
                borderwidth=5,  # works - trough border
                troughcolor='salmon',  # works
                sliderthickness=40,  # thickness of horizonatl slider
                sliderrelief=tk.RAISED,  # works
                background='salmon',  # works - slider color
                )
    s.configure('LightsMed.Horizontal.TScale',
                borderwidth=5,  # works - trough border
                troughcolor='tomato',  # works
                sliderthickness=40,  # thickness of horizonatl slider
                sliderrelief=tk.RAISED,  # works
                background='tomato',  # works - slider color
                )
    s.configure('LightsFull.Horizontal.TScale',
                borderwidth=5,  # works - trough border
                troughcolor='red',  # works
                sliderthickness=30,  # thickness of horizonatl slider
                sliderrelief=tk.RAISED,  # works
                background='red',  # works - slider color
                )

    ##############################
    # Label Styles
    ##############################
    s.configure("RidgeReliefML.TLabel",
                relief=tk.RIDGE,
                borderwidth=2,
                padding=(3, 3, 3, 3),
                anchor=tk.CENTER,
                wraplength=130,
                justify=tk.CENTER,
                font=("Helvetica", 12, "normal")
                )

    s.configure('Active.TLabel', background=ACTIVE_COLOR)
    s.configure('Disabled.TLabel', background=DISABLED_COLOR)
    s.configure('MediumGray.TLabel',font=("Helvetica", tcc.large_text, "normal"), background=GRAY_BACKGROUND)
    s.configure('DarkGray.TLabel',font=("Helvetica", tcc.large_text, "normal"), background=GRAY_BORDER)
    s.configure("Bigger.TLabel", font=("TkDefaultFont", tcc.med_large_text, "normal"))

    ##############################
    # Frame Styles
    ##############################
    s.configure('Disabled.TFrame', background=DISABLED_COLOR)
    s.configure('Active.TFrame', background=ACTIVE_COLOR)
    s.configure('MediumGray.TFrame', background=GRAY_BACKGROUND)
    s.configure('DarkGray.TFrame', background=GRAY_BORDER)

    ##############################
    # Button Styles
    ##############################
    s.configure('DarkGray.TButton', font=("Helvetica", tcc.med_text, "normal"), background='GRAY_BORDER', padding=8)
    s.configure('Gray.TButton', font=("Helvetica", tcc.med_text, "normal"), background='gray75', padding=8)

    # #######################
    # Lights Panel
    # #######################
    s.configure('LightsReady.TButton', font=("Helvetica", tcc.med_text, "normal"), background='gray75', padding=10, borderwidth = 5)

    s.configure('LightsOff.TButton', font=("Helvetica", tcc.med_text, "normal"), background=MYLIMEGREEN,padding=10, borderwidth=5)
    s.map("LightsOff.TButton", background=[('active', 'lime green')])

    s.configure('LightsOnLow.TButton', font=("Helvetica", tcc.med_text, "normal"), background='salmon', padding=10, borderwidth=5)
    s.map("LightsOnLow.TButton", background=[('active', 'salmon')])

    s.configure('LightsOnMed.TButton', font=("Helvetica", tcc.med_text, "normal"), background='tomato', padding=10, borderwidth=5)
    s.map("LightsOnMed.TButton", background=[('active', 'tomato')])

    s.configure('LightsOnFull.TButton', font=("Helvetica", tcc.med_text, "normal"), background='red', padding=10, borderwidth=5)
    s.map("LightsOnFull.TButton", background=[('active', 'red')])

    # #######################
    # Switch Panel
    # #######################
    s.configure('ThruActive.TButton', font=("Helvetica", tcc.med_text, "normal"), background=THRU_ACTIVE_COLOR, padding=10)
    s.map("ThruActive.TButton", background=[('active', THRU_ACTIVE_COLOR)])
    s.configure('ThruInactive.TButton', font=("Helvetica", tcc.med_text, "normal"), background='gray', padding=10)
    s.map("ThruInactive.TButton", background=[('active', 'gray')])

    s.configure('DivertActive.TButton', font=("Helvetica", tcc.med_text, "normal"), background=DIV_ACTIVE_COLOR, padding=10)
    s.map("DivertActive.TButton", background=[('active', DIV_ACTIVE_COLOR)])
    s.configure('DivertInactive.TButton', font=("Helvetica", tcc.med_text, "normal"), background=DIV_INACTIVE_COLOR, padding=10)
    s.map("DivertInactive.TButton", background=[('active', DIV_INACTIVE_COLOR)])

    s.configure('Name.TButton', font=("Helvetica", tcc.med_text, "normal"), background=GRAY_BORDER, padding=10, relief=tk.FLAT)
    s.map("Name.TButton", background=[('active', GRAY_BORDER)])
    s.configure('NameActive.TButton', font=("Helvetica", tcc.med_text, "normal"), background='white', padding=10)
    s.map("NameActive.TButton", background=[('active', 'white')])

    # #######################
    # Throttle Panel
    # #######################
    s.configure('Yellow.TButton', font=("Helvetica", tcc.med_text, "normal"), background='yellow', padding=8, borderwidth=5)
    s.map("Yellow.TButton", background=[('active', 'yellow')])

    s.configure('Red.TButton', font=("Helvetica", tcc.med_text, "normal"), background='red', padding=8, borderwidth=5)
    s.map("Red.TButton", background=[('active', 'red')])

    s.configure('LimeGreen.TButton', font=("Helvetica", tcc.med_text, "normal"), background='lime Green',padding=8, borderwidth=5)
    s.map("LimeGreen.TButton", background=[('active', 'lime green')])

    s.configure('Wheat1.TButton', font=("Helvetica", tcc.med_text, "normal"), background='wheat1', padding=8, borderwidth=5)
    s.map("Wheat1.TButton", background=[('active', 'wheat1')])

    s.configure('Wheat3.TButton', font=("Helvetica", tcc.med_text, "normal"), background='wheat3', padding=8, borderwidth=5)
    s.map("Wheat3.TButton", background=[('active', 'wheat3')])

    ##############################
    # Entry Styles
    ##############################
    s.configure('Padded.TEntry', padding=(4, 4))

    ##############################
    # Combobox Style
    ##############################@
    # width in the following does not work
    s.configure('Padded.TCombobox', padding=(4, 4))


