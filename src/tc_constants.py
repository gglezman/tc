#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
# This file contains constants that are used by the train control python scripts.
#


# the following section contains constants for the GUI

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

# See I2C register definitions
# Inventory data
I2C_REG_ID_LEN = 1

I2C_REG_INVENTORY_VERSION = 0
I2C_INVENTORY_VERSION_LEN = 1

I2C_REG_I2C_ADR = 1
I2C_I2C_ADR_LEN = 1

I2C_REG_BOARD_TYPE = 2
I2C_BOARD_TYPE_LEN = 1

I2C_REG_BOARD_DESCRIPTION = 3
I2C_BOARD_DESCRIPTION_LEN = 16

I2C_REG_BOARD_VERSION = 4
I2C_BOARD_VERSION_LEN = 1

I2C_REG_I2C_COMM_SW_VERSION = 10
I2C_I2C_COMM_SW_VERSION_LEN = 9

I2C_REG_INVENTORY_SW_VERSION = 11
I2C_INVENTORY_SW_VERSION_LEN = 9

I2C_REG_I2C_WRITE_CHKSUM_FAILURE = 18
I2C_I2C_WRITE_CHKSUM_FAILURE_LEN = 2

I2C_REG_WRITE_SEQ_NUM = 19
I2C_WRITE_SEQ_NUM_LEN = 1

I2C_REG_APP_SW_VERSION = 20
I2C_APP_SW_VERSION_LEN = 9

I2C_CHECKSUM_LEN = 1
# ################################################
#  I2C Register map for this application
#
#  Define all register assignemnts specific to
#  the application here.
# #################################################
I2C_REG_DT_A_POWER_STATUS = 30
I2C_REG_DT_B_POWER_STATUS = 40
I2C_DT_POWER_STATUS_LEN = 1

I2C_REG_DT_A_ADIRECTION = 31
I2C_REG_DT_B_ADIRECTION = 41
I2C_DT_DIRECTION_LEN = 1

I2C_REG_DT_A_MOMENTUM = 32
I2C_REG_DT_B_MOMENTUM = 42
I2C_DT_MOMENTUM_LEN = 1

I2C_REG_DT_A_POWER_LEVEL = 33
I2C_REG_DT_B_POWER_LEVEL = 43
I2C_DT_POWER_LEVE_LEN = 1

I2C_REG_DT_A_SPEED = 34;
I2C_REG_DT_B_SPEED = 44;
I2C_DT_SPEED_LEN = 1;

I2C_REG_DT_A_EMERGENCY_STOP = 35;
I2C_REG_DT_B_EMERGENCY_STOP = 45;
I2C_DT_EMERGENCY_STOP_LEN = 1;
