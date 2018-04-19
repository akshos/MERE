import sys

_SYMBOL_NODE = 1
_REGION_NODE = 2

_NOREGION = -1
_ABOVE = 1
_BELOW = 2
_SUBSC = 3
_SUPER = 4
_UPPER = 5
_LOWER = 6
_TLEFT = 7
_BLEFT = 8
_CONTAINS = 9
_EXPRESSION = 0

_NONSCRIPTED = 0
_OPENBRACKET = 1
_ROOT = 2
_VARIABLERANGE = 3
_ASCENDER = 4
_DESCENDER = 5
_CENTERED = 6
_CLOSEBRACKET = 7

_NONSCRIPTED_SYMBOLS = ['+', '-', '=', '*', '_']
_OPENBRACKET_SYMBOLS = ['(', '[']
_ASCENDER_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
_CLOSEBRACKET_SYMBOLS = [')', '[']


def createSymbolNodes(segmentList):
    symbolNodeList = []
    for segment in segmentList:
        symbolNode = imageRegion()
        symbolNode.setSymbolNode(segment[0], segment[1], segment[2])
        symbolNode.calculateCentroid()
        symbolNodeList.append(symbolNode)
    return symbolNodeList


def assignThresholds(symbolNode, symbolClass):
    t = 0
    if symbolClass == _NONSCRIPTED:
        symbolNode.setBelowThreshold(0.5 * symbolNode.getHeight())
        symbolNode.setAboveThreshold(0.5 * symbolNode.getHeight())
    elif symbolClass == _OPENBRACKET:
        symbolNode.setAboveThreshold(symbolNode.getHeight())
        symbolNode.setBelowThreshold(0)
    elif symbolClass == _ASCENDER or symbolClass == _CLOSEBRACKET:
        symbolNode.setBelowThreshold(t * symbolNode.getHeight())
        symbolNode.setAboveThreshold(symbolNode.getHeight() - (t * symbolNode.getHeight()))
        symbolNode.setSubscThreshold(t * symbolNode.getHeight())
        symbolNode.setSuperThreshold(symbolNode.getHeight() - (t * symbolNode.getHeight()))


def assignSymbolClasses(symbolNodeList):
    for symbolNode in symbolNodeList:
        id = symbolNode.getSymbolID()
        symbolClass = _CENTERED
        if id in _NONSCRIPTED_SYMBOLS:
            symbolClass = _NONSCRIPTED
        elif id in _OPENBRACKET_SYMBOLS:
            symbolClass = _OPENBRACKET
        elif id in _ASCENDER_SYMBOLS:
            symbolClass = _ASCENDER
        elif id in _CLOSEBRACKET_SYMBOLS:
            symbolClass = _CLOSEBRACKET
        symbolNode.setSymbolClass(symbolClass)
        assignThresholds(symbolNode, symbolClass)
    return symbolNodeList


class imageRegion:

    def __init__(self):
        self.regionFlag = _REGION_NODE
        self.children = []

    def setSymbolNode(self, image, data, dimensions):
        self.regionFlag = _SYMBOL_NODE
        self.symbolID = None
        self.symbolImage = image
        self.symbolData = data
        self.symbolX = dimensions[0]
        self.symbolY = dimensions[1]
        self.symbolWidth = dimensions[2]
        self.symbolHeight = dimensions[3]
        self.maxX = self.symbolX + self.symbolWidth
        self.maxY = self.symbolY + self.symbolHeight
        self.symbolCentroid = []
        self.symbolClass = None

    def setRegionLabel(self, regionLabel):
        if self.regionFlag == _REGION_NODE:
            self.regionLabel = regionLabel
        else:
            print 'ERROR : Assigning region label to symbol node type'
            sys.exit()

    def getRegionLabel(self):
        if self.regionFlag == _REGION_NODE:
            return self.regionLabel

    def getSymbolImage(self):
        return self.symbolImage

    def getSymbolData(self):
        return self.symbolData

    def getSymbolID(self):
        return self.symbolID

    def setSymbolClass(self, symbolClass):
        self.symbolClass = symbolClass

    def setId(self, id):
        self.symbolID = id

    def calculateCentroid(self):
        self.symbolCentroid.append(self.symbolY + self.symbolHeight / 2)
        self.symbolCentroid.append(self.symbolX + self.symbolWidth / 2)

    def setBelowThreshold(self, thresh):
        self.belowThreshold = self.symbolY + thresh

    def setAboveThreshold(self, thresh):
        self.aboveThreshold = self.symbolY + thresh

    def setSubscThreshold(self, thresh):
        self.subscThreshold = self.symbolY + thresh

    def setSuperThreshold(self, thresh):
        self.superThreshold = self.symbolY + thresh

    def getBelowThreshold(self):
        return self.belowThreshold

    def getAboveThreshold(self):
        return self.aboveThreshold

    def getSymbolClass(self):
        return self.symbolClass

    def getSubscThreshold(self):
        return self.subscThreshold

    def getSuperThreshold(self):
        return self.superThreshold

    def getCentroid(self):
        return self.symbolCentroid

    def getCentroidX(self):
        return self.symbolCentroid[1]

    def getCentroidY(self):
        return self.symbolCentroid[0]

    def addChild(self, child):
        self.children.append(child)

    def addChildren(self, children):
        self.children = self.children + children

    def getChildren(self):
        return self.children

    def getChild(self, index):
        return self.children[index]

    def getMaxX(self):
        return self.symbolX + self.symbolWidth

    def getMaxY(self):
        return self.symbolY + self.symbolHeight

    def getMinX(self):
        return self.symbolX

    def getMinY(self):
        return self.symbolY

    def getClass(self):
        return self.symbolClass

    def getWidth(self):
        return self.symbolWidth

    def getHeight(self):
        return self.symbolHeight

    def removeChild(self, child):
        self.children.remove(child)

    def replaceChildren(self, children):
        self.children = children
