import cv2
import numpy as np
from Common.functions import imreadgray
from Common.functions import flip

picture = 'sima'
img = imreadgray('../Common/' + picture + '.png')
flip(img)

print(img)

kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(img, kernel, iterations=1)
dilation = cv2.dilate(img, kernel, iterations=1)

print(erosion)
print(dilation)

