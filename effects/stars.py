#int probability, int fadeSpeed, uint8_t red, uint8_t green, uint8_t blue, uint8_t white


import effects.effect as effect
from pixels import Pixels
from random import randint
from common import max

class Stars(effect.Effect):
    def __init__(self, pixels: Pixels, red, green, blue, white, probability = 99500, fade_steps = 20) -> None:
        self.fading_step_red = red // fade_steps
        self.fading_step_green = green // fade_steps
        self.fading_step_blue = blue // fade_steps
        self.fading_step_white = white // fade_steps
        
        self.max_red = red
        self.max_green = green
        self.max_blue = blue
        self.max_white = white

        self.probability = probability
    
    def reset(self):
        self.clear()

    def next_frame(self):
        for i in range(self.count):
            if randint % 100000 > self.probability:
                self.pixels.setPixelColorRGB(
                    self.max_red,
                    self.max_green,
                    self.max_blue,
                    self.max_white
                )
            else:
                pixel = self.pixels.getPixelColorRGBW(i)
                self.pixels.setPixelColorRGB(
                    max(0, self.pixels.r - self.fading_step_red),
                    max(0, self.pixels.b - self.fading_step_blue),
                    max(0, self.pixels.w - self.fading_step_white),
                    max(0, self.pixels.g - self.fading_step_green)
                )