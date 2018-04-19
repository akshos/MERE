import imageRegion
from cv2 import findContours, imwrite, RETR_EXTERNAL, CHAIN_APPROX_NONE, boundingRect
import os
import learning


def deleteSegments():
    folder = 'segments'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def segmentation(image):
    print 'Segmenting the image : '
    print 'Deleting any previous segments'
    height, width = image.shape
    deleteSegments()
    segmentList = []
    res, contours, hierarchy = findContours(image, RETR_EXTERNAL, CHAIN_APPROX_NONE)
    i = 1
    for contour in contours:
        [x, y, w, h] = boundingRect(contour)
        if w < 30 and h < 30:
            continue
        region = image[y:y + h, x:x + w]
        data = learning.getResizedImage(region)
        segmentList.append((region, data, (x, height-y-h, w, h)))
        imwrite("segments/" + str(i) + ".png", region)
        i = i + 1
    return segmentList
