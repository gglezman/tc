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

    def get_device_info(self, adr):

        board_info = {"inventoryVersion":0, "i2cAddress":0, "boardType":0, "boardDescription":"unknown",
                      "boardVersion":0, "i2cCommSwVersion":"unknown","inventorySwVersion":"unknown",
                      "applicationSwVersion":"unknown"}

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_INVENTORY_VERSION,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_INVENTORY_VERSION_LEN )
        if  reg == tcc.I2C_REG_INVENTORY_VERSION and dev_info[0] == 1:
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
            #description = self.char_list_to_string(dev_info)
            if reg > 0:
                board_info["boardDescription"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, tcc.I2C_REG_BOARD_VERSION, tcc.I2C_REG_ID_LEN + tcc.I2C_BOARD_VERSION_LEN)
            if reg > 0:
                board_info["boardVersion"] = dev_info[0]
                #print("brd version {}".format(board_info["boardVersion"]))
            reg, dev_info = self.get_register(adr, tcc.I2C_REG_I2C_COMM_SW_VERSION, tcc.I2C_REG_ID_LEN + tcc.I2C_I2C_COMM_SW_VERSION_LEN)
            if reg > 0:
                board_info["i2cCommSwVersion"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, tcc.I2C_REG_INVENTORY_SW_VERSION,  tcc.I2C_REG_ID_LEN + tcc.I2C_INVENTORY_SW_VERSION_LEN)
            #inv_sw_version = self.char_list_to_string(dev_info)
            if reg > 0:
                board_info["inventorySwVersion"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, tcc.I2C_REG_APP_SW_VERSION, tcc.I2C_REG_ID_LEN + tcc.I2C_APP_SW_VERSION_LEN)
            if reg > 0:
                board_info["applicationSwVersion"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, 99, 2)
            if len(dev_info) > 0:
                #print("99 data : {}".format(dev_info[0]))
                print("99 data : {}".format(dev_info))
            else:
                print("99 data: None****")
        #print(board_info)
        return board_info

    def char_list_to_string(self, char_list):   # TODO - rewrite this !!!
        string = " "
        for c in char_list:
            if 32 <= c <= 128:
                string += chr(c)
        return string

    def get_register(self, adr, reg, data_length):
        """
        :param adr: I2C Bus address
        :param reg: board register
        :param length: of data to read (not counting the checksum)
        :return: reg or -1 (on error),
                 reg_data (remaining bytes read)
        """
        cmd = -1            # Assume error return
        reg_data = []
        length = data_length + tcc.I2C_CHECKSUM_LEN
        for retry in range(0,4):
            try:
                #print("adr {}, reg {}, len {}".format(adr, reg, length))    # take me out
                reg_data = self.smbus.read_i2c_block_data(adr, reg, length)
                #print("len {} length {}".format(len(reg_data), length))      # take me out
                if len(reg_data) == length:
                    if self.validateChecksum(reg_data) == 0:
                        cmd = reg_data.pop(0)        # todo - checksum is still attached !
                        if cmd == reg:
                            break
                    else:
                        print("get_register checksum error {}".format(self.validateChecksum(reg_data)))
                else:
                    print("get_register blipped: len:{}".format(length))
            except IOError:
                print("Error get _register at adr {} / reg {}".format(adr, reg))

        return cmd, reg_data

    def set_register(self, adr, reg, send_data):
        # TODO - yake this out
        print("set reg {} / {}  / {}".format(adr, reg, send_data))
        try:
            self.smbus.write_i2c_block_data(adr, reg, send_data)
        except IOError:
            print("Error setRegister at adr {} / reg {}".format(adr, reg))

    def get_byte_reg(self, adr, reg):
        """Read one byte of data from the specified register at the specified address.

        This would be a useful function for collecting inventory data except the Arduino
        code would need to be rewritten. The Arduino code sends multiple bytes back, starting
        with the regId. It would need to send only the requested data.

        To make use of this method, the Ardino code would need to send a single byte back
        in response to a request. Maybe later there will be registers where I need to do this.
        This method would be appropriate where higher performance is required.

        :param adr:
        :param reg:
        :return: reg or -1 on error
                 reg_data
        """
        for retry in range (0,4):
            try:
                reg_data = self.smbus.read_byte_data(adr, reg)
                return_reg = reg
                break
            except IOError:
                print("Error get_byte_reg at adr {} / reg {}".format(adr, reg))
                # Note the following values may be overwritten by a successful retry
                return_reg = -1  # assume error
                reg_data = 0

        return return_reg, reg_data

    @staticmethod
    def get_controller_list():
        """ Find all active I2C devices on the bus

        :return: list of I2C addresses of all active devices
        """
        arduino_list = []

        cmd = "i2cdetect -y 1"
        #run_cmd = ["i2cdetect", "-y", "1"]   use when shell=False
        run_cmd = "i2cdetect -y 1"

        try:
            i2c_detect_output = subprocess.run(run_cmd, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)

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

        return arduino_list

    def block_read_test(self, adr, reg):
        """Execute a block read test on the given address / register

        A loopback test consists of the following message sent 256 times
        to the given adr:
             block data read to
             - register 'reg'

        The  return value is a tuple (messagesSent, readExceptions, data_mismatches).
        """
        messages_to_send = 256
        read_exception = 0
        data_mismatch = 0
        length = 3
        for i in range(messages_to_send):
            try:
                read_data = self.smbus.read_i2c_block_data(adr, reg, length)
                if len(read_data) == length:
                    if self.validateChecksum(read_data) == 0:
                        if read_data[0] != reg:
                            data_mismatch += 1
                            print("RegId read error")
                    else:
                        data_mismatch += 1
                        print("Checksum error: {} {} ".format(read_data[1], read_data[2]))
                else:
                    data_mismatch += 1
                    print("Length read error")
            except IOError:
                read_exception += 1
                print("Read IOerror at adr {}".format(adr))
                #print("Read IOerror at adr {} on attempt # {}".format(adr, i))
            sleep(0.00001)

        return messages_to_send, read_exception, data_mismatch

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

    @staticmethod
    def validateChecksum(list):
        ''' Return zero is the checksum is valid'''

        checksum = 0
        for element in list:
            checksum += element
        return checksum % 256
