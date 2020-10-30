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


# TODO - clean this out of unused styles
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
                sliderlength=int(tcc.SCREEN_HEIGHT/16),
                sliderthickness=int(tcc.SCREEN_WIDTH/20),   # 40
                sliderrelief=tk.RIDGE,
                background='gray',
                )
    s.map('Tc.Vertical.TScale',
          background=[('!disabled', 'brown')],
          troughcolor=[('!disabled', ACTIVE_COLOR)])

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
    s.configure("Bigger.TLabel", font=("TkDefaultFont", 14, "normal"))

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
    #s.configure('BiggerText.TButton', font=("Helvetica", 12, "normal"))
    s.configure('Gray.TButton', font=("Helvetica", tcc.med_text, "normal"), background='gray75', padding=10)
    s.configure('Yellow.TButton', font=("Helvetica", tcc.med_text, "normal"), background='yellow', padding=10)
    s.configure('Red.TButton', font=("Helvetica", tcc.med_text, "normal"), background='red', padding=10)
    s.configure('LimeGreen.TButton', font=("Helvetica", tcc.med_text, "normal"), background='lime Green', padding=10)
    s.configure('Wheat1.TButton', font=("Helvetica", tcc.med_text, "normal"), background='wheat1', padding=10)
    s.configure('Wheat3.TButton', font=("Helvetica", tcc.med_text, "normal"), background='wheat3', padding=10)
    s.map("Yellow.TButton", background=[('active', 'yellow')])
    s.map("Red.TButton", background=[('active', 'red')])
    s.map("LimeGreen.TButton", background=[('active', 'lime green')])
    s.map("Wheat1.TButton", background=[('active', 'wheat1')])
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


