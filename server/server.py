import imageRegion, binarize, segmentation, recognition, learning
import cv2
from sklearn.externals import joblib

def test():
	imageFileName = str( raw_input('Enter image file name : ') )
	image = cv2.imread("testImages/"+imageFileName)
	
	grayImage = binarize.toGrayScale(image)
	binarizedImage = binarize.binarize(grayImage)
	
	res, contours, hierarchy = cv2.findContours(binarizedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
	for contour in contours:
		[x,y,w,h] = cv2.boundingRect(contours[0])
		if x < 20 and y < 20 :
			continue
		else:
			region = binarizedImage[y:y+h,x:x+w]
			break
	
	cv2.imshow('test', region)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	testData = learning.getResizedImage(region)
	classifier = joblib.load('classifiers/linearSVC.pkl') 
	print classifier.predict([testData])

def main():
	option = 'n'
	while option != 'q':
		print '\nMAIN MENU'
		print '(t)Train (g)Generate Training Set (e)Test (q)Quit'
		option = str(raw_input('Option: '))
		if option == 'q':
			break
		elif option == 't':
			learning.train()
		elif option == 'g':
			learning.generateTrainingSet()
		elif option == 'e':
			test()
		
			


main()
