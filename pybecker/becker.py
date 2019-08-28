import os, time
import serial

STX = b'\x02'
ETX = b'\x03'
COMMAND_UP = 0x20
COMMAND_UP2 = 0x24 # intermediate position "up"
COMMAND_DOWN = 0x40
COMMAND_DOWN2 = 0x44 # intermediate position "down"
COMMAND_HALT = 0x10
COMMAND_PAIR = 0x80
COMMAND_PAIR2 = 0x81 # simulates the delay of 3 seconds
COMMAND_PAIR3 = 0x82 # simulates the delay of 6 seconds
COMMAND_PAIR4 = 0x83 # simulates the delay of 10 seconds (important for deletion)
DEFAULT_DEVICE = '/dev/serial/by-id/usb-BECKER-ANTRIEBE_GmbH_CDC_RS232_v125_Centronic-if00'

CODE_PREFIX = "0000000002010B" # 0-23 (24 chars)
CODE_SUFFIX = "000000"
CODE_DEVICE = "1737b0" # 24-32 (8 chars) / CentralControl number (https://forum.fhem.de/index.php/topic,53756.165.html)
CODE_21 = "21"
CODE_REMOTE = "01" # centronic remote control used "02" while contralControl seem to use "01"


class Becker:
    def __init__(self, **kwargs):
        """ Constructor for Becker API.

        :param port: the device port if not set the default one will be used
        """
        self._device = DEFAULT_DEVICE
        if 'port' in kwargs:
            self._device = kwargs['port']
        self._number_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "centronic-stick.num")

    def __hex2(self, n):
        return "%02X"%(n&0xFF)

    def __hex4(self, n):
        return "%04X"%(n&0xFFFF)

    def __read_number(self):
        exists = os.path.isfile(self._number_file_path)
        number = "0"
        if exists:
            number_file = open(self._number_file_path, "r")
            number = number_file.read()
        return int(number)

    def __increment_number(self):
        number = self.__read_number()
        number += 1
        number_file = open(self._number_file_path, "w")
        number_file.write(str(number))

    def __generate_code(self, channel, cmd):
        number = self.__read_number()
        code = CODE_PREFIX + ("%s" % self.__hex4(number)) + CODE_SUFFIX + CODE_DEVICE + CODE_21 + CODE_REMOTE
        code += ("%s" % self.__hex2(channel)) + "00" + ("%s" % self.__hex2(cmd))
        return code

    def __send(self, channel, cmd):

        codes = []

        with serial.Serial(self._device, 115200, timeout=1) as ser:

            if cmd == "UP":
                codes.append(self.__generate_code(channel, COMMAND_UP))
            elif cmd == "UP2":
                codes.append(self.__generate_code(channel, COMMAND_UP2))
            elif cmd == "HALT":
                codes.append(self.__generate_code(channel, COMMAND_HALT))
            elif cmd == "DOWN":
                codes.append(self.__generate_code(channel, COMMAND_DOWN))
            elif cmd == "DOWN2":
                codes.append(self.__generate_code(channel, COMMAND_DOWN2))
            elif cmd == "PAIR":
                codes.append(self.__generate_code(channel, COMMAND_PAIR))
                self.__increment_number()
                codes.append(self.__generate_code(channel, COMMAND_PAIR2))

            self.__increment_number()
            codes.append(self.__generate_code(channel, 0))  # append the release button code
            self.__increment_number()
            for code in codes:
                ser.write(STX + code.encode() + ETX)

                time.sleep(0.1)

    def move_up(self, channel):
        """ Sent the command to move up for a given channel.

        :param channel: the channel on which the shutter is listening
        """
        self.__send(channel, "UP")

    def move_down(self, channel):
        """ Sent the command to move down for a given channel.

        :param channel: the channel on which the shutter is listening
        """
        self.__send(channel, "DOWN")

    def stop(self, channel):
        """ Sent the command to stop for a given channel.

        :param channel: the channel on which the shutter is listening
        """
        self.__send(channel, "HALT")

    def pair(self, channel):
        """ Initiate the pairing for a given channel.

        :param channel: the channel on which the shutter is listening
        """
        self.__send(channel, "PAIR")

