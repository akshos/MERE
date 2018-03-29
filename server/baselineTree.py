import imageRegion

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
            while stack[len(stack)-1] != '(':
                postfix.append(stack.pop())
            stack.pop()
            continue
        while precedence(id) <= precedence(stack[len(stack)-1]):
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
    symbolNodeList.sort(key=lambda x: x.getX() )

def printSymbolNodeList(symbolNodeList):
    for symbolNode in symbolNodeList:
        print symbolNode.getSymbolID()

def addChildren(parent, children):
    for child in children:
        parent.addChild(child)


def buildBST(symbolNodeList):
    root = imageRegion.imageRegion()
    root.setRegionLabel(imageRegion._EXPRESSION)
    if len(symbolNodeList) == 0 :
        return root
    sortSymbolsByMinX(symbolNodeList)
    printSymbolNodeList(symbolNodeList)
    addChildren(root, symbolNodeList)
    evaluateSingleLevel(root)
    return extractBaseLine(root)

def contains(snode1, snode2):
    if snode1 != snode2 and snode1.getClass() == imageRegion._ROOT:
        if snode1.getMinX <= snode2.getCentroidX() and snode2.getCentroidX < snode1.getMaxX():
            if snode1.getMinY() <= snode2.getCentroidY() and snode2.getCentroidY() < snode1.getMaxy():
                return True
    return False

def overlapCondition1(snode1, snode2):
    if snode2.getClass() in {imageRegion._OPENBRACKET, imageRegion._CLOSEBTACKET}:
        if snode2.getMinY() <= snode1.getCentroidY() and snode1.getCentroidY() < snode2.getMaxY():
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
                if not (contains(snode2, snode1)):
                    if not (overlapCondition1(snode1, snode2)) and not (overlapCondition2(snode1, snode2)):
                        return True
    return False

def start(snodeList):
    length = len(snodeList)
    if length == 1:
        return snodeList[0]
    snode1 = snodeList[length-1]
    snode2 = snodeList[length-2]
    if overlaps(snode1, snode2) or contains(snode1, snode2) or (snode1.getClass() == imageRegion._VARIABLERANGE and not(isAdjacent(snode2, snode1) ) ):
        del snodeList[length-2]
    else:
        del snodeList[length-1]
    return start(snodeList)

def extractBaseLine(rnode):
    snodeList = rnode.getChildren()
    if len(snodeList) <= 1:
        return rnode
    Sstart = start(snodeList[:])

