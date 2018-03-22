import imageRegion, binarize, segmentation, recognition, learning, baselineTree
import cv2
from sklearn.externals import joblib

def test():
	imageFileName = str( raw_input('Enter image file name : ') )
	image = cv2.imread("testImages/"+imageFileName)
	
	grayImage = binarize.toGrayScale(image)
	binarizedImage = binarize.binarize(grayImage)
	regions = []
	res, contours, hierarchy = cv2.findContours(binarizedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
	for contour in contours:
		[x,y,w,h] = cv2.boundingRect(contour)
		if h < 30 and w < 30 :
			continue
		else:
			regions.append( (binarizedImage[y:y+h,x:x+w], (x,y,w,h) ) )
	classifier = joblib.load('classifiers/linearSVC.pkl') 
	for region in regions:
		testData = learning.getResizedImage(region[0])
		(x,y,w,h)= region[1]
		result = classifier.predict([testData])
		cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,0), 2)
		cv2.putText(image, str(result[0]), (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1,cv2.LINE_AA)
		print result
	
	cv2.imshow('test', image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def standalone():
	print 'Started in Standalone mode'
	imageFileName = str(raw_input('Enter the image file name : '))
	image = cv2.imread(imageFileName)
	grayImage = binarize.toGrayScale(image)
	binarizedImage = binarize.binarize(grayImage)
	segmentList = []
	res, contours, hierarchy = cv2.findContours(binarizedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
	for contour in contours:
		[x,y,w,h] = cv2.boundingRect(contour)
		if h < 30 and w < 30 :
			continue
		else:
			data = learning.getResizedImage(binarizedImage[y:y+h,x:x+w])
			segment = ( binarizedImage[y:y+h,x:x+w], data, (x,y,w,h) )
			segmentList.append(segment)
	
	symbolNodeList = imageRegion.createSymbolNodes(segmentList)
	symbolNodeList = recognition.symbolRecognition(symbolNodeList)
	symbolNodeList = imageRegion.assignSymbolClasses(symbolNodeList)
	root = baselineTree.buildBST(symbolNodeList)

def main():
	option = 'n'
	while option != 'q':
		print '\nMAIN MENU'
		print '(s)Standalone Mode (t)Train (g)Generate Training Set (e)Test (q)Quit'
		option = str(raw_input('Option: '))
		if option == 'q':
			break
		elif option == 't':
			learning.train()
		elif option == 'g':
			learning.generateTrainingSet()
		elif option == 'e':
			test()
		elif option == 's':
			standalone()
		
main()
