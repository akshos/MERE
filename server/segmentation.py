import imageRegion
from cv2 import findContours, imwrite, RETR_EXTERNAL, CHAIN_APPROX_NONE, boundingRect

SEG_PADDING = 8

def segmentation(image):
	print 'Segmenting the image : ',
	segments = []
	res, contours, hierarchy = findContours(image, RETR_EXTERNAL, CHAIN_APPROX_NONE)
	i = 1
	for contour in contours:
		[x,y,w,h] = boundingRect(contour)
		if w < 20 and h < 20:
			continue
		region = image[y-10:y+h+10,x-10:x+w+10]
		
		imwrite("segments/"+str(i)+".jpg", region)
		i = i + 1
		
		segment = imageRegion.imageRegion()
		segment.setSymbolNode(region, x, y, w, h)
		segments.append(segment)
	print 'done'
	return segments
