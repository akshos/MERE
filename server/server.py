#!/usr/bin/python2

import imageRegion, binarize, segmentation, recognition, learning, baselineTree, baseline2
import cv2
import os
import socket


svm_nn = 'svm'


def test(imageFileName, image=None, flag=0):
    if flag == 0:
        image = getImage(imageFileName)
    grayImage = binarize.toGrayScale(image)
    binarizedImage = binarize.binarize(grayImage)
    cv2.imshow('image', binarizedImage)
    regions = []
    res, contours, hierarchy = cv2.findContours(binarizedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        if h < 30 and w < 30:
            continue
        else:
            regions.append((binarizedImage[y:y + h, x:x + w], (x, y, w, h)))
    classifier = learning.getClassifier(svm_nn)
    for region in regions:
        testData = learning.getResizedImage(region[0])
        (x, y, w, h) = region[1]
        result = classifier.predict([testData])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 2)
        cv2.putText(image, str(result[0]), (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
        print result
    cv2.imshow('test', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def getImage(imageFileName):
    if not os.path.isfile(imageFileName):
        print 'ERROR : Cannot load the given file'
        return None
    image = cv2.imread(imageFileName)
    return image


def preprocess(image):
    height, width, channels = image.shape
    grayImage = binarize.toGrayScale(image)
    binarizedImage = binarize.binarize(grayImage)
    segmentList = segmentation.segmentation(binarizedImage)
    return segmentList


def standalone(imageFileName, image = None, flag = 0):
    if flag == 0:
        image = getImage(imageFileName)
    # preprocess and segment the image, returns segment list
    segmentList = preprocess(image)
    # create symbol nodes with the segments
    symbolNodeList = imageRegion.createSymbolNodes(segmentList)
    # recognize symbols represented by each segment
    symbolNodeList = recognition.symbolRecognition(symbolNodeList)
    # assign symbol classes
    symbolNodeList = imageRegion.assignSymbolClasses(symbolNodeList)
    # create BST
    bstRoot = baseline2.buildBST(symbolNodeList)
    output = ''
    output = baseline2.parseTree(bstRoot)
    print 'OUTPUT : ' + output
    result = baseline2.evaluateInfixExpression(output)
    print '==========================================='
    print 'RESULT: ', result
    print '===========================================\n'



def receiveFile(clientConnection):
    fileName = str(clientConnection.recv(1024))
    fileName = fileName.rstrip()
    fileName = fileName + '.jpg'
    fileName = 'received/' + fileName
    print 'Image file Name : ' + str(fileName)
    saveFile = open(fileName, 'wb')
    recvData = clientConnection.recv(1024)
    print 'Receiving file......'
    while recvData:
        saveFile.write(recvData)
        recvData = clientConnection.recv(1024)
    print 'File saved as ' + fileName
    clientConnection.close()
    saveFile.close()
    image = cv2.imread(fileName)
    image = cv2.resize(image, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("received/curr.png", image)
    fileName = 'received/curr.png'
    return fileName;


refPt = []
cropping = False
cropped = False


def clickCrop(event, x, y, flags, param):
    global refPt, cropping, cropped
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
        cropped = False
        print 'crop start'
    elif event == cv2.EVENT_LBUTTONUP and cropping == True:
        refPt.append((x, y))
        cropping = False
        cropped = True
        print 'crop end'


def processReceivedFile(imageFileName):
    image = getImage(imageFileName)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", clickCrop)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    global cropped
    if cropped == True:
        cropped = False
        cv2.rectangle(clone, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", clone)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        image = image[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    while True:
        print '(t)Test (e)Evaluate (q)Quit'
        option = str(raw_input("Option: "))
        if option == 't':
            tmp = image.copy()
            test(imageFileName, tmp, 1)
        elif option == 'e':
            tmp = image.copy()
            standalone(imageFileName, tmp, 1)
        elif option == 'q':
            break


def server():
    serverSocket = socket.socket()
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    host = "192.168.2.31"
    port = 1234
    serverSocket.bind((host, port))
    print 'Server started bind to : ', host, ' port : ', port
    try:
        while True:
            print 'Waiting for clients....'
            serverSocket.listen(2)
            clientConnection, clientAddress = serverSocket.accept()
            print "Received Connection from : ", clientAddress
            msg = clientConnection.recv(1024)
            print 'Received : ', unicode(msg)
            fileName = receiveFile(clientConnection)
            print 'Processing image...'
            clientConnection.close()
            processReceivedFile(fileName)
    except KeyboardInterrupt:
        print 'Received terminate signal'
    finally:
        serverSocket.shutdown(socket.SHUT_RDWR)
        serverSocket.close()


def changeClassifier():
    print '(s)SVC (m)MLP'
    option = str(raw_input("Option: "))
    global svm_nn
    if option == 's':
        svm_nn = 'svm'
    if option == 'm':
        svm_nn = 'mlp'


def main():
    option = 'n'
    print '---------------------------------------------------'
    print 'MATHEMATICAL EXPRESSION RECOGNITION AND EVALUATION'
    print '---------------------------------------------------'
    while option != 'q':
        print 'Main Menu (Classifier: ' + svm_nn + ')'
        print '(s)Standalone Mode \n(S)Server Mode \n(t)Train \n(g)Generate Training Set \n(e)Test \n(c)Change Classifier \n(q)Quit'
        option = str(raw_input('Option: '))
        if option == 'q':
            break
        elif option == 't':
            learning.train()
        elif option == 'g':
            learning.generateTrainingSet()
        elif option == 'e':
            imageFileName = str(raw_input('Enter image file name : '))
            if imageFileName == 'q':
                continue
            test(imageFileName)
        elif option == 's':
            print 'Started in Standalone mode'
            imageFileName = str(raw_input('Enter image file name : '))
            if imageFileName == 'q':
                continue
            standalone(imageFileName)
        elif option == 'S':
            server()
        elif option == 'c':
            changeClassifier()
        else:
            print 'Please enter a valid option'


main()
