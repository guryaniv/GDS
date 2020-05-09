import os
import sys
import csv
from statistics import median, mean
# from utils import consts

# importing modules from a different directory is different between systems and python versions
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../data_gathering')
try:
    import data_gathering.consts as consts
    print("consts imported")
except:
    try:
        import consts as consts
        print("consts imported")
    except:
        try:
            from .consts import consts as consts
            print("consts imported")
        except:
            try:
                from data_gathering import consts as consts
                print("consts imported")
            except:
                print("couldn't import consts")

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

def enum(**enums):
    return type('Enum', (), enums)

def incrementMemory():
    maxInt = sys.maxsize
    decrement = True

    while decrement:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True

def getDictOfCellsPerNB():
    with open(consts.CELLS_TSV, 'r', encoding="utf-8", newline='') as csvCellFile:
        csvCellsReader = csv.reader(csvCellFile, delimiter='\t')
        nbDict = {}
        names = set()
        for row in csvCellsReader:
            if row and row[1].lower() != 'notebook name':
                names.add(row[1])
                if row[1] not in nbDict:
                    nbDict[row[1]] = 1
                else:
                    nbDict[row[1]] += 1
        return nbDict

def getDictOfNBsPerDataset():
    with open(consts.NB_CSV, 'r', encoding="utf-8", newline='') as csvCellFile:
        csvNbReader = csv.reader(csvCellFile)
        dsDict = {}
        names = set()
        for row in csvNbReader:
            if row and row[3].lower() != 'dataset':
                names.add(row[3])
                if row[3] not in dsDict:
                    dsDict[row[3]] = 1
                else:
                    dsDict[row[3]] += 1
        return dsDict

def analyzeXAndYLists(nbDict, diff):
    '''
    Create ranges of values by the diff.
    Return two lists of keys and values in ranges
    '''
    cellsLevel = {}
    for nb in nbDict:
        index = nbDict[nb] // diff
        if index not in cellsLevel:
            cellsLevel[index] = [nb]
        else:
            cellsLevel[index].append(nb)
    res = {k:len(v) for k, v in sorted(cellsLevel.items())}
    return list(res.keys()), list(res.values())

def calculateParamters(valuesList):
    return max(valuesList), min(valuesList), mean(valuesList), median(valuesList)

    
def findAndRemoveComments(line):
    if '#' not in line:
        return line
    res = ''
    hashIndexes = [pos for pos, char in enumerate(line) if char == '#']
    newlineIndexes = [pos for pos, char in enumerate(line) if line[pos:pos+4] == '\\r\\n' or line[pos:pos+2] == '\\n']
    tuples = []
    taken = False
    taken2 = False
    for j in range(len(hashIndexes)):
        for i in newlineIndexes:
            if taken2:
                taken2 = False
                break
            elif j != len(hashIndexes)-1:
                if hashIndexes[j] < i and hashIndexes[j+1] > i and not taken2:
                    tuples.append((hashIndexes[j], i))
                    taken2 = True
            elif not taken and i > hashIndexes[j]:
                tuples.append((hashIndexes[j], i))
                taken = True

    lastIndex = 0
    for tple in tuples:
        res += line[lastIndex:tple[0]]
        lastIndex = tple[1]
    res += line[lastIndex:]
    return res