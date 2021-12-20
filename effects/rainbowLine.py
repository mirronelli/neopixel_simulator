import effects.effect as effect
from pixels import Pixels
from effects.common import color_function

class RainbowLine(effect.Effect):
    def __init__(self, pixels: Pixels, brightness) -> None:
        super().__init__(pixels)
        self.brightness =  brightness
        self.third = self.count / 3
        self.reset()

    def next_frame(self):
        super().cycle()

    def reset(self):
        # ¯\__/¯    # phase shift + 1/3
        # /¯¯\__    # no shift
        # __/¯¯\    # phase shift + 2/3
        for i in range(self.count):
            self.pixels.setPixelColorRGB(
                i, 
                color_function(i + self.third,    self.count, self.brightness),
                color_function(i,                 self.count, self.brightness),
                color_function(i + 2* self.third, self.count, self.brightness)
            )
