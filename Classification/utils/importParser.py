import os
import re
import sys
import json
from data_exploration.utils import changeCurrentDirToDatasets, Enum

cellType = Enum(['markdown', 'code'])

def importsParser(filePath):
    try:
        with open(filePath, 'r', encoding="utf-8") as f:
            cells = json.load(f)
    except Exception:
        return []

    fromIsOn = False
    importIndeciesList = []
    for cell in cells['cells']:
        if 'source' not in cell:
            continue
        sourceCode = cell['source']
        if sourceCode is None:
            continue
        if 'import' in sourceCode and cell['cell_type'] == cellType.code:
            sourceWordsList = re.sub("[^\w]", " ", sourceCode).split()
            for i, word in enumerate(sourceWordsList):
                if i == len(sourceWordsList) - 1:
                    continue
                if word == 'from':
                    importIndeciesList.append(sourceWordsList[i + 1])
                    fromIsOn = True
                elif word == 'import':
                    if fromIsOn:
                       fromIsOn = False
                    else:
                        importIndeciesList.append(sourceWordsList[i+1])
    if importIndeciesList:
        return set(importIndeciesList)

def filterPackages(packages):
    builtInPackages = sys.modules.keys()
    return {package:packages[package] for package in packages if package not in set(builtInPackages)}

def savePackagesAsFile(folderPath, packagesList):
    filePath = os.path.join(folderPath, 'packages.txt')
    with open(filePath, 'w') as f:
        [f.write('{}, {}\n'.format(package[0], package[1])) for package in packagesList]

def getMostCommonsPackages(packages, numOfPackages):
    sortedPackages = reversed(sorted(packages.items(), key=lambda kv: kv[1]))
    res = []
    for i, package in enumerate(sortedPackages):
        if i > numOfPackages:
            break
        res.append(package)
    return res


if __name__ == '__main__':
    changeCurrentDirToDatasets()
    dirPath = os.getcwd()
    packagesDict = {}
    for folder in os.listdir(dirPath):
        if os.path.isdir(folder):
            currentDirPath = os.path.join(dirPath, folder, 'kernels')
            for file in os.listdir(currentDirPath):
                filePath = os.path.join(currentDirPath, file)
                res = importsParser(filePath)
                if res:
                    for i in res:
                        if i not in packagesDict:
                            packagesDict[i] = 1
                        else:
                            packagesDict[i] += 1

    packagesDict = filterPackages(packagesDict)
    packagesDict = getMostCommonsPackages(packagesDict, 15)
    savePackagesAsFile(os.path.abspath(dirPath), packagesDict)
