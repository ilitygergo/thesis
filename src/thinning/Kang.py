from src.thinning.interface.IAlgorithm import IAlgorithm


class Kang(IAlgorithm):
    def getName(self) -> str:
        return """
         _  __                    _____       _       _  ___
        | |/ /                   / ____|     | |     | |/ (_)
        | ' / __ _ _ __   __ _  | (___  _   _| |__   | ' / _ _ __ ___
        |  < / _` | '_ \\ / _` |  \\___ \\| | | | '_ \\  |  < | | '_ ` _ \\
        | . \\ (_| | | | | (_| |  ____) | |_| | | | | | . \\| | | | | | |
        |_|\\_\\__,_|_| |_|\\__, | |_____/ \\__,_|_| |_| |_|\\_\\_|_| |_| |_|
                          __/ |
                         |___/
        """