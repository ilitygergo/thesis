from classes.Algorithm import Algorithm
from core.Image import Image

class DyerRosenfeld(Algorithm):
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

    def step(self, img):
        print(img)
        img2 = Image(img.path)
        print(img2)
        return None
