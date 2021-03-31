'''
Has to implement:
    from common.functions import rvalue
    from common.functions import minimize
    from common.functions import notendpoint
    from common.functions import connected
    findBorderPoints
'''

from thinning.interface.IAlgorithm import IAlgorithm
from thinning.Image import Image

class DyerRosenfeld(IAlgorithm):
    def getName(self) -> str:
        return """
         _____                    _____                       __     _     _
        |  __ \\                  |  __ \\                     / _|   | |   | |
        | |  | |_   _  ___ _ __  | |__) |___  ___  ___ _ __ | |_ ___| | __| |
        | |  | | | | |/ _ \\ '__| |  _  // _ \\/ __|/ _ \\ '_ \\|  _/ _ \\ |/ _` |
        | |__| | |_| |  __/ |    | | \\ \\ (_) \\__ \\  __/ | | | ||  __/ | (_| |
        |_____/ \\__, |\\___|_|    |_|  \\_\\___/|___/\\___|_| |_|_| \\___|_|\\__,_|
                 __/ |
                |___/
        """

    def processStepOnImage(self, img):
        self.previousStep = Image(img.path)



        return img

    def findBorderPoints(self):
        pass
