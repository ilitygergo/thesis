import time
from common import Image

startTime = time.time()

try:
    image = Image.Image('fingerprint_mini.png')
    image2 = Image.Image('fingerprint_mini.png')
    # image.save()
    if image.isEqualTo(image2):
        image = image2
except Exception as e:
    print(e)

endTime = time.time()
print(endTime - startTime)
