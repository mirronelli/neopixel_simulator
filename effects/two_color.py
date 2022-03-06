import effects.effect as effect
from pixels import Pixels

class TwoColor(effect.Effect):
    def __init__(self, pixels: Pixels, r1, g1, b1, r2, g2, b2) -> None:
        super().__init__(pixels)
        self.r1 = r1
        self.g1 = g1
        self.b1 = b1
        self.r2 = r2
        self.g2 = g2
        self.b2 = b2

    def next_frame(self):
        super().cycle()

    def reset(self):
        first_half = self.count // 2
        for i in range(first_half):
            self.pixels.setPixelColorRGB(i, self.r1, self.g1, self.b1)
        for i in range(first_half, self.count):
            self.pixels.setPixelColorRGB(i, self.r2, self.g2, self.b2)