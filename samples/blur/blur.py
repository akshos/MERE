import cv2

img = cv2.imread('blurtest.png')
imgBlur = cv2.GaussianBlur(img,(5,5),0)
cv2.imwrite('restult.png', imgBlur)
