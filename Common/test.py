from Common.functions import imreadgray
from Common.functions import flip

picture = 'sima'
img = imreadgray('../Common/' + picture + '.png')
flip(img)

size = img.shape
hist = [0] * 256
maximum = 0

for row in range(size[0]):
    for col in range(size[1]):
        hist[int(img[row][col])] += 1

for max in range(256):
    if maximum < hist[max]:
        maximum = hist[max]

print(hist)
print(maximum)
