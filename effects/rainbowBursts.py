import effects.effect as effect
from pixels import Pixels
from effects.common import color_function

class RainbowBursts(effect.Effect):
    def __init__(self, pixels: Pixels, brightness, steps) -> None:
        super().__init__(pixels)
        self.brightness =  brightness
        self.step = 0
        self.steps = steps
        self.third = 2*steps
        self.all_steps = 6*steps
        self.next_frame()

    def next_frame(self):
        red   = color_function(self.step + self.third,    self.all_steps, self.brightness)
        green = color_function(self.step,                 self.all_steps, self.brightness)
        blue  = color_function(self.step + 2* self.third, self.all_steps, self.brightness)
        for i in range(self.count):
            self.pixels.setPixelColorRGB(i, red, green, blue, 0)
        
        self.step = self.step + 1 if self.step < self.all_steps else 0