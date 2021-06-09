from src.thinning.interface.IAlgorithm import IAlgorithm


class Couprie(IAlgorithm):
    def getName(self) -> str:
        return r"""
          _____                       _             _           _ 
         / ____|                     (_)           | |         | |
        | |     ___  _   _ _ __  _ __ _  ___    ___| |_    __ _| |
        | |    / _ \| | | | '_ \| '__| |/ _ \  / _ \ __|  / _` | |
        | |___| (_) | |_| | |_) | |  | |  __/ |  __/ |_  | (_| | |
         \_____\___/ \__,_| .__/|_|  |_|\___|  \___|\__|  \__,_|_|
                          | |
                          |_|
        """
