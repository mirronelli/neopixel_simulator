from pixels import Pixels

class Effect():
    def __init__(self, pixels, color_mode = 'rgb') -> None:
        self.pixels: Pixels = pixels
        self.count = pixels.numPixels()
        self.color_mode = color_mode

    def next_frame(self):
        pass

    def clear(self):
        for i in range(self.count):
            self.pixels.setPixelColorRGB(i, 0, 0, 0, 0)

    def reset(self):
        pass
