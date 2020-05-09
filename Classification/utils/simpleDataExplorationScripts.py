import csv
import statistics
from typing import Dict
from utils import consts
from utils.Graphs import *


def sumOfLines(linesPerCellDicExtended):
    numOfLines = 0
    for key in linesPerCellDicExtended:
        numOfLines += key * linesPerCellDicExtended[key]
    return numOfLines


def countPrintCells():
    linesPerCellDic: Dict[int, int] = {}
    linesPerCellDicExtended: Dict[int, int] = {}
    extendedList = []
    printCounter = 0
    numberOfEmptyCells = 0
    with open(consts.CELLS_TSV, mode="r", encoding="utf-8") as cellsFile:
        tsvReader = csv.reader(cellsFile, delimiter='\t')
        for cell in tsvReader:
            if cell:
                if isCellUseless(cell):
                    printCounter += 1
                cellAsString = str(cell[3])
                if cellAsString == "":
                    numberOfEmptyCells += 1
                else:
                    numOfLinesInCell = cellAsString.count("\\n") + 1
                    extendedList.append(numOfLinesInCell)
                    if (numOfLinesInCell // 10) in linesPerCellDic:
                        linesPerCellDic[(numOfLinesInCell // 10)] += 1
                    else:
                        linesPerCellDic[(numOfLinesInCell // 10)] = 1
                    if numOfLinesInCell in linesPerCellDicExtended:
                        linesPerCellDicExtended[numOfLinesInCell] += 1
                    else:
                        linesPerCellDicExtended[numOfLinesInCell] = 1
    printDesiredData(linesPerCellDic, linesPerCellDicExtended, printCounter, numberOfEmptyCells, extendedList)
    return linesPerCellDic


def printDesiredData(linesPerCellDic, linesPerCellDicExtended, printCounter, numberOfEmptyCells, extendedList):
    print("There are", printCounter,
          "cells that only display data and doesn't manipulate it (print/display/show/comments).")
    print("Number of cells with 0", "::", numberOfEmptyCells)
#     for key in sorted(linesPerCellDic.keys()):
#         print("Number of cells with", (key * 10) + 1, "-", key * 10 + 10, "::", linesPerCellDic[key])
    print("Mean:", statistics.mean(extendedList))
    print("Median:", statistics.median(extendedList))
    print("Max:", max(linesPerCellDicExtended.keys()))
    print("Min:", min(linesPerCellDicExtended.keys()))
    print("Total num of lines:", sumOfLines(linesPerCellDicExtended))
    print("Total num of cells:", sum(linesPerCellDicExtended.values()))
    print("Average number of lines per cell:",
          sumOfLines(linesPerCellDicExtended) // sum(linesPerCellDicExtended.values()))


def isCellUseless(cell):
    dividedCell = str(cell[3]).split(sep='\\n')
    for line in dividedCell:
        if line[:5] == "print" or line[:7] == "display" or line[:4] == "show" or line[:1] == "#" or line == "" \
                or "import" in line:
            continue
        else:
            return False
    return True

