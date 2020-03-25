#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
# This file contains constants that are used by the train control python scripts.
#

SMALL_SCREEN = 0
if SMALL_SCREEN:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 400
else:
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 600

if SCREEN_HEIGHT > 400:

    small_text = 8
    med_text = 10
    med_large_text = 12
    large_text = 16
    extra_large = 18
    title_padding = 5
    tab_padding = 3
    slider_proportion = .76              # percentage of height for slider
    scale_slider_padding = (8, 5, 10)    # spacing around slider title
    # print('Large screen detected')
else:
    small_text = 7
    med_text = 9
    med_large_text = 10
    large_text = 14
    extra_large = 16
    title_padding = 0
    tab_padding = 1
    slider_proportion = .70
    scale_slider_padding = (8, 3, 10)
    # print('small screen detected')
