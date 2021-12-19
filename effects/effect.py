from pixels import Pixels

class Effect():
    def __init__(self, pixels) -> None:
        self.pixels: Pixels = pixels
        self.count = pixels.numPixels()

    def next_frame(self):
        pass

    def clear(self):
        for i in range(self.count):
            self.pixels.setPixelColorRGB(i, 0, 0, 0, 0)

    def reset(self):
        pass