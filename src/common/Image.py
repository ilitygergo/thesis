class Image:
    import cv2
    import numpy
    lookUpTable = []

    def __init__(self, file_name):
        self.name = file_name
        self.path = 'common/files/input/' + file_name
        self.extension = self.path.split('.')[1]
        self.pixels = self.readGrayImage()
        self.rowSize, self.colSize = self.pixels.shape
        self.convertPixelValuesToOpposite()

    def readGrayImage(self):
        image = self.cv2.imread(self.path)
        return self.cv2.cvtColor(image, self.cv2.COLOR_BGR2GRAY)

    def convertPixelValuesToOpposite(self):
        for i in range(256):
            self.lookUpTable.append(255 - i)

        self.setPixelValuesByLookUpTable()

    def setPixelValuesByLookUpTable(self):
        lookUpTable = self.numpy.array(self.lookUpTable, dtype=self.numpy.uint8)
        self.pixels = lookUpTable[self.pixels]
        self.lookUpTable = []

    def save(self):
        self.convertPixelValuesToOpposite()
        self.cv2.imwrite('common/files/output/' + self.name, self.pixels)
