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

ACTIVE_COLOR = 'DeepSkyBlue2'
DISABLED_COLOR = 'gray75'
GRAY_BACKGROUND = 'gray75'
GRAY_BORDER = 'gray72'


def set_styles():

    s = ttk.Style()

    ##############################
    # Notebook Styles
    ##############################
    s.configure('TNotebook.Tab', justify='center')  # no effect
    s.configure('TNotebook.Tab', relief=tk.SUNKEN)  # no effect
    # s.configure('TNotebook.Frame', padding=3)     # no effect
    s.configure('TNotebook.Tab', underline=3)       # no effect
    # s.theme_settings("default", {"TNotebook.Tab": {"configure": {"padding": [5, 5]}}})
    s.configure('TNotebook.Tab', padding=(5, 5))
    s.configure('TNotebook.Tab', width=20)

    ###########################################
    # Scale Styles
    ###########################################

    s.configure('Tc.Vertical.TScale',
                borderwidth=int(tcc.SCREEN_WIDTH/130),
                troughcolor='black',
                troughrelief=tk.SUNKEN,
                sliderlength=int(tcc.SCREEN_HEIGHT/20),
                sliderthickness=int(tcc.SCREEN_WIDTH/30),   # 40
                sliderrelief=tk.RIDGE,
                background='gray',
                )
    s.map('Tc.Vertical.TScale',
          background=[('!disabled', 'brown')],
          troughcolor=[('!disabled', ACTIVE_COLOR)])

    ##############################
    # Label Styles
    ##############################
    s.configure("RidgeReliefML.TLabel", relief=tk.RIDGE, borderwidth=3, padding=(3,3,3,3),
                anchor=tk.CENTER, wraplength=100, justify=tk.CENTER)

    s.configure('Centered.TLabel', justify='center', anchor='center')
    s.configure('Medium.TLabel', padding=(2, 2))
    # not sure if anchor in the following works
    s.configure('MediumLeft.TLabel',
                # justify='right',  # I get left justified labels
                # anchor=tk.W,      #     without these 2 options
                padding=(2, 2))
    s.configure('ThinLeft.TLabel', padding=(1, 1))
    s.configure('Padded.TLabel', padding=(12, 0, 8))
    s.configure('NoPad.TLabel', padding=(0, 0, 0))
    s.configure('LimitedPad.TLabel', padding=(6, 0, 3))
    s.configure('Borderless.TLabel', borderwidth=0, padding=(6, 2, 1))
    s.configure('Active.TLabel', background=ACTIVE_COLOR)
    s.configure('Disabled.TLabel', background=DISABLED_COLOR)
    s.configure('MediumGray.TLabel', background=GRAY_BACKGROUND)

    ##############################
    # Labelframe Styles
    ##############################
    s.configure('Ridge.TLabelframe',
                # borderwidth=dfc.SMALL_BORDER_WIDTH,
                relief=tk.RIDGE)
    s.configure('Padded5Ridge.TLabelframe',
                # borderwidth=dfc.SMALL_BORDER_WIDTH,
                relief=tk.RIDGE, padding=5)

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
    s.configure('TButton', padding=(1, 3))
    s.configure('Medium.TButton', padding=(2, 2))
    s.configure('MediumThin.TButton', padding=(1, 1))
    s.configure('Thin.TButton', padding=(0, 0))
    s.configure('Special.Thin.TButton')
    s.configure('Borderless.TButton', borderwidth=0,
                background='White', anchor='w', padding=(18, 2, 1))
    s.configure('Yellow.TButton', background='yellow')
    s.configure('Red.TButton', background='red')
    s.configure('LimeGreen.TButton', background='lime Green')
    s.configure('Wheat1.TButton', background='wheat1')
    s.configure('Wheat3.TButton', background='wheat3')
    s.map("Yellow.TButton", background=[('active', 'yellow')])
    s.map("Red.TButton", background=[('active', 'red')])
    s.map("LimeGreen.TButton", background=[('active', 'lime green')])
    s.map("Wheat1.TButton", background=[('active', 'wheat1')])
    s.map("Wheat3.TButton", background=[('active', 'wheat3')])

    ##############################
    # Entry Styles
    ##############################
    s.configure('Special.TEntry')

    ##############################
    # Combobox Style
    ##############################
    # width in the following does not work
    s.configure('Common.TCombobox', width=9)
    s.configure('Special.TCombobox')

    ##############################
    # Radiobutton Styles
    ##############################
    s.configure('TRadiobutton', padding=(1, 3))

