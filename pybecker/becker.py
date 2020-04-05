import logging
import os
import time
import socket
import serial

from .database import Database
from .becker_helper import finalize_code
from .becker_helper import generate_code

COMMAND_UP = 0x20
COMMAND_UP2 = 0x24  # intermediate position "up"
COMMAND_DOWN = 0x40
COMMAND_DOWN2 = 0x44  # intermediate position "down"
COMMAND_HALT = 0x10
COMMAND_PAIR = 0x80  # pair button press
COMMAND_PAIR2 = 0x81  # pair button pressed for 3 seconds (without releasing)
COMMAND_PAIR3 = 0x82  # pair button pressed for 6 seconds (without releasing)
COMMAND_PAIR4 = 0x83  # pair button pressed for 10 seconds (without releasing)

DEFAULT_DEVICE_NAME = '/dev/serial/by-id/usb-BECKER-ANTRIEBE_GmbH_CDC_RS232_v125_Centronic-if00'

logging.basicConfig()
_LOGGER = logging.getLogger(__name__)


class Becker:

    def __init__(self, device_name=DEFAULT_DEVICE_NAME):
        self.is_serial = "/" in device_name or "\\" in device_name
        if self.is_serial and not os.path.exists(device_name):
            raise FileExistsError(device_name + " don't exists")
        self.device = device_name
        self.db = Database()
        if self.is_serial:
            self.s = serial.Serial(self.device, 115200, timeout=1)
            self.write_function = self.s.write
        else:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if ':' in device_name:
                host, port = self.device.split(':')
            else:
                host = device_name
                port = '5000'
            self.s.connect((host, int(port)))
            self.write_function = self.s.sendall

    async def write(self, codes):
        for code in codes:
            self.write_function(finalize_code(code))
            time.sleep(0.1)

    async def run_codes(self, channel, unit, cmd, test):
        if unit[2] == 0 and cmd != "TRAIN":
            _LOGGER.error("The unit %s is not configured" % (unit[0]))
            return

        codes = []
        if cmd == "UP":
            codes.append(generate_code(channel, unit, COMMAND_UP))
        elif cmd == "UP2":
            codes.append(generate_code(channel, unit, COMMAND_UP2))
        elif cmd == "HALT":
            codes.append(generate_code(channel, unit, COMMAND_HALT))
        elif cmd == "DOWN":
            codes.append(generate_code(channel, unit, COMMAND_DOWN))
        elif cmd == "DOWN2":
            codes.append(generate_code(channel, unit, COMMAND_DOWN2))
        elif cmd == "TRAIN":
            codes.append(generate_code(channel, unit, COMMAND_PAIR))
            unit[1] += 1
            codes.append(generate_code(channel, unit, COMMAND_PAIR2))
            unit[1] += 1
            codes.append(generate_code(channel, unit, COMMAND_PAIR))
            unit[1] += 1
            codes.append(generate_code(channel, unit, COMMAND_PAIR2))
            # set unit as configured
            unit[2] = 1
        elif cmd == "REMOVE":
            codes.append(generate_code(channel, unit, COMMAND_PAIR))
            unit[1] += 1
            codes.append(generate_code(channel, unit, COMMAND_PAIR2))
            unit[1] += 1
            codes.append(generate_code(channel, unit, COMMAND_PAIR))
            unit[1] += 1
            codes.append(generate_code(channel, unit, COMMAND_PAIR2))
            unit[1] += 1
            codes.append(generate_code(channel, unit, COMMAND_PAIR3))
            unit[1] += 1
            codes.append(generate_code(channel, unit, COMMAND_PAIR4))

        unit[1] += 1

        # append the release button code
        codes.append(generate_code(channel, unit, 0))

        unit[1] += 1

        await self.write(codes)
        self.db.set_unit(unit, test)

    async def send(self, channel, cmd, test=False):
        b = channel.split(':')
        if len(b) > 1:
            ch = int(b[1])
            un = int(b[0])
        else:
            ch = int(channel)
            un = 1

        if not 1 <= ch <= 7 and ch != 15:
            _LOGGER.error("Channel must be in range of 1-7 or 15")
            return

        if not self.device:
            _LOGGER.error("No device defined")
            return

        if un > 0:
            unit = self.db.get_unit(un)
            await self.run_codes(ch, unit, cmd, test)
        else:
            units = self.db.get_all_units()
            for unit in units:
                await self.run_codes(ch, unit, cmd, test)

    async def move_up(self, channel):
        """ Sent the command to move up for a given channel.

        :param channel: the channel on which the shutter is listening
        """
        await self.send(channel, "UP")

    async def move_up_intermediate(self, channel):
        """ Sent the command to move up in the intermediate position for a given channel.

        :param channel: the channel on which the shutter is listening
        """
        await self.send(channel, "UP2")

    async def move_down(self, channel):
        """ Sent the command to move down for a given channel.

        :param channel: the channel on which the shutter is listening
        """
        await self.send(channel, "DOWN")

    async def move_down_intermediate(self, channel):
        """ Sent the command to move down in the intermediate position for a given channel.

        :param channel: the channel on which the shutter is listening
        """
        await self.send(channel, "DOWN2")

    async def stop(self, channel):
        """ Sent the command to stop for a given channel.

        :param channel: the channel on which the shutter is listening
        """
        await self.send(channel, "HALT")

    async def pair(self, channel):
        """ Initiate the pairing for a given channel.

        :param channel: the channel on which the shutter is listening
        """
        await self.send(channel, "TRAIN")
