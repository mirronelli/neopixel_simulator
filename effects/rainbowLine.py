import effects.effect as effect
from pixels import Pixels
from effects.common import color_function

class RainbowLine(effect.Effect):
    def __init__(self, pixels: Pixels, brightness) -> None:
        super().__init__(pixels)
        self.brightness =  brightness
        self.setup()

    def next_frame(self):
        last_pixel_color = self.pixels.getPixelColorRGBW(-1)
        for i in reversed(range(self.count)):
            moved_pixel = self.pixels.getPixelColorRGBW(i-1)
            self.pixels.setPixelColorRGB(i, moved_pixel['red'], moved_pixel['green'], moved_pixel['blue'], moved_pixel['white'])

        self.pixels.setPixelColorRGB(0, last_pixel_color['red'], last_pixel_color['green'], last_pixel_color['blue'], last_pixel_color['white'])

    def setup(self):
        # ¯\__/¯    # phase shift + 1/3
        # /¯¯\__    # no shift
        # __/¯¯\    # phase shift + 2/3
        third = self.count / 3
        for i in range(self.count):
            self.pixels.setPixelColorRGB(
                i, 
                color_function(i + third,    self.count, self.brightness),
                color_function(i,            self.count, self.brightness),
                color_function(i + 2* third, self.count, self.brightness)
            )