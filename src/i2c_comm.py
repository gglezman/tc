#
# Author: Greg Glezman
#
# SCCSID : "%W% %G%
#
# Copyright (c) 2020 G.Glezman.  All Rights Reserved.
#
#

import tc_constants as tcc
import subprocess
from time import sleep
from smbus2 import SMBus


class I2C_Comm:
    def __init__(self, bus):
        self.smbus = SMBus(bus=bus)
        self.write_seq_num = 0
        sleep(1)   # give the bus a chance to settle

    def get_device_info(self, adr):

        board_info = {"inventoryVersion": 0, "i2cAddress": 0, "boardType": 0, "boardDescription": "unknown",
                      "boardVersion": 0, "i2cCommSwVersion": "unknown", "inventorySwVersion": "unknown",
                      "applicationSwVersion": "unknown"}

        reg, dev_info = self.get_register(adr,
                                          tcc.I2C_REG_INVENTORY_VERSION,
                                          tcc.I2C_REG_ID_LEN + tcc.I2C_INVENTORY_VERSION_LEN)
        if reg == tcc.I2C_REG_INVENTORY_VERSION and dev_info[0] == 1:
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
            if reg > 0:
                board_info["boardDescription"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, tcc.I2C_REG_BOARD_VERSION, tcc.I2C_REG_ID_LEN + tcc.I2C_BOARD_VERSION_LEN)
            if reg > 0:
                board_info["boardVersion"] = dev_info[0]
            reg, dev_info = self.get_register(adr, tcc.I2C_REG_I2C_COMM_SW_VERSION, tcc.I2C_REG_ID_LEN + tcc.I2C_I2C_COMM_SW_VERSION_LEN)
            if reg > 0:
                board_info["i2cCommSwVersion"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, tcc.I2C_REG_INVENTORY_SW_VERSION,  tcc.I2C_REG_ID_LEN + tcc.I2C_INVENTORY_SW_VERSION_LEN)
            if reg > 0:
                board_info["inventorySwVersion"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, tcc.I2C_REG_APP_SW_VERSION, tcc.I2C_REG_ID_LEN + tcc.I2C_APP_SW_VERSION_LEN)
            if reg > 0:
                board_info["applicationSwVersion"] = self.char_list_to_string(dev_info)

            reg, dev_info = self.get_register(adr, 99, 2)
            if len(dev_info) > 0:
                print("99 data : {}".format(dev_info))
            else:
                print("99 data: None****")
        return board_info

    @staticmethod
    def char_list_to_string(char_list):
        return ''.join([chr(c) for c in char_list if c > 31 and c < 128])

    def get_register(self, adr, reg, data_length):
        """
        :param adr: I2C Bus address
        :param reg: board register
        :param data_length: of data to read (not counting the checksum)
        :return: reg or -1 (on error),
                 reg_data (remaining bytes read)
        """
        cmd = -1            # Assume error return
        reg_data = []
        length = data_length + tcc.I2C_CHECKSUM_LEN
        for retry in range(0, 4):
            try:
                reg_data = self.smbus.read_i2c_block_data(adr, reg, length)
                if len(reg_data) == length:
                    if self.validate_checksum(reg_data) == 0:
                        cmd = reg_data.pop(0)        # todo - checksum is still attached !
                        reg_data.pop(-1)             # remove the checksum
                        if cmd == reg:
                            break
                    else:
                        print("get_register checksum error {}".format(self.validate_checksum(reg_data)))
                else:
                    print("get_register blipped: len:{}".format(length))
            except IOError:
                print("Error get _register at adr {} / reg {}".format(adr, reg))

        return cmd, reg_data

    def set_register(self, adr, reg, send_data):
        try:
            self.smbus.write_i2c_block_data(adr, reg, send_data)
        except IOError:
            print("Error setRegister at adr {} / reg {}".format(adr, reg))

    def get_byte_reg(self, adr, reg):
        """Read one byte of data from the specified register at the specified address.

        This would be a useful function for collecting inventory data except the Arduino
        code would need to be rewritten. The Arduino code sends multiple bytes back, starting
        with the regId. It would need to send only the requested data.

        To make use of this method, the Arduino code would need to send a single byte back
        in response to a request. Maybe later there will be registers where I need to do this.
        This method would be appropriate where higher performance is required.

        :param adr:
        :param reg:
        :return: reg or -1 on error
                 reg_data
        """
        for retry in range(0, 4):
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
        # run_cmd = ["i2cdetect", "-y", "1"]   use when shell=False
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
        length = 3    # reg, count, cs
        for i in range(messages_to_send):
            try:
                read_data = self.smbus.read_i2c_block_data(adr, reg, length)
                if len(read_data) == length:
                    if self.validate_checksum(read_data) == 0:
                        read_data.pop(-1)   # remove the checksum
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
            sleep(0.00001)

        return messages_to_send, read_exception, data_mismatch

    def block_write_test(self, adr, reg):
        """Execute a loopback test on the given address

        A loopback test consists of the following message sent 256 times
        to the given adr:
             block data write to
             - register 100
             - data [d1, d2, d3, cs]
             block data read from
             - register 100, 1+3+1 bytes (regId and data and cs)

        The  return value is a tuple (
                 messages_sent,
                 read_exception,
                 write_exception,
                 data_mismatch,
                 uncorrectable_errors
        """
        messages_to_send = 256

        write_exception = 0
        read_exception = 0
        data_mismatch = 0
        uncorrectable_err = 0

        for i in range(messages_to_send):
            # generate the data
            data = [i % 256, (i + 1) % 256, (i + 2) % 256]
            # do the write
            ue, re, we, dm = self.write_verify(adr, reg, data)

            # update the results
            uncorrectable_err += ue
            read_exception += re
            write_exception += we
            data_mismatch += dm

        return messages_to_send, read_exception, write_exception, \
               data_mismatch, uncorrectable_err

    def write_verify(self, adr, reg, data):
        """Do a single write / verify test with retries on the write and read back"""
        write_exception = 0
        read_exception = 0
        data_mismatch = 0
        final_result = 0
        read_result = -1

        for attempt in range(1, 5):
            write_result, we = self.write_func(adr, reg, data)
            write_exception += we
            if write_result == 0:
                # todo - .5 slows things down enough to print in the main Arduino loop if necessary
                #   I also used .1 to process buffers in the main loop prior to changing verify
                #   from reading data back to reading sequence number back.
                # sleep(.001)
                read_result, re, dm = self.read_verify(adr, 19, [self.write_seq_num])

                read_exception += re
                data_mismatch += dm
                if read_result == 0:
                    break
        # if attempt >= 5:                     # todo - i changed the check from 4 to 5
        if read_result != 0:                     # todo - i changed the check from 4 to 5
            final_result = 1
        errors = write_exception + read_exception + data_mismatch + final_result
        """
        if errors > 0:
        print("we {}, re {}, dm {}, unerr {}".format(write_exception,
        read_exception,
        data_mismatch,
        final_result))
        """
        return final_result, read_exception, write_exception, data_mismatch

    def write_func(self, adr, reg, data):
        """Write given data to the given address / register
        Inputs
           adr - I2C bus adr
           reg - register to write to
           data - list of bytes to write
        Generate a checksum and append it to the data. Make n attempts to
        write the data to adr/register. If an IOError occurs during the
        write, count it and retry. If a retry is required, use a new
        write_seq number.

        return
            result  0 : success, data was written, (may have taken retries)
                   -1 : failure, unable to write data
            write_exception - number of IOErrors encountered
        """
        write_exception = 0
        result = -1  # assume failure

        for attempt in range(1, 5):
            try:
                self.write_seq_num = (self.write_seq_num + 1) % 256
                cs = self.gen_checksum(reg, [self.write_seq_num] + data)
                self.smbus.write_i2c_block_data(adr, reg, [self.write_seq_num] + data + [cs], force=True)
                result = 0
                break
            except IOError:
                print("Write exception {}".format(self.write_seq_num))
                write_exception += 1

        return result, write_exception

    def read_verify(self, adr, reg, data):
        """Read from the given address/register and verify the expected_data
        Inputs
           adr - I2C bus adr
           reg - register to read from
           data - list of bytes expected

        Make n attempts to read from the given adr/register and verify the expected_data.
        If an IOError occurs during the read, count it and retry.
        If a checksum error occurs during the read, count it and retry.

        return
            result  0 : success, data was verified (may have taken retries)
                   -1 : failure, unable to verify data
            read_exception - number of IOErrors encountered
            data_mismatch - number of read failures
        """
        read_exception = 0
        data_mismatch = 0
        result = -1  # assume failure

        expected_data = [reg] + data       # Put the reg in the data list. Its part of the return data

        for attempt in range(1, 5):  # 4 retries for now
            try:
                # do the read/verify
                read_data = self.smbus.read_i2c_block_data(adr, reg, len(expected_data) + 1)  # +1 for checksum
                if self.validate_checksum(read_data) == 0:
                    read_data.pop(-1)    # removed the trailing checksum
                    if read_data == expected_data:
                        result = 0
                    else:
                        data_mismatch += 1
                    break   # OK, we were able to successfully read the register - we're done trying
                else:
                    data_mismatch += 1
                    print("Read Verify Checksum error")
            except IOError:
                read_exception += 1

        return result, read_exception, data_mismatch

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
    def validate_checksum(data):
        """Return zero is the checksum is valid"""
        checksum = 0
        for element in data:
            checksum += element
        return checksum % 256

    @staticmethod
    def gen_checksum(reg, buffer):
        check_sum = reg
        for element in buffer:
            check_sum += element
        return -(check_sum % 256)
