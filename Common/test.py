from Common.functions import imreadgray
from Common.functions import flip

picture = 'fingerprintmini'
img = imreadgray('../Common/' + picture + '.png')
flip(img)

size = img.shape
hist = [0] * 256
maxima = 0
maximum = 0

for row in range(size[0]):
    for col in range(size[1]):
        hist[int(img[row][col])] += 1

for max in range(256):
    if max == 0:
        continue
    if maxima < hist[max]:
        maxima = hist[max]
        maximum = max

print(hist)
print(maximum)
