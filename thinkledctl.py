#!/bin/python

# thinkledctl
# Copyright (C) 2023 Yannis Charalambidis
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import time
import argparse

parser = argparse.ArgumentParser(
    prog='thinkledctl',
    description='Display morse code on the led of a thinkpad\'s lid. Supports \
    only letters [a-zA-Z-=\\/0-9 ].',
    epilog='This is free software under the GNU GPL version 3.')
parser.add_argument('MESSAGE')
args = parser.parse_args()

MESSAGE = str(args.MESSAGE).upper()
LED_PATH = "/sys/class/leds/tpacpi::lid_logo_dot/brightness"
LED_ON = '1'
LED_OFF = '0'

UNIT_S = 0.2

DIT_LENGTH_S = 1 * UNIT_S  # .
DAH_LENGTH_S = 3 * UNIT_S  # -
INTRA_CHAR_S = 1 * UNIT_S  # Intra char space
INTER_CHAR_S = 3 * UNIT_S  # Space between chars in a word
WORD_S = 7 * UNIT_S  # Space between words
END_S = 14 * UNIT_S  # Space between messages

code = {'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        '0': '-----',
        ' ': '/'}


def on():
    f = open(LED_PATH, 'r+')
    f.write(LED_ON)
    f.close()


def off():
    f = open(LED_PATH, 'r+')
    f.write(LED_OFF)
    f.close()


IDX = 0

try:
    while True:
        off()
        time.sleep(INTER_CHAR_S)

        morse = code[MESSAGE[IDX]]
        for char in morse:
            off()
            time.sleep(INTRA_CHAR_S)

            on()
            if char == '.':
                time.sleep(DIT_LENGTH_S)
            elif char == '-':
                time.sleep(DAH_LENGTH_S)
            elif char == '/':
                off()
                time.sleep(WORD_S)

        IDX += 1

        if IDX == len(MESSAGE):
            off()
            time.sleep(END_S)
            IDX = 0
except:
    off()
