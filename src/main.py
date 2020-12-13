import time
from common import Image

startTime = time.time()

image = Image.Image('fingerprint_mini.png')
image.save()

endTime = time.time()
print(endTime - startTime)
