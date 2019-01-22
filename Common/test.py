import cv2
from Common.functions import imreadgray
from Common.functions import flip
from Common.functions import countf

img = imreadgray('../Common/fasz2.png')
flip(img)

X = [1, 0, -1, 0, 1, 0, -1, 0, 1, -1]
# print(X)

last_sign = 0
sign_changes = 0

for x in X:
    if x == 0:
        continue
    elif x == 1:
        if last_sign == -1:
            sign_changes += 1
    last_sign = x

# print(sign_changes)

print(img)
print(countf(img, 2, 2))