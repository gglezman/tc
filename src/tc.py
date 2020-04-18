#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
#

import tc_gui
from time import sleep
import i2c_comm as i2c_comm

bus_id = 1


def main():
    # #########################################
    # Run the GUI
    # #########################################

    gui = tc_gui.TcGui()

    i2c_bus = i2c_comm.I2C_Comm(bus_id)
    dev_list = i2c_bus.get_controller_list()
    print("DevList = {}".format(dev_list))

    for dev in dev_list:
        print("Collect Board info from {}".format(dev))
        adr = int(dev, base=16)
        info = i2c_bus.get_device_info(adr)
        # print(info)

    gui.run(i2c_bus)


if __name__ == "__main__":
    main()

