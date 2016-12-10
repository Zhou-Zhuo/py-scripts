#!/usr/bin/env python
# Author: ZhouZhuo

import sys
import re
from config import *

rawInL = []
state = 0

def find_cmd(line):
    if re.findall(inListPrefixPattern, line) != []:
        global state
        state = 1

def read_cmd(line):
    if re.match(inListSuffixPattern, line):
        global state
        state = 2
    try:
        rawInL.append(re.findall(inCmdPrefixPattern+r'(.*)$', line)[0])
    except:
        return

parse_tbl = {
        0: find_cmd,
        1: read_cmd,
        }

def cookInL(L):
    outL = []
    n = 0
    for line in L:
        line = re.sub(r'^ *(..)', r'\1 '+outCmdMagic, line)
        line = re.sub(r' *\b(..)\b', r'0x\1, ', line)
        line = re.sub(r' *(0x..,) *(0x..,) *(0x..,) *(0x..,)', r'\1 \2 \3 \4\n', line)
        line = re.sub(r'\n ', r'\n', line)
        for x in range((4 + 1 - len(line.split(','))) % 4):
            line += ' 0xFF,'
        line = re.sub(r' +', r' ', line)
        line = outCmdPrefixFormat % n + line
        line += outCmdSuffix
        n += 1
        outL.append(line)
    return outL

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("*** Specify a file.")
        sys.exit(1)

    f = open(sys.argv[1])
    for line in f:
        parse_tbl[state](line)
        if state == 2:
            break

    for line in cookInL(rawInL):
        print line
