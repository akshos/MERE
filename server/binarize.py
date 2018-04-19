from cv2 import threshold, THRESH_BINARY_INV, THRESH_OTSU, cvtColor, COLOR_BGR2GRAY


# uses Otsu's thresholding to binarize the image.
#

##
# convert RGB image to gray scale
##
def toGrayScale(image):
    print 'Converting image to grayscale : ',
    gray = cvtColor(image, COLOR_BGR2GRAY)
    print 'done'
    return gray


##
# returns a binarized form of the input image using otsu thresholding
# image will have back backgound with white foreground features
# argument : image object
##
def binarize(image):
    print 'Binarizing the image : ',
    ret, binarizedImage = threshold(image, 0, 255, THRESH_BINARY_INV + THRESH_OTSU)
    print 'done'
    return binarizedImage
