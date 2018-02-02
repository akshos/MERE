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


class imageRegion:
	
	def __init__(self):
		self.regionFlag = _REGION_NODE
		self.children = []		
	
	def setSymbolNode(self, image, sX, sY, sW, sH):
		self.regionFlag = _SYMBOL_NODE
		self.symbolIdentity = None
		self.symbolImage = image
		self.symbolX = sX
		self.symbolY = sY
		self.symbolWidth = sW
		self.symbolHeight = sH
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
