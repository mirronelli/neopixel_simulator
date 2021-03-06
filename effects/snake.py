import effects.effect as effect
from effects.common import min
from pixels import Pixels

class Snake(effect.Effect):
    def __init__(self, pixels: Pixels, snake_length, dimmed_led_count, red, green, blue, white) -> None:
        super().__init__(pixels)
        self.snake_length = snake_length
        self.dimmed_led_count = dimmed_led_count
        self.red = red
        self.green = green
        self.blue = blue
        self.white = white
        self.reset()

    def reset(self):
        super().clear()
        self.first_pixel = 0
        self.step = 1

    def next_frame(self):
        self.half_snake(self.first_pixel)

        if (self.first_pixel >= self.count - self.snake_length):
            self.step = -1

        if (self.first_pixel <= 0):
            self.step = 1

        self.first_pixel = self.first_pixel + self.step

    def half_snake(self, first_pixel):
        half_count = self.snake_length // 2
        last_pixel = self.first_pixel + self.snake_length - 1
        luminance = 0
        luminance_step = 255 // self.dimmed_led_count

        for i in range(half_count):
            luminance = min(i * luminance_step, 255)
            self.pixels.setPixelColorRGB(
                first_pixel + i, 
                int((luminance * self.red) / 255), 
                int((luminance * self.green) / 255), 
                int((luminance * self.blue) / 255), 
                int((luminance * self.white) / 255)
            )
            self.pixels.setPixelColorRGB(
                last_pixel - i, 
                int((luminance * self.red) / 255),
                int((luminance * self.green) / 255),
                int((luminance * self.blue) / 255),
                int((luminance * self.white) / 255)
            )