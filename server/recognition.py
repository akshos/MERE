import imageRegion
from PIL import Image
import cv2
from sklearn.externals import joblib
import matplotlib.pyplot as plt


def nonZero2DAverage(array, rlen, clen):
    total = 0
    count = 0
    for i in range(0, rlen):
        for j in range(0, clen):
            if (array[i][j] != 0):
                total = total + array[i][j]
                count = count + 1
    avg = total / count
    return avg


def symbolRecognition(symbolNodeList):
    classifier = joblib.load('classifiers/linearSVC.pkl')
    for symbolNode in symbolNodeList:
        data = symbolNode.getSymbolData()
        result = classifier.predict([data])
        symbolNode.setId(str(result[0]))
    return symbolNodeList
