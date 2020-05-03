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
import subprocess
from time import sleep
from smbus2 import SMBus


class I2C_Comm:
    def __init__(self, bus):
        self.smbus = SMBus(bus=bus)
        sleep(1)   # give the bus a chance to settle
        #print("Bus settled")

    def get_device_info(self, adr):

        board_info = {"inventoryVersion":0, "i2cAdr":0, "boardType":0, "boardDescriptionb":"unknown",
                      "boardVersion":0, "i2cCommSwVersion":"unknown","inventorySwVersion":"unknown","appSwVersion":"unknown"}

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_INVENTORY_VERSION,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_INVENTORY_VERSION_LEN)
        if  reg >= 0 and dev_info[0] == 1:
            # ####################################
            # inventory structure version 1
            # ####################################
            board_info["inventoryVersion"] = dev_info[0]
            #
            reg, dev_info = self.get_register(adr, tcc.I2C_REG_I2C_ADR, tcc.I2C_REG_ID_LEN + tcc.I2C_I2C_ADR_LEN)
            if reg > 0:
                board_info["i2cAddress"] = dev_info[0]
            #
            reg, dev_info = self.get_register(adr, tcc.I2C_REG_BOARD_TYPE, tcc.I2C_REG_ID_LEN + tcc.I2C_BOARD_TYPE_LEN)
            if reg > 0:
                board_info["boardType"] = dev_info[0]
            #
            reg, dev_info = self.get_register(adr, tcc.I2C_REG_BOARD_DESCRIPTION, tcc.I2C_REG_ID_LEN + tcc.I2C_BOARD_DESCRIPTION_LEN)
            description = self.char_list_to_string(dev_info)
            if reg > 0:
                board_info["boardDescription"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, tcc.I2C_REG_BOARD_VERSION, tcc.I2C_REG_ID_LEN + tcc.I2C_BOARD_VERSION_LEN)
            if reg > 0:
                board_info["boardVersion"] = dev_info[0]
                print("brd version {}".format(board_info["boardVersion"]))
            reg, dev_info = self.get_register(adr, tcc.I2C_REG_I2C_COMM_SW_VERSION, tcc.I2C_REG_ID_LEN + tcc.I2C_I2C_COMM_SW_VERSION_LEN)
            if reg > 0:
                board_info["i2cCommSwVersion"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, tcc.I2C_REG_INVENTORY_SW_VERSION,  tcc.I2C_REG_ID_LEN + tcc.I2C_INVENTORY_SW_VERSION_LEN)
            inv_sw_version = self.char_list_to_string(dev_info)
            if reg > 0:
                board_info["inventorySwVersion"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, tcc.I2C_REG_APP_SW_VERSION, tcc.I2C_REG_ID_LEN + tcc.I2C_APP_SW_VERSION_LEN)
            if reg > 0:
                board_info["applicationSwVersion"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, 99, 2)
            if len(dev_info) > 0:
                print("99 data : {}".format(dev_info[0]))
            else:
                print("99 data: None****")

        return board_info

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
        :return: regId or -1 (on error), remaining_bytes read
        """
        cmd = -1            # Assume error return
        reg_data = []
        try:
            reg_data = self.smbus.read_i2c_block_data(adr, reg, length)
            if len(reg_data) > 0:
                cmd = reg_data.pop(0)
        except IOError:
            print("Error on adr {}/ reg {}".format(adr, reg))
        return cmd, reg_data

    @staticmethod
    def get_controller_list():
        """ Find all active I2C devices on the bus

        :return: list of I2C addresses of all active devices
        """
        arduino_list = []

        cmd = "i2cdetect -y 1"
        run_cmd = ["i2cdetect", "-y", "1"]

        try:
            i2c_detect_output = subprocess.run(run_cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

            i2c_detect_output.check_returncode()
            i2c_rows = i2c_detect_output.stdout.splitlines()
            del i2c_rows[0]               # delete top row, its the heading
            for row in i2c_rows:
                adr_list = row.split()
                # delete the row identifier
                del adr_list[0]
                for adr in adr_list:
                    if adr != '--':
                        arduino_list.append(adr)
        except subprocess.CalledProcessError:
            print("CallProcessError encountered")

        """
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
        """
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
