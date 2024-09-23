#!/usr/bin/env python3

import os
import sys
import matplotlib.pyplot as plt
from pathlib import Path

def PrintHelp():
    mesg = '''
    Draw hist of number of the characters of the input file.
    Usually, every line records the filename of the root file,
    # character each line should be similar. Once a vary large
    variation found, it could be an error. Check it with histogram.

    ==============================================================

    usage: python3 checkLineNumber_LocallyBrowseRootFiles.py a.txt b.txt
    '''
    raise RuntimeError(mesg)



def GetArg_InputFiles(argv):
    if len(argv) > 1:
        return argv[1:]
    PrintHelp()

def info(mesg):
    print(f'i@ {mesg}')

def DrawHist_charactersPerLine(inFILEname:str):
    plt.cla()
    with open(inFILEname, 'r') as fIN:
        line_numbers = [ len(line) for line in fIN.readlines() ]
        nbin = 40
        fig, ax = plt.subplots()
        ax.hist(line_numbers, bins=nbin)
        filename = f'linenumber_{Path(inFILEname).stem}.jpg'
        ax.set_yscale('log')
        ax.set_xlabel('characters of each line')
        plt.savefig(filename)
        info(f'[OutputFig] {filename}')


if __name__ == "__main__":
    files = GetArg_InputFiles(sys.argv)
    for file in files:
        DrawHist_charactersPerLine(file)
