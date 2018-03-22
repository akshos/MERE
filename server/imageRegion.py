import sys

_SYMBOL_NODE = 1
_REGION_NODE = 2

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

_NONSCRIPTED_SYMBOLS = ['+', '-', '=', '*', '_']
_OPENBRACKET_SYMBOLS = ['(', '[']
_DESCENDER_SYMBOLS = ['p', 'g', 'q', 'y', 'j']
_ASCENDER_SYMBOLS = ['b', 'd', 'h', 'k', 't']


def createSymbolNodes(segmentList):
	symbolNodeList = []
	for segment in segmentList:
		symbolNode = imageRegion()
		symbolNode.setSymbolNode(segment[0], segment[1], segment[2])
		symbolNode.calculateCentroid()
		symbolNodeList.append(symbolNode)
	return symbolNodeList


def assignSymbolClasses(symbolNodeList):
	for symbolNode in symbolNodeList:
		id = symbolNode.getSymbolID()
		symbolClass = _CENTERED
		if id in _NONSCRIPTED_SYMBOLS :
			symbolClass = _NONSCRIPTED
		elif id in _OPENBRACKET_SYMBOLS :
			symbolClass = _OPENBRACKET
		elif id in _ASCENDER_SYMBOLS :
			symbolClass = _ASCENDER
		elif id in _DESCENDER_SYMBOLS :
			symbolClass = _DESCENDER
		symbolNode.setSymbolClass(symbolClass)
	return symbolNodeList

class imageRegion:
	
	def __init__(self):
		self.regionFlag = _REGION_NODE
		self.children = []

	def setSymbolNode(self, image, data, dimensions ):
		self.regionFlag = _SYMBOL_NODE
		self.symbolID = None
		self.symbolImage = image
		self.symbolData = data
		self.symbolX = dimensions[0]
		self.symbolY = dimensions[1]
		self.symbolWidth = dimensions[2]
		self.symbolHeight = dimensions[3]
		self.symbolCentroid = []
		self.symbolClass = None
	
#	def __init__(self, regionFlag, regionLabel = None):
#		self.regionFlag = regionFlag
#		self.regionLabel = regionLabel
#		self.children = []
	
	def setRegionLabel(self, regionLabel):
		if( self.regionFlag == _REGION_NODE ):
			self.regionLabel = regionLabel
		else:
			print 'ERROR : Assigning region label to symbol node type'
			sys.exit()
	
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
		self.symbolCentroid.append(self.symbolHeight/2)
		self.symbolCentroid.append(self.symbolWidth/2)

	def getCentroid(self):
		return self.symbolCentroid

	def addChild(self, child):
		self.children.append(child)
	
	def getChildren(self):
		return self.children
	
	def getChild(self, index):
		return self.children[index]
	
	def getX(self):
		return self.symbolX
