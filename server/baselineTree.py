import imageRegion
import sys


def precedence(id):
    if id == '#':
        return -1
    if id == '(':
        return 0
    if id == '+' or id == '-':
        return 1
    if id == '*' or id == '/':
        return 2


def operate(op1, op2, ele):
    if ele == '+':
        return int(op1) + int(op2)
    if ele == '-':
        return int(op1) - int(op2)
    if ele == '*':
        return int(op1) * int(op2)


def evaluateSingleLevel(root):
    children = root.getChildren()
    postfix = []
    stack = []
    stack.append('#')
    for child in children:
        id = child.getSymbolID()
        if id.isdigit():
            postfix.append(id)
            continue
        if id == '(':
            stack.append(id)
            continue
        if id == ')':
            while stack[len(stack) - 1] != '(':
                postfix.append(stack.pop())
            stack.pop()
            continue
        while precedence(id) <= precedence(stack[len(stack) - 1]):
            postfix.append(stack.pop())
        stack.append(id)
    while len(stack) > 1:
        postfix.append(stack.pop())
    print postfix
    for ele in postfix:
        if ele.isdigit():
            stack.append(ele)
        else:
            op1 = stack.pop()
            op2 = stack.pop()
            result = operate(op1, op2, ele)
            stack.append(result)

    print 'result = ', stack[1]


def sortSymbolsByMinX(symbolNodeList):
    symbolNodeList.sort(key=lambda x: x.getMinX())


def printSymbolNodeList(symbolNodeList):
    for symbolNode in symbolNodeList:
        print symbolNode.getSymbolID()


def addChildren(parent, children):
    for child in children:
        parent.addChild(child)


def buildBST(symbolNodeList):
    root = imageRegion.imageRegion()
    root.setRegionLabel(imageRegion._EXPRESSION)
    if len(symbolNodeList) == 0:
        return root
    sortSymbolsByMinX(symbolNodeList)
    printSymbolNodeList(symbolNodeList)
    addChildren(root, symbolNodeList)
    #evaluateSingleLevel(root)
    return extractBaseLine(root)


def contains(snode1, snode2):
    if snode1 != snode2 and snode1.getClass() == imageRegion._ROOT:
        if snode1.getMinX <= snode2.getCentroidX() and snode2.getCentroidX < snode1.getMaxX():
            if snode1.getMinY() <= snode2.getCentroidY() and snode2.getCentroidY() < snode1.getMaxy():
                return True
    return False


def overlapCondition1(snode1, snode2):
    if snode2.getClass() in {imageRegion._OPENBRACKET, imageRegion._CLOSEBRACKET}:
        if (snode2.getMinY() <= snode1.getCentroidY()) and (snode1.getCentroidY() < snode2.getMaxY()):
            if snode2.getMinX() <= snode1.getMinX():
                return True
    return False


def overlapCondition2(snode1, snode2):
    if snode2.getClass() in {imageRegion._NONSCRIPTED, imageRegion._VARIABLERANGE}:
        if snode2.getWidth() > snode1.getWidth():
            return True
    return False


def overlaps(snode1, snode2):
    if snode1 != snode2:
        if snode1.getClass() == imageRegion._NONSCRIPTED:
            if snode1.getMinX() <= snode2.getCentroidX() and snode2.getCentroidX() <= snode1.getMaxX():
                if not contains(snode2, snode1):
                    if not overlapCondition1(snode1, snode2) and not overlapCondition2(snode1, snode2):
                        return True
    return False


def addAbove(snodeList, snode):
    addSymbolNodeListToRegion(snode, snodeList, imageRegion._ABOVE)


def addBelow(snodeList, snode):
    addSymbolNodeListToRegion(snode, snodeList, imageRegion._BELOW)


def addSuper(snodeList, snode):
    addSymbolNodeListToRegion(snode, snodeList, imageRegion._SUPER)


def addSubsc(snodeList, snode):
    addSymbolNodeListToRegion(snode, snodeList, imageRegion._SUBSC)


def addContains(snodeList, snode):
    addSymbolNodeListToRegion(snode, snodeList, imageRegion._CONTAINS)


def addTLeft(snodeList, snode):
    addSymbolNodeListToRegion(snode, snodeList, imageRegion._TLEFT)


def addBLeft(snodeList, snode):
    addSymbolNodeListToRegion(snode, snodeList, imageRegion._BLEFT)


def checkOverlap(snode, snodeList):
    maxWidth = 0
    widestNode = None
    for node in snodeList:
        if overlaps(snode, node) and snode != node:
            nodeWidth = node.getMaxX() - node.getMinX()
            if nodeWidth > maxWidth:
                widestNode = node
    if maxWidth == 0:
        return snode
    else:
        return widestNode


# def concatLists(snodeList1,snodeList2)

def hasNonEmptyRegion(snode, region_label):
    childNode = snode.getChildren()
    for child in childNode:
        childLabel = child.getRegionLabel()
        if childLabel == region_label and len(child.getChildren()) > 0:
            return True
        else:
            return False


def regularHorCondition1(snode1, snode2):
    if (snode1.getMaxY() <= snode2.getMaxY()):
        if snode1.getMinY() >= snode2.getMinY():
            return True
    else:
        return False


def regularHorCondition2(snode1, snode2):
    if snode2.getSymbolClass() == imageRegion._OPENBRACKET or snode2.getSymbolClass() == imageRegion._CLOSEBRACKET:
        if snode2.getMinY() <= snode1.getCentroidY():
            if snode1.getCentroidY() < snode2.getMaxY():
                return True
    else:
        return False


def isRegularHor(snode1, snode2):
    if isAdjacent(snode1, snode2) or regularHorCondition1(snode1, snode2) or regularHorCondition2(snode1, snode2):
        return True
    else:
        return False


def concatLists(snodeList1, snodeList2):
    return snodeList1 + snodeList2


def testRegion1(snode, symbolNode):
    if symbolNode.getMaxX() < snode.getMaxX():
        y = symbolNode.getCentroidY()
        if y > snode.getAboveThreshold():
            return imageRegion._ABOVE
        if y > snode.getSuperThreshold():
            return imageRegion._TLEFT
        if y < snode.getBelowThreshold():
            return imageRegion._BELOW
        if y < snode.getSubscThreshold():
            return imageRegion._BLEFT
    return imageRegion._NOREGION


def testRegion2(snode, symbolNode):
    if symbolNode.getCentroidX < snode.getMaxX():
        y = symbolNode.getCentroidY()
        if y > snode.getSuperThreshold():
            return imageRegion._SUPER
        if y < snode.getSubscThreshold():
            return imageRegion._SUBSC
    return imageRegion._NOREGION


def addSymbolNodeToRegion(snode, symbolNode, region):
    children = snode.getChildren()
    if len(children) != 0:
        for childRegion in children:
            if childRegion.getRegionLabel() == region:
                childRegion.addChild(symbolNode)
                return
    regionNode = imageRegion.imageRegion()
    regionNode.setRegionLabel(region)
    regionNode.addChild(symbolNode)
    snode.addChild(regionNode)


def addSymbolNodeListToRegion(snode, symbolNodeList, region):
    children = snode.getChildren()
    if len(children) != 0:
        for childRegion in children:
            if childRegion.getRegionLabel() == region:
                childRegion.addChildren(symbolNodeList)
                return
    regionNode = imageRegion.imageRegion()
    regionNode.setRegionLabel(region)
    regionNode.addChildren(symbolNodeList)
    snode.addChild(regionNode)


def partition(snodeList, snode):
    failedSnodeList = []
    for symbolNode in snodeList:
        region = testRegion1(snode, symbolNode)
        if region != imageRegion._NOREGION:
            addSymbolNodeToRegion(snode, symbolNode, region)
        else:
            failedSnodeList.append(symbolNode)
    return failedSnodeList


def partitionFinal(snodeList, snode):
    for symbolNode in snodeList:
        region = testRegion2(snode, symbolNode)
        if region == imageRegion._NOREGION:
            print 'error in partition final : no region'
            sys.exit(1)
        addSymbolNodeToRegion(snode, symbolNode, region)


def hor(snodeList1, snodeList2):
    if len(snodeList2) == 0:
        return snodeList1
    currentSymbol = snodeList1[-1]
    remainingSymbols = partition(snodeList2, currentSymbol)
    if len(remainingSymbols) == 0:
        return snodeList1
    if currentSymbol.getClass() == imageRegion._NONSCRIPTED:
        return hor(concatLists(snodeList1, [start(remainingSymbols)]), remainingSymbols)
    sl = remainingSymbols[:]
    while len(sl) != 0:
        l = sl[0]
        if isRegularHor(currentSymbol, l):
            return hor(concatLists(snodeList1, [checkOverlap(l, remainingSymbols)]), remainingSymbols)
        del sl[0]
    partitionFinal(remainingSymbols, currentSymbol)
    return concatLists(snodeList1, [currentSymbol])


def getRegionNode(snode, regionLabel):
    children = snode.getChildren()
    for child in children:
        if child.getRegionLabel() == regionLabel:
            return child
    return None


def removeRegions(regionLabelList, snode):
    children = snode.getChildren()
    for child in children:
        if child.getRegionLabel() in regionLabelList:
            snode.removeChild(child)


def partitionSharedRegion(regionLabel, snode1, snode2):
    if regionLabel == imageRegion._TLEFT:
        rnode = getRegionNode(snode1, regionLabel)
        if rnode == None:
            print 'In partition shared region TLEFT case : getRegionNode returned None'
        symbolNodeList = rnode.getChildren()
        snodeList1 = []
        i = 0
        if snode1.getClass() == imageRegion._NONSCRIPTED:
            snodeList1 = []
        elif snode2.getClass() != imageRegion._VARIABLERANGE or (
                snode2.getClass() == imageRegion._VARIABLERANGE and hasNonEmptyRegion(snode2,
                                                                                      imageRegion._ABOVE) == False):
            snodeList1 = symbolNodeList
        elif snode2.getClass() == imageRegion._VARIABLERANGE and hasNonEmptyRegion(snode2, imageRegion._ABOVE):
            for symbolNode in symbolNodeList:
                if isAdjacent(symbolNode, snode2):
                    snodeList1.append(symbolNode)
                    i = i + 1
                else:
                    break
        return snodeList1, symbolNodeList[i:]
    elif regionLabel == imageRegion._BLEFT:
        rnode = getRegionNode(snode1, regionLabel)
        if rnode == None:
            print 'In partition shared region TLEFT case : getRegionNode returned None'
        symbolNodeList = rnode.getChildren()
        snodeList1 = []
        i = 0
        if snode1.getClass() == imageRegion._NONSCRIPTED:
            snodeList1 = []
        elif snode2.getClass() != imageRegion._VARIABLERANGE or (
                snode2.getClass() == imageRegion._VARIABLERANGE and hasNonEmptyRegion(snode2,
                                                                                      imageRegion._BELOW) == False):
            snodeList1 = symbolNodeList
        elif snode2.getClass() == imageRegion._VARIABLERANGE and hasNonEmptyRegion(snode2, imageRegion._BELOW):
            for symbolNode in symbolNodeList:
                if isAdjacent(symbolNode, snode2):
                    snodeList1.append(symbolNode)
                    i = i + 1
                else:
                    break
        return snodeList1, symbolNodeList[i:]


def mergeRegions(regionLabelList, regionLabel, snode):
    regionNodeList = snode.getChildren()
    for region in regionNodeList:
        if region.getRegionLabel() in regionLabelList:
            snodeList = region.getChildren()
            snode.removeChild(region)
            addSymbolNodeListToRegion(snode, snodeList, regionLabel)


def collectRegions(snodeList):
    if len(snodeList) == 0:
        return snodeList
    s1 = snodeList[0]
    snodeList2 = snodeList[:]
    del snodeList2[0]
    if len(snodeList2) > 1:
        s2 = snodeList[1]
        superList, tleftList = partitionSharedRegion(imageRegion._TLEFT, s1, s2)
        addSuper(superList, s1)
        removeRegions([imageRegion._TLEFT], s2)
        addTLeft(tleftList, s2)
    if s1.getClass() == imageRegion._VARIABLERANGE:
        upperList = [imageRegion._TLEFT, imageRegion._ABOVE, imageRegion._SUPER]
        mergeRegions(upperList, imageRegion._UPPER, s1)
    return concatLists([s1], collectRegions(snodeList2))


def isAdjacent(snode1, snode2):
    if snode2.getClass() != imageRegion._NONSCRIPTED and snode1 != snode2:
        if snode2.getSubscThreshold() <= snode1.getCentroidY() and snode1.getCentroidY() < snode2.getSuperThreshold():
            return True
    return False


def start(snodeList):
    length = len(snodeList)
    if length == 1:
        return snodeList[0]
    snode1 = snodeList[length - 1]
    snode2 = snodeList[length - 2]
    if overlaps(snode1, snode2) or contains(snode1, snode2) or (
            snode1.getClass() == imageRegion._VARIABLERANGE and not (isAdjacent(snode2, snode1))):
        del snodeList[length - 2]
    else:
        del snodeList[length - 1]
    return start(snodeList)


def extractBaseLine(rnode):
    snodeList = rnode.getChildren()
    if len(snodeList) <= 1:
        return rnode
    startSymbol = start(snodeList[:])
    baselineSymbols = hor([startSymbol], snodeList)
    updatedBaseline = collectRegions(baselineSymbols)
    rnode.replaceChildren(updatedBaseline)
    for symbolNode in updatedBaseline:
        regionList = symbolNode.getChildren()
        for regionNode in regionList:
            extractBaseLine(regionNode)
    return rnode
