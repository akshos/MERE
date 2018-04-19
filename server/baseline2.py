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
    if id == '^':
        return 3


def operate(op1, op2, ele):
    if ele == '+':
        print op1, '+', op2
        return float(op1) + float(op2)
    if ele == '-':
        print op1, '-', op2
        return float(op1) - float(op2)
    if ele == '*':
        print op1, '*', op2
        return float(op1) * float(op2)
    if ele == '^':
        print op1, '^', op2
        return pow(float(op1), float(op2))
    if ele == '/':
        print op1, '/', op2
        return float(op1) / float(op2)


def evaluateInfixExpression(infix):
    postfix = []
    stack = ['#']
    prevId = ''
    for id in infix:
        if id.isdigit():
            if prevId.isdigit():
                num = int(postfix[-1])
                num = (num * 10) + int(id)
                postfix[-1] = str(num)
            else:
                postfix.append(id)
        elif id == '(':
            stack.append(id)
        elif id == ')':
            while stack[len(stack) - 1] != '(':
                postfix.append(stack.pop())
            stack.pop()
        else:
            while precedence(id) <= precedence(stack[len(stack) - 1]):
                postfix.append(stack.pop())
            stack.append(id)
        prevId = id
    while len(stack) > 1:
        postfix.append(stack.pop())
    print postfix
    for ele in postfix:
        if ele.isdigit():
            stack.append(ele)
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            result = operate(op1, op2, ele)
            stack.append(result)

    return stack[1]


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
    extractBaseline(root, symbolNodeList)
    return root


def verticalOverlap(snode1, snode2):
    if snode2.getMaxY() > snode1.getMinY() and snode2.getMinY() < snode1.getMaxY():
        return True

def isAdjacent(snode1, snode2):
    if snode1.getClass() == imageRegion._NONSCRIPTED:
        if snode2.getClass() == imageRegion._NONSCRIPTED:
            if verticalOverlap(snode1, snode2) or verticalOverlap(snode2, snode1):
                return True
        if snode2.getBelowThreshold() < snode1.getCentroidY() < snode2.getAboveThreshold():
            return True
    else:
        if snode1.getBelowThreshold() < snode2.getCentroidY() < snode1.getAboveThreshold():
            return True
    return False


def findRegion(snode1, snode2):
    if snode1.getClass() in (imageRegion._NONSCRIPTED, imageRegion._VARIABLERANGE):
        if snode2.getCentroidY() > snode1.getAboveThreshold():
            return imageRegion._ABOVE
        elif snode2.getCentroidY() < snode1.getBelowThreshold():
            return imageRegion._BELOW
    else:
        if snode2.getCentroidY() > snode1.getSuperThreshold():
            return imageRegion._SUPER
        elif snode2.getCentroidY() < snode1.getSubscThreshold():
            return imageRegion._SUBSC


def findNextBaselineSymbol(snode, symbolNodeList, i):
    while i < len(symbolNodeList):
        currSymbolNode = symbolNodeList[i]
        if isAdjacent(snode, currSymbolNode):
            break
        i = i+1
    return i


def partition(snode, snodeList):
    upperList = []
    lowerList = []
    upperRegion = imageRegion._NOREGION
    lowerRegion = imageRegion._NOREGION
    for s in snodeList:
        if isAdjacent(snode, s):
            break
        regionLabel = findRegion(snode, s)
        if regionLabel in (imageRegion._SUBSC, imageRegion._BELOW):
            lowerRegion = regionLabel
            lowerList.append(s)
        elif regionLabel in(imageRegion._SUPER, imageRegion._ABOVE):
            upperRegion = regionLabel
            upperList.append(s)
    return lowerList, upperList, lowerRegion, upperRegion


def createRegion(regionLabel):
    rnode = imageRegion.imageRegion()
    rnode.setRegionLabel(regionLabel)
    return rnode


def addRegionNode(snode, regionLabel):
    rnodeList = snode.getChildren()
    if len(rnodeList) != 0:
        for rnode in rnodeList:
            if rnode.getRegionLabel() == regionLabel:
                return rnode
    rnode = createRegion(regionLabel)
    snode.addChild(rnode)
    return rnode


def extractBaseline(rnode, symbolNodeList):
    if len(symbolNodeList) == 0:
        return
    prevSymbolNode = symbolNodeList[0]
    rnode.addChild(prevSymbolNode)
    i = 1
    length = len(symbolNodeList)
    while i < length:
        currSymbolNode = symbolNodeList[i]
        if isAdjacent(prevSymbolNode, currSymbolNode):
            rnode.addChild(currSymbolNode)
            prevSymbolNode = currSymbolNode
            i = i + 1
            continue
        else:
            j = findNextBaselineSymbol(prevSymbolNode, symbolNodeList, i+1)
            lowerList, upperList, lowerRegion, upperRegion = partition(prevSymbolNode, symbolNodeList[i:j])
            if len(lowerList) != 0:
                regionNode = addRegionNode(prevSymbolNode, lowerRegion)
                extractBaseline(regionNode, lowerList)
            if len(upperList) != 0:
                regionNode = addRegionNode(prevSymbolNode, upperRegion)
                extractBaseline(regionNode, upperList)
            i = j


def hasChildren(node):
    children = node.getChildren()
    if len(children) == 0:
        return False
    return True


def checkDivisionValidity(nodeList):
    if len(nodeList) == 2:
        if nodeList[0].getRegionLabel() == imageRegion._BELOW:
            if nodeList[1].getRegionLabel() == imageRegion._ABOVE:
                return
    print 'error division validity check failed'
    sys.exit(1)


def parseTree(root):
    output = ''
    children = root.getChildren()
    for snode in children:
        symbolId = snode.getSymbolID()
        if symbolId.isdigit() or symbolId in (')', ']'):
            output = output + symbolId
            if hasChildren(snode):
                superRegion = snode.getChildren()[0]
                if superRegion.getRegionLabel() == imageRegion._SUPER:
                    output = output + '^('
                    output = output + parseTree(superRegion)
                    output = output + ')'
                else:
                    print 'error symbol ' + symbolId + ' has region : ' + superRegion.getRegionLabel()
                    sys.exit(1)
        elif symbolId == '-' and hasChildren(snode):
            children = snode.getChildren()
            checkDivisionValidity(children)
            output = output + '('
            output = output + parseTree(children[1]) #above symbols
            output = output + ')/('
            output = output + parseTree(children[0]) #below symbols
            output = output + ')'
        else:
            if symbolId in ('+', '-', '*', '/', '(', '['):
                output = output + symbolId
            else:
                print 'error undefined symbol'
                sys.exit(1)
    return output