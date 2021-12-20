import effects.effect as effect
from pixels import Pixels

class Solid(effect.Effect):
    def __init__(self, pixels: Pixels, red, green, blue, white) -> None:
        super().__init__(pixels)
        self.red = red
        self.green = green
        self.blue = blue
        self.white = white

    def reset(self):
        self.clear(self.red, self.green, self.blue, self.white)