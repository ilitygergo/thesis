from src.thinning.interface.IAlgorithm import IAlgorithm


class Kim(IAlgorithm):
    def getName(self) -> str:
        return r"""
         _  ___             _                  _____ _           _ 
        | |/ (_)           | |                / ____| |         (_)
        | ' / _ _ __ ___   | |     ___  ___  | |    | |__   ___  _ 
        |  < | | '_ ` _ \  | |    / _ \/ _ \ | |    | '_ \ / _ \| |
        | . \| | | | | | | | |___|  __/  __/ | |____| | | | (_) | |
        |_|\_\_|_| |_| |_| |______\___|\___|  \_____|_| |_|\___/|_|
        """
