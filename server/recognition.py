import pytesseract
import imageRegion
from PIL import Image
import cv2
from sklearn import datasets
from sklearn import svm
from sklearn import preprocessing
import matplotlib.pyplot as plt

def nonZero2DAverage(array, rlen, clen):
	total = 0
	count = 0
	for i in range(0, rlen):
		for j in range(0, clen):
			if( array[i][j] != 0 ):
				total = total + array[i][j]
				count = count + 1
	avg = total/count
	return avg
		
def recogTests(symbolNodes):
	resized = cv2.resize(symbolNodes[13].getSymbolImage(), (8,8), interpolation=cv2.INTER_AREA )	
	print resized
	thresh = nonZero2DAverage(resized, 8, 8)
	binr = preprocessing.binarize(resized, threshold=thresh, copy=True)
	binr = 1 - binr
	testImg = binr.flatten()
	print binr
	plt.imshow(resized, cmap=plt.cm.gray_r, interpolation='nearest')
	plt.show()
	plt.imshow(binr, cmap=plt.cm.gray_r, interpolation='nearest')
	plt.show()
	
	digits = datasets.load_digits()
	images = digits.images

	X = []
	y = digits.target

	for image in images:
		thresh = nonZero2DAverage(image, 8, 8)
		binr = preprocessing.binarize(image, threshold=thresh/2, copy=True)
		inv = 1-binr
		inv = inv.flatten()
		X.append(inv)
	
	clf = svm.SVC(gamma=0.001, C=100)
	clf.fit(X,y)
	print clf.predict([testImg])
	print y[1]


def symbolRecognition(segments):
	for segment in segments:
		image = segment.getSymbolImage()
#		cv2.imshow("Image : ", image)
#		cv2.waitKey(0)

		pilImage = Image.fromarray(image)

#		pilImage.show()
		symbol = pytesseract.image_to_string(pilImage)
		print 'symbol : ' , symbol
		segment.setId(symbol)
	return segments
