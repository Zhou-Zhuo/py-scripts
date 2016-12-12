#!/usr/bin/env python
# Author: ZhouZhuo

import sys
if len(sys.argv) != 2:
    print("*** Specify a file.")
    sys.exit(1)

import re
import matplotlib.pyplot as plt
from config import *

def extrat_num(L):
    outL = []
    for line in L:
        for num in re.findall(r'[-]?\d+', line):
            outL.append(int(num))
    return outL

filename = sys.argv[1]
f = open(filename)

rawTemp = []
rawPers = []
rawData = []
state = 0

def find_lut(line):
    if re.findall(OcvLutPrefixPattern, line) != []:
        global state
        state = 1
        find_col(line)

def find_col(line):
    if re.findall(lutColPrefixPattern, line) != []:
        global state
        state = 2
        read_col(line)

def read_col(line):
    rawTemp.append(line)
    if re.findall(r';', line) != []:
        global state
        state = 3

def find_row(line):
    if re.findall(lutRowPrefixPattern, line) != []:
        global state
        state = 4
        read_row(line)

def read_row(line):
    rawPers.append(line)
    if re.findall(r';', line) != []:
        global state
        state = 5

def find_dat(line):
    if re.findall(lutDataPrefixPattern, line) != []:
        global state
        state = 6
        read_dat(line)

def read_dat(line):
    rawData.append(line)
    if re.findall(r';', line) != []:
        global state
        state = 7

parse_tab = {
        0: find_lut,
        1: find_col,
        2: read_col,
        3: find_row,
        4: read_row,
        5: find_dat,
        6: read_dat
        }

if __name__ == "__main__":
    for line in f:
        parse_tab[state](line)
        if state == 7:
            break
    f.close()
    
    Temp = extrat_num(rawTemp)
    Pers = extrat_num(rawPers)
    _Data = []
    for line in rawData:
        _Data.append(extrat_num([line]))
    Data = []
    for n in range(len(_Data[0])):
        colData = []
        for row in _Data:
            colData.append(row[n])
        Data.append(colData)
    
    for n in range(len(Temp)):
        plt.plot(Pers, Data[n], label='Temp = %d'%Temp[n])
    plt.legend(loc=0)
    plt.show()
