#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
#

import tc_constants as tcc

import os
from time import sleep
from smbus2 import SMBus


class I2C_Comm:
    def __init__(self, bus):
        self.smbus = SMBus(bus=bus)
        sleep(1)   # give the bus a chance to settle
        #print("Bus settled")

    def get_device_info(self, adr):

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_INVENTORY_VERSION,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_INVENTORY_VERSION_LEN)
        print("Inventory revision : {} ".format(*dev_info))

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_I2C_ADR,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_I2C_ADR_LEN)
        print("I2C address : 0x{:02x} ".format(*dev_info))

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_BOARD_TYPE,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_BOARD_TYPE_LEN)
        print("Board Type : {} ".format(*dev_info))

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_BOARD_DESCRIPTION,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_BOARD_DESCRIPTION_LEN)
        description = self.char_list_to_string(dev_info)
        print("Board Description : {}".format(description))

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_BOARD_VERSION,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_BOARD_VERSION_LEN)
        print("Board Version : {} ".format(*dev_info))

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_I2C_COMM_SW_VERSION,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_I2C_COMM_SW_VERSION_LEN)
        i2c_comm_version = self.char_list_to_string(dev_info)
        print("I2C Comm Sw Version : {} ".format(i2c_comm_version))

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_INVENTORY_SW_VERSION,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_INVENTORY_SW_VERSION_LEN)
        inv_sw_version = self.char_list_to_string(dev_info)
        print("Inventory Sw Version : {} ".format(inv_sw_version))

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_APP_SW_VERSION,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_APP_SW_VERSION_LEN)
        app_sw_version = self.char_list_to_string(dev_info)
        print("Application Sw Version : {} ".format(app_sw_version))

        reg, dev_info = self.get_register(adr, 99, 2)
        if len(dev_info) > 0:
            print("99 data : {}".format(dev_info[0]))
        else:
            print("99 data: None****")

    def char_list_to_string(self, char_list):
        string = " "
        for c in char_list:
            if 32 <= c <= 128:
                string += chr(c)
        return string

    def get_register(self, adr, reg, length):
        """
        :param adr:
        :param reg:
        :param length:
        :return: 1st byte, remaining_bytes
        """
        reg_data = []
        cmd = 0
        try:
            reg_data = self.smbus.read_i2c_block_data(adr, reg, length)
            if len(reg_data) > 0:
                cmd = reg_data.pop(0)
        except IOError:
            print("Error on adr {}".format(adr))
        return cmd, reg_data

    @staticmethod
    def get_controller_list():
        """ Find all active I2C devices on the bus

        :return: list of I2C addresses of all active devices
        """
        arduino_list = []

        cmd = "i2cdetect -y 1"
        i2c_detect_output = os.popen(cmd).read()

        i2c_rows = i2c_detect_output.splitlines()
        # delete the top row, its the column headings
        del i2c_rows[0]
        for row in i2c_rows:
            adr_list = row.split()
            # delete the row identifier
            del adr_list[0]
            for adr in adr_list:
                if adr != '--':
                    arduino_list.append(adr)
        return arduino_list

    def loopback_test(self, adr):
        """Execute a loopback test on the given address

        A loopback test consists of the following message sent 256 times
        to the given adr
        block data read to
        - register 99
        - seq number

        The  return value is a tuple (messagesSent, resendCount).
        """
        messages_to_send = 256
        errors = 0
        for i in range(messages_to_send):
            try:
                self.smbus.read_i2c_block_data(adr, 99, 2)  # 2=length
            except IOError:
                errors += 1
                print("Oops - error at adr {}".format(adr))
            sleep(0.001)

        return messages_to_send, errors
