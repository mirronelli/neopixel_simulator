import effects.effect as effect
import pixels

class RedGreen(effect.Effect):
    def __init__(self, pixels: pixels.Pixels) -> None:
        super().__init__(pixels)
        self.reset()

    def reset(self):
        self.step = 0

    def next_frame(self):
        for i in range(self.count):
            index = (i + self.step) % self.count
            self.pixels.setPixelColorRGB(index, i/(self.count-1) * 255, 255 - i/(self.count-1)*255, 0, i*20)
        
        self.step = self.step + 1 if self.step < self.count else 0