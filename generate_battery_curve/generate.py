#!/usr/bin/env python
# Author: ZhouZhuo

import sys
if (len(sys.argv) != 2):
    print('***Specific a curve file.')
    sys.exit(1)
import re
from config import *

state = 0
parsingTemp = 0
# { temp : [ batt ] }
TempBattListMap={}
# { temp : [ ocv ] }
TempOcvListMap={}
outTempOcvListMap={}
# { temp : [{ batt : ocv }] }
TempBattOcvListMap={}

def find_start(line):
    match = re.findall(r'START[ \t]+(-?\d+)', line)
    if len(match) == 1:
        global state
        global parsingTemp
        temp = match[0]
        parsingTemp = int(temp)
        TempOcvListMap[parsingTemp] = []
        TempBattListMap[parsingTemp] = []
        state = 1

def fill_map(line):
    match = re.findall(r'(\d+(?:\.\d+)?)[\t ]+(\d+(?:\.\d+)?)', line)
    if len(match) == 1:
        ocv, batt = match[0]
        TempOcvListMap[parsingTemp].append(float(ocv))
        TempBattListMap[parsingTemp].append(float(batt))
    elif re.findall(r'END', line) != []:
        global state
        state = 0

parse_tab = {
        0: find_start,
        1: fill_map
        }

if __name__ == '__main__':
    f = open(sys.argv[1])
    for line in f:
        parse_tab[state](line)
    f.close()

    TempBattListMap = {temp : [int(100 - round(batt/TempBattListMap[temp][-1]*100))
        for batt in TempBattListMap[temp]]
        for temp in TempBattListMap}
    TempOcvListMap = {temp : [int(round(1000*ocv))
        for ocv in TempOcvListMap[temp]]
        for temp in TempBattListMap}
    TempBattOcvListMap = {temp: {TempBattListMap[temp][i] : TempOcvListMap[temp][i]
        for i in range(len(TempBattListMap[temp]))}
        for temp in TempBattListMap}
    outTempOcvListMap = {temp : [TempBattOcvListMap[temp][batt]
        for batt in CareBattList]
        for temp in TempBattListMap}

    print ' ',
    length = None
    for temp in outTempOcvListMap:
        if length == None:
            length = len(outTempOcvListMap[temp])
        print '%4d' % temp,
    print
    for i in range(length):
        print '<',
        for temp in outTempOcvListMap:
            print '%d' % outTempOcvListMap[temp][i],
        print '>,'
