from __future__ import division

import imageRegion
import binarize
import segmentation
import cv2
from sklearn import svm
from sklearn.neural_network import MLPClassifier
import os
import copy
from sklearn.externals import joblib
import tflearn

TARGETS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
           'x', 'y', 'z', '+', '-', '*', '(', ')', '[', ']', '@', '#', '!', '_']

SIZE = 5


def getResizedImage(image):
    resized = cv2.resize(image, (20, 20), interpolation=cv2.INTER_AREA)
    #thresh = recognition.nonZero2DAverage(resized, 20, 20)
    #resized_binary = preprocessing.binarize(resized, threshold=thresh, copy=True)
    flattened_array = resized.flatten()
    return flattened_array


def writeToFile(targetFile, data):
    for ch in data:
        item = str(ch) + " "
        targetFile.write(item)
    targetFile.write("\n")


def includeTrainingSet(imageRegionSet, target):
    targetFile = open("trainingSet/" + target, "a")
    for imageRegion in imageRegionSet:
        image = imageRegion[0]
        data = getResizedImage(image)
        writeToFile(targetFile, data)


def trainingSetFromImage(trainImage, target):
    grayImage = binarize.toGrayScale(trainImage)
    binarizedImage = binarize.binarize(grayImage)

    tmpBinImage = copy.deepcopy(binarizedImage)
    height, width = binarizedImage.shape
    imageRegionSet = segmentation.segmentation(binarizedImage)

    i = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    for imageRegion in imageRegionSet:
        dim = imageRegion[2]
        (x, y, w, h) = dim
        cv2.rectangle(tmpBinImage, (x, height - y - h), (x + w, height - y), (255, 255, 255), 2)
        cv2.putText(tmpBinImage, str(i), (x, height - y - h - 20), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        i = i + 1

    cv2.imshow("Training Image", tmpBinImage)
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()

    print 'Number of Segments : ' + str(len(imageRegionSet))
    while True:
        print "(i)Include Training Set (r)Retry (q)Quit"
        option = str(raw_input("Option : "))
        if option == 'q':
            break
        elif option == 'i':
            includeTrainingSet(imageRegionSet, target)
            break
        elif option == 'r':
            break

    return option


def generateTrainingSet():
    print "Generate Training Set"
    option = 'n'

    while option != 'q':
        target = str(raw_input("Enter target : "))
        if target == 'q':
            break
        trainImageName = str(raw_input("Enter the training image file number: "))
        if trainImageName == 'q':
            break
        fileName = "trainImages" + "/" + target + "/" + trainImageName + ".png"
        print fileName
        if os.path.isfile(fileName):
            trainImage = cv2.imread(fileName)
            option = trainingSetFromImage(trainImage, target)
        else:
            print 'Invalid file name'
            continue


def getTargetCount():
    count = 0
    for fileName in TARGETS:
        if os.path.isfile('trainingSet/' + fileName):
            count = count + 1
    return count


def createNNModel(inputNodeCount, outputNodeCount):
    net = tflearn.input_data(shape=[None, 400])
    net = tflearn.fully_connected(net, inputNodeCount / 2)
    net = tflearn.fully_connected(net, inputNodeCount / 4)
    net = tflearn.fully_connected(net, inputNodeCount / 8)
    net = tflearn.fully_connected(net, outputNodeCount, activation='softmax')
    net = tflearn.regression(net)
    model = tflearn.DNN(net)
    return model


def neuralNetTrain(data, target):
    floatTarget = []
    for t in target:
        floatTarget.append(float(ord(t)))
    inputNodeCount = len(data[0])
    outputNodeCount = getTargetCount()
    nnModel = createNNModel(inputNodeCount, outputNodeCount)
    nnModel.fit(data, floatTarget, n_epoch=1000, batch_size=100, show_metric=True)
    nnModel.save('classifiers/neuralNet')


def mlpTrain(data, target):
    clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(100,), random_state=1, max_iter=1000)
    clf.fit(data, target)
    print clf
    joblib.dump(clf, 'classifiers/mlp.pkl')


def linearSvcTrain(data, target):
    classifier = svm.LinearSVC()
    classifier.fit(data, target)
    print classifier
    joblib.dump(classifier, 'classifiers/linearSVC.pkl')


def getDataFromFile(fileName):
    targetFile = open('trainingSet/' + fileName)
    data = []
    target = []
    for line in targetFile:
        items = line.split()
        row = map(int, items)
        data.append(row)
        target.append(fileName)
    return data, target


def train():
    data = []
    target = []
    for fileName in TARGETS:
        if os.path.isfile('trainingSet/' + fileName):
            print 'Got training set for  : ' + fileName
            dataTmp, targetTmp = getDataFromFile(fileName)
            data = data + dataTmp
            target = target + targetTmp
    while True:
        print 'Choose classifier to train'
        print '(s) Linear SVM (n) Neural Network (q) Quit'
        option = str(raw_input('Option : '))
        if option == 's':
            linearSvcTrain(data, target)
        elif option == 'n':
            mlpTrain(data, target)
        elif option == 'q':
            break
        else:
            print 'Sorry, invalid option try again'

    print 'Training complete'


def getClassifier(type):
    if type == 'svm':
        return joblib.load('classifiers/linearSVC.pkl')
    elif type == 'nn':
        outputNodeCount = getTargetCount()
        model = createNNModel(400, outputNodeCount)
        model.load('classifiers/neuralNet')
        return model
    elif type == 'mlp':
        return joblib.load('classifiers/mlp.pkl')
