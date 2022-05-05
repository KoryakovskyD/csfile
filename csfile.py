#!/usr/bin/env python3
##############################
# File name: csfile
#
# Purpose:
#   Count file's control sum
#
# Args:
#   1 - file path
import sys


def count_cs(fn):
    """
    Tries to read a file byte by byte and count control sum

    Args:
        fn - file path (string)

    Returns:
        Returns CS number if file successfully readed and counted
                0 file is bigger than required or parsing exception occurs
    """
    # constants
    BOARD_BOOTER_ELF_MAX_SIZE = 0x4000000    # 64M !
    SCHAR_MAX = 127
    UCHAR_MAX = 255
    INT_MAX = 2147483647
    INT_MIN = (INT_MAX + 1) * (-1)

    try:
        # read file byte by byte
        byte_list = []
        file = open(fn, "rb")
        while True:
            byte = file.read(1)
            if not byte:
                break
            byte_list.append(byte)
        file.close()

        # check file size limit
        bytes_quant = len(byte_list);
        print("BYTES IN FILE =", bytes_quant)
        if bytes_quant > BOARD_BOOTER_ELF_MAX_SIZE:
            print("File size error.")
            return 0

        # count CS (in one signed int with overflowing)
        overall_cs = 0
        for byte in byte_list:
           # byte to signed char
           signed_char = byte[0]
           if signed_char > SCHAR_MAX:
              signed_char = ((UCHAR_MAX + 1) - signed_char) * (-1)
           print("current signed_char NUM = ", signed_char)
           print("current signed_char byte HEX = ", hex(signed_char))
           # add signed chars to signed int with overflowing
           overall_cs += signed_char
           if overall_cs > INT_MAX:
               overall_cs = (INT_MIN - 1) + (overall_cs - INT_MAX)
           elif overall_cs < INT_MIN:
               overall_cs = (INT_MAX + 1) - (INT_MIN - overall_cs)

        return overall_cs

    except IOError:
        print("Read file error.")
        return 0


###############    Main

print("Script name: ", sys.argv[0])

# params analyzing
if len(sys.argv) < 2:
    print("Warning: Script did not get filename.")
    sys.exit(0)

file_name = sys.argv[1]

# read file and count CS
cs = count_cs(file_name)
# represent an integer as a binary value
print("OVERALL CS RESULT = 0 x", format(cs & 0xffffffff, "08X"))
