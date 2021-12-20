from pixels import Pixels

class Effect():
    def __init__(self, pixels, color_mode = 'rgb') -> None:
        self.pixels: Pixels = pixels
        self.count = pixels.numPixels()
        self.color_mode = color_mode

    def clear(self, red = 0, green = 0, blue = 0, white = 0):
        for i in range(self.count):
            self.pixels.setPixelColorRGB(i, red, green, blue, white)

    def cycle(self):
        last_pixel_color = self.pixels.getPixelColorRGBW(self.count - 1)
        for i in reversed(range(self.count -1)):
            moved_pixel = self.pixels.getPixelColorRGBW(i)
            self.pixels.setPixelColorRGB(i + 1, moved_pixel.r, moved_pixel.g, moved_pixel.b, moved_pixel.w)

        self.pixels.setPixelColorRGB(0, last_pixel_color.r, last_pixel_color.g, last_pixel_color.b, last_pixel_color.w)

    def next_frame(self):
        pass

    def reset(self):
        pass
