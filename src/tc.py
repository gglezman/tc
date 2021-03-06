#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
#

import tc_gui
import i2c_comm as i2c_comm

bus_id = 1


def main():
    # #########################################
    # Run the GUI
    # #########################################

    i2c_bus = i2c_comm.I2C_Comm(bus_id)

    gui = tc_gui.TcGui(i2c_bus)

    gui.run()


if __name__ == "__main__":
    main()

