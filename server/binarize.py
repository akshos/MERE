from cv2 import threshold, THRESH_BINARY, THRESH_OTSU

#uses Otsu's thresholding to binarize the image.
#

##
#returns a binarized form of the input image
#argument : image object
##
def binarize(image):
	ret,binarizedImage = threshold(imgBlur, 0, 255, THRESH_BINARY + THRESH_OTSU)
	return binarizedImage


