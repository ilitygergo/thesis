from modules.functions import endpoint
from modules.functions import imreadgray
from modules.functions import flip

picture = 'test2'

img = imreadgray('../pictures/' + picture + '.png')
img = flip(img)

print(img)
print(endpoint(img, 3, 3))