from abc import ABC


class Platform(ABC):
    def __inif__(self, x, y):
        pass

    def stop_player_fall(self):
        pass

    def float(self):
        pass