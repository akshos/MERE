import imageRegion
import binarize
import segmentation
from PIL import Image
import cv2
from sklearn import datasets
from sklearn import svm
from sklearn import preprocessing
import matplotlib.pyplot as plt
import recognition
import os.path
import copy
from sklearn.externals import joblib

TARGETS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
			'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
			'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w',
			'x', 'y', 'z', '+', '-', '*', '(', ')', '[', ']', '@', '#', '!' ]

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
	
def includeTrainingSet(imageRegionSet):
	tmp = getResizedImage( imageRegionSet[0][0] )
	
	target = str( raw_input("Enter target : ") )
	targetFile = open("trainingSet/"+target, "a")
	
	for imageRegion in imageRegionSet:
		image = imageRegion[0]
		data = getResizedImage(image)
		writeToFile(targetFile, data)

def generateTrainingSet():
	print "Generate Training Set"
	option = 'n'
	
	while( option != 'q' ):
		trainImageName = str(raw_input("Enter the training image file name (with extension): "))
		if trainImageName == 'q':
			break
		trainImage = cv2.imread("trainImages/"+trainImageName)
		grayImage = binarize.toGrayScale(trainImage)
		binarizedImage = binarize.binarize(grayImage)
		
		#segmentation
		res, contours, hierarchy = cv2.findContours(binarizedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		tmpBinImage = copy.deepcopy(binarizedImage)
		imageRegionSet = []
	
		i = 1
		font = cv2.FONT_HERSHEY_SIMPLEX
		for contour in contours:
			[x,y,w,h] = cv2.boundingRect(contour)
			if w < 10 and h < 10:
				continue 
			region = binarizedImage[y:y+h,x:x+w]
			imageRegionSet.append( (region,(x,y,w,h) ) )
			cv2.rectangle(tmpBinImage, (x, y), (x+w,y+h), (255,255,255), 2)
			cv2.putText(tmpBinImage, str(i) ,(x , y-20), font, 0.4,(255,255,255),1,cv2.LINE_AA)
			i = i + 1
						
		cv2.imshow("Training Image", tmpBinImage)
		k = cv2.waitKey(0)
		cv2.destroyAllWindows()
		
		cv2.imwrite("test.png", imageRegionSet[0][0])
		
		print 'Number of Segments : ' + str( len(imageRegionSet) )
		while True:
			print "(i)Include Training Set (r)Retry (q)Quit"
			option = str(raw_input("Option : "))
			if option == 'q':
				break
			elif option == 'i':
				includeTrainingSet(imageRegionSet)
				break
			elif option == 'r':
				break

def linearSvcTrain(data, target):
	classifier = svm.LinearSVC()
	classifier.fit(data, target)
	joblib.dump(classifier, 'classifiers/linearSVC.pkl') 
		
def getDataFromFile(fileName):
	targetFile = open('trainingSet/'+fileName)
	data = []
	target = []
	for line in targetFile:
		items = line.split();
		row = map( int, items )
		data.append(row)
		target.append(fileName)
	return data, target
		
def train():
	data = []
	target = []
	index = 0
	
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
	
	
	
	
			
