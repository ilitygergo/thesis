from modules.functions import endpoint
from modules.functions import imreadgray
from modules.functions import flip
from modules.functions import localmaximum

picture = 'test2'

img = imreadgray('../pictures/' + picture + '.png')
img = flip(img)

print(img)
print(endpoint(img, 3, 3))
print(localmaximum(253, 34, 16, 30, 44, 51, 210, 234, 254))