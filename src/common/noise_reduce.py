import cv2
from src.common.functions import imreadgray
from src.common.functions import flip

picture = 'chromosomemini'

img = imreadgray('../kang_et_al/results/' + picture + '.png')
img = flip(img)
size = img.shape

for row in range(0, size[0]):
    for col in range(0, size[1]):
        if img[row][col] < 50:
            img[row][col] = 0

flip(img)

cv2.imwrite('noise_reduced/' + picture + '.png', img)
