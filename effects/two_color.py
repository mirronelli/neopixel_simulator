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
        # super().cycle()
        self.switch_forward +=1
        if (self.switch_forward >= self.count):
            self.switch_forward = 0
        
        self.switch_back +=1
        if (self.switch_back >= self.count):
            self.switch_back = 0
        
        self.pixels.setPixelColorRGB(self.switch_forward, self.r1, self.g1, self.b1)
        self.pixels.setPixelColorRGB(self.switch_back, self.r2, self.g2, self.b2)

    def reset(self):
        self.switch_forward = self.count // 2 - 1
        self.switch_back = self.count
        for i in range(self.count // 2):
            self.pixels.setPixelColorRGB(i, self.r1, self.g1, self.b1)
        for i in range(self.count // 2, self.count):
            self.pixels.setPixelColorRGB(i, self.r2, self.g2, self.b2)