import imageRegion
import binarize
import segmentation
from PIL import Image
import cv2
import recognition
from sklearn import svm
from sklearn import preprocessing
import os
import copy
from sklearn.externals import joblib
import numpy as np

TARGETS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
			'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
			'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w',
			'x', 'y', 'z', '+', '-', '*', '(', ')', '[', ']', '@', '#', '!', '_' ]

SIZE = 5

def getResizedImage(image):
	resized = cv2.resize(image, (20,20), interpolation=cv2.INTER_AREA )
	thresh = recognition.nonZero2DAverage(resized, 20, 20)
	resized_binary = preprocessing.binarize(resized, threshold=thresh, copy=True)
	flattened_array = resized_binary.flatten()	
	return flattened_array 

def writeToFile( targetFile, data ):
	for ch in data:
		item = str(ch) + " "
		targetFile.write(item)
	targetFile.write("\n") 
	
def includeTrainingSet(imageRegionSet, target):
	#tmp = getResizedImage( imageRegionSet[0][0] )
	targetFile = open("trainingSet/"+target, "a")
	for imageRegion in imageRegionSet:
		image = imageRegion[0]
		data = getResizedImage(image)
		writeToFile(targetFile, data)

def trainingSetFromImage(trainImage, target):
	grayImage = binarize.toGrayScale(trainImage)
	binarizedImage = binarize.binarize(grayImage)
	
	tmpBinImage = copy.deepcopy(binarizedImage)
	imageRegionSet = segmentation.segmentation(binarizedImage)

	i = 1
	font = cv2.FONT_HERSHEY_SIMPLEX
	for imageRegion in imageRegionSet:
		dim = imageRegion[1]
		(x, y, w, h) = dim
		cv2.rectangle(tmpBinImage, (x, y), (x+w,y+h), (255,255,255), 2)
		cv2.putText(tmpBinImage, str(i) ,(x , y-20), font, 0.4,(255,255,255),1,cv2.LINE_AA)
		i = i+1
		
	cv2.imshow("Training Image", tmpBinImage)
	k = cv2.waitKey(0)
	cv2.destroyAllWindows()
			
	print 'Number of Segments : ' + str( len(imageRegionSet) )
	option = 'n'
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
	
	while( option != 'q' ):
		target = str( raw_input("Enter target : ") )
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

def neuralNetTrain(data, target):
	print 'Comming soon'

def linearSvcTrain(data, target):
	classifier = svm.LinearSVC()
	classifier.fit(data, target)
	joblib.dump(classifier, 'classifiers/linearSVC.pkl') 
		
def getDataFromFile(fileName):
	targetFile = open('trainingSet/'+fileName)
	data = []
	target = []
	for line in targetFile:
		items = line.split()
		row = map( int, items )
		data.append(row)
		target.append(fileName)
	return data, target
		
def train():
	data = []
	target = []
	for fileName in TARGETS:
		if( os.path.isfile('trainingSet/'+fileName) ):
			print 'Got training set for  : ' + fileName
			dataTmp, targetTmp = getDataFromFile(fileName)
			data = data + dataTmp
			target = target + targetTmp
	while True:
		print 'Choose classifier to train'
		print '(s) Linear SVM (n) Neural Network (q) Quit'
		option = str( raw_input('Option : ') )
		if option == 's':
			linearSvcTrain(data, target)
		elif option == 'n':
			neuralNetTrain(data, target)
		elif option == 'q':
			break
		else:
			print 'Sorry, invalid option try again'
	
	print 'Training complete'
	
	
	
	
			
