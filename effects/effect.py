from pixels import Pixels

class Effect():
    def __init__(self, pixels) -> None:
        self.pixels: Pixels = pixels
        self.count = len(pixels)

    def next_frame(self):
        pass
