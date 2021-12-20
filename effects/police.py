import effects.effect as effect
from pixels import Pixels

class Police(effect.Effect):
    def __init__(self, pixels: Pixels, brightness = 255) -> None:
        super().__init__(pixels)
        self.brightness = brightness

    def next_frame(self):
        super().cycle()

    def reset(self):
        first_half = self.count // 2
        for i in range(first_half):
            self.pixels.setPixelColorRGB(i, self.brightness, 0, 0)
        for i in range(first_half, self.count):
            self.pixels.setPixelColorRGB(i, 0, 0, self.brightness)