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

SCREEN_SIZE = "LARGE"

if SCREEN_SIZE == "SMALL":
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 400
    small_text = 7
    med_text = 9
    med_large_text = 10
    large_text = 11
    extra_large = 13
    title_padding = 0
    tab_padding = 1
    slider_proportion = .70
    scale_slider_padding = (8, 3, 10)
    stop_sign_file="stop_sign_50_50.png"
elif SCREEN_SIZE == "MEDIUM":
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 600
    small_text = 8
    med_text = 10
    med_large_text = 12
    large_text = 14
    extra_large = 16
    title_padding = 5
    tab_padding = 3
    slider_proportion = .76              # percentage of height for slider
    scale_slider_padding = (8, 5, 10)    # spacing around slider title
    stop_sign_file="stop_sign_50_50.png"
elif SCREEN_SIZE == "LARGE":
    SCREEN_WIDTH = 1310
    SCREEN_HEIGHT = 740
    small_text = 10
    med_text = 12
    med_large_text = 14
    large_text = 18
    extra_large = 22
    title_padding = 5
    tab_padding = 3
    slider_proportion = .76              # percentage of height for slider
    scale_slider_padding = (8, 5, 10)    # spacing around slider title
    stop_sign_file="stop_sign_74_74.png"

# ############################################################################
# See I2C register definitions. The following are the I2C register assignments
# (and register length) for each of the supported I2C registers. For example,
# the WRITE_SEQ_NUM register is assigned address 19 and it is 1 byte in length.
# ############################################################################

# Note this information must match that used by the Arduinos

# Inventory data
I2C_REG_ID_LEN = 1

I2C_REG_INVENTORY_VERSION = 0
I2C_INVENTORY_VERSION_LEN = 1

I2C_REG_I2C_ADR = 1
I2C_I2C_ADR_LEN = 1

I2C_REG_BOARD_TYPE = 2
I2C_BOARD_TYPE_LEN = 1

# Board type definitions
BOARD_TYPE_THROTTLE = 1
BOARD_TYPE_SWITCHING = 2
BOARD_TYPE_LIGHTS = 3

I2C_REG_BOARD_DESCRIPTION = 3
I2C_BOARD_DESCRIPTION_LEN = 16

I2C_REG_BOARD_VERSION = 4
I2C_BOARD_VERSION_LEN = 1

I2C_REG_I2C_COMM_SW_VERSION = 10
I2C_I2C_COMM_SW_VERSION_LEN = 9

I2C_REG_INVENTORY_SW_VERSION = 11
I2C_INVENTORY_SW_VERSION_LEN = 9

I2C_REG_WRITE_TEST = 15
I2C_WRITE_TEST_LEN = 3

I2C_REG_UP_COUNTER = 16
I2C_UP_COUNTER_LEN = 1

# ############################################################################
# Checksum failure register. This is a counter which is incremented each time
# a checksum is detected in the received data AT the Arduino. The top level
# controller can read this register to determine how many checksum failures
# have occurred
# ############################################################################
I2C_REG_I2C_WRITE_CHKSUM_FAILURE = 18
I2C_I2C_WRITE_CHKSUM_FAILURE_LEN = 2

I2C_REG_WRITE_SEQ_NUM = 19
I2C_WRITE_SEQ_NUM_LEN = 1

I2C_REG_APP_SW_VERSION = 20
I2C_APP_SW_VERSION_LEN = 9

# All transmissions include a 1 byte checksum
I2C_CHECKSUM_LEN = 1

# ################################################
#  I2C Register map for the Throttle application
# #################################################

DT_THROTTLE_BASE = 30
DT_THROTTLE_ALLOCATION = 20

I2C_REG_DT_POWER_STATUS = DT_THROTTLE_BASE + 0         # A: 30, B:50
I2C_DT_POWER_STATUS_LEN = 1
POWER_ENABLED = 1
POWER_DISABLED = 0

I2C_REG_DT_DIRECTION = DT_THROTTLE_BASE + 1          # A: 31, B:51
I2C_DT_DIRECTION_LEN = 1
DIR_FORWARD = 1
DIR_REVERSE = 2

I2C_REG_DT_MOMENTUM = DT_THROTTLE_BASE + 2            # A: 32, B:52
I2C_DT_MOMENTUM_LEN = 1
MOMENTUM_ENABLED = 1
MOMENTUM_DISABLED = 0

I2C_REG_DT_POWER_LEVEL = DT_THROTTLE_BASE + 3         # A: 33, B:53
I2C_DT_POWER_LEVEL_LEN = 1

I2C_REG_DT_SPEED = DT_THROTTLE_BASE + 4               # A: 34, B:54
I2C_DT_SPEED_LEN = 1

I2C_REG_DT_EMERGENCY_STOP = DT_THROTTLE_BASE + 5      # A: 35, B:55
I2C_DT_EMERGENCY_STOP_LEN = 1
STOP_ACTIVATED = 1

# ################################################
#  I2C Register map for the Lights application
# #################################################

I2C_REG_LIGHT_POWER_LEVEL = 150
I2C_LIGHT_POWER_LEVEL_LEN = 2