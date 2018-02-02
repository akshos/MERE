import imageRegion
from cv2 import findContours, imwrite, RETR_EXTERNAL, CHAIN_APPROX_NONE, boundingRect

def segmentation(image):
	print 'Segmenting the image : ',
	segments = []
	res, contours, hierarchy = findContours(image, RETR_EXTERNAL, CHAIN_APPROX_NONE)
	i = 1
	for contour in contours:
		[x,y,w,h] = boundingRect(contour)
		if w < 20 and h < 20:
			continue
		region = image[y:y+h,x:x+w]
		
		imwrite(str(i)+".jpg", region)
		i = i + 1
		
		segment = imageRegion.imageRegion()
		segment.setSymbolNode(region, x, y, w, h)
		segments.append(region)
	print 'done'
	return segments
