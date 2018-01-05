import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def grayScaleExample():
	img = mpimg.imread('image.png')     
	gray = rgb2gray(img)    
	plt.imshow(gray, cmap = plt.get_cmap('gray'))
	plt.show()
	
def binarizationExample():
	img = cv2.imread('imageGray.png',0)
	img = cv2.medianBlur(img,5)
	#img = rgb2gray(colorImg)
	ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
	ret,thresh2 = cv2.threshold(img,150,255,cv2.THRESH_BINARY_INV)
	ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
	thresh4 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
	thresh5 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

	titles = ['Original Image','BINARY','BINARY_INV','TRUNC','Adaptive Mean','Adaptive Gaussian']
	images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

	for i in xrange(6):
		plt.subplot(2,3,i+1),plt.imshow(images[i], cmap = plt.get_cmap('gray') )
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])

	plt.show()

def otsusMethod():
	img = cv2.imread('imageGray.png',0)

	# global thresholding
	ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

	# Otsu's thresholding
	ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	# Otsu's thresholding after Gaussian filtering
	blur = cv2.GaussianBlur(img,(5,5),0)
	ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	# plot all the images and their histograms
	images = [img, 0, th1,
		      img, 0, th2,
		      blur, 0, th3]
	titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
		      'Original Noisy Image','Histogram',"Otsu's Thresholding",
		      'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]

	for i in xrange(3):
		plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
		plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
		plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
		plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
		plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
		plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
	plt.show()

#grayScaleExample()	
#binarizationExample()
otsusMethod()
