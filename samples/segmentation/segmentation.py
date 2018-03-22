import cv2

image = cv2.imread("image2.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
res, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
res, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

i = 1
for contour in contours:
	[x,y,w,h] = cv2.boundingRect(contour)
	if w < 20 and h < 20:
		continue
	cv2.imwrite(str(i)+".jpg", thresh[y:y+h,x:x+w])
	i = i + 1

