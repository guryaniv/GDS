import matplotlib.pyplot as plt
from utils.utils import Enum, incrementMemory, getDictOfCellsPerNB, getDictOfNBsPerDataset, calculateParamters, analyzeXAndYLists

graphTypes = Enum(['NOTEBOOKS_PER_DATASET', 'CELLS_PER_NOTEBOOKS'])

def createGraph(diff, graphType, xLabels, yLabels, title):
    nbDict = {}
    if graphType == graphTypes.CELLS_PER_NOTEBOOKS:
        nbDict = getDictOfCellsPerNB()
    elif graphType == graphTypes.NOTEBOOKS_PER_DATASET:
        nbDict = getDictOfNBsPerDataset()
    maxV, minV, meanV, medianV = calculateParamters(nbDict.values())
    print('Max value: {}\nMin value: {}\nMean value: {}\nMedian value: {}'.format(maxV, minV, meanV, medianV))
    x, y = analyzeXAndYLists(nbDict, diff)
    xStr = ['[{}-{})'.format(i*diff, i*diff + (diff-1)) for i in x] + ['[{}-inf)'.format(x[-1]*diff)]
    drawBarPlot(x, y, xStr, xLabels, yLabels, title)

def drawBarPlot(x, y, xStr, xLabels, yLabels, title):
    plt.xticks(x, xStr, rotation=70)
    plt.ylabel(yLabels)
    plt.xlabel(xLabels)
    plt.title(title)

    bar1 = plt.bar(x, height=y)

    for rect in bar1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '{}'.format(int(height)), ha='center', va='bottom')

    plt.show()


# if __name__ == '__main__':
#     incrementMemory()
#     createGraph(diff=10, graphType=graphTypes.CELLS_PER_NOTEBOOKS, xLabels='Cells', yLabels='Notebooks', title='Cells Per Notebook')
#     createGraph(diff=20, graphType=graphTypes.NOTEBOOKS_PER_DATASET, xLabels='Notebooks', yLabels='Datasets', title='Notebooks per Datasets')
#     print('Done.')
