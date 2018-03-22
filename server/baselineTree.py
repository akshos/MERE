import imageRegion

def sortSymbolsByMinX(symbolNodeList):
    symbolNodeList.sort(key=lambda x: x.getX() )

def printSymbolNodeList(symbolNodeList):
    for symbolNode in symbolNodeList:
        print symbolNode.getSymbolID()

def addChildren(parent, children):
    for child in children:
        parent.addChild(child)


def buildBST(symbolNodeList):
    print 'in progress'
    root = imageRegion.imageRegion()
    root.setRegionLabel(imageRegion._EXPRESSION)
    if len(symbolNodeList) == 0 :
        return root
    sortSymbolsByMinX(symbolNodeList)
    printSymbolNodeList(symbolNodeList)
    addChildren(root, symbolNodeList)
    return extractBaseLine(root)

def extractBaseLine(rnode):
    print 'comming soon'
    