import imageRegion, binarize, segmentation
from cv2 import imread

def test():
	image = imread("image2.png")
	grayImage = binarize.toGrayScale(image)
	binarizedImage = binarize.binarize(grayImage)
	symbolNodes = segmentation.segmentation(binarizedImage)
	

def main():
	test()


main()
