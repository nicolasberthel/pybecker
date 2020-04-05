import logging

STX = b'\x02'
ETX = b'\x03'

CODE_PREFIX = "0000000002010B"  # 0-23 (24 chars)
CODE_SUFFIX = "000000"
CODE_21 = "021"
CODE_REMOTE = "01"  # centronic remote control used "02" while contralControl seem to use "01"

_LOGGER = logging.getLogger(__name__)


def hex2(n):
    return '%02X' % (n & 0xFF)


def hex4(n):
    return '%04X' % (n & 0xFFFF)


def checksum(code):
    code_length = len(code)
    if code_length != 40:
        _LOGGER.error("The code must be 40 characters long (without <STX>, <ETX> and checksum)")
        return
    code_sum = 0
    i = 0
    while i < code_length:
        hex_code = code[i] + code[i + 1]
        code_sum += int(hex_code, 16)
        i += 2
    return '%s%s' % (code.upper(), hex2(0x03 - code_sum))


def generate_code(channel, unit, cmd_code, with_checksum=True):
    unit_id = unit[0]  # contains the unit code in hex (5 chars)
    unit_inc = unit[1]  # contains the next increment (required to convert into hex4)

    code = CODE_PREFIX + hex4(unit_inc) + CODE_SUFFIX + unit_id + CODE_21 + CODE_REMOTE + hex2(channel) + '00' \
        + hex2(cmd_code)
    return checksum(code) if with_checksum else code


def finalize_code(code):
    return b"".join([STX, code.encode(), ETX])
