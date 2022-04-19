from math import pow
from effects.common import create_gamma_table

class Pixels:
    def __init__(self, count, gamma = 2.8) -> None:
        self.count = count
        self.data = [{'red':0, 'green':0, 'blue': 0, 'white': 0} for _ in range(self.count)]
        self.gamma_table = create_gamma_table(gamma)

    def show(self):
        print("".join(
            [ str( 
                round(
                    10*
                    (i["red"] + i["green"] + i["blue"] + i["white"])/4
                    /255)
                )
                for i in self.data
            ]
        ))

    def setPixelColorRGB(self, n, red:int, green:int, blue:int, white:int = 0):
        if n < 0:
            raise NameError("Cannot use negative indexes, the C style array in rpi_ws281x does not support it and writes bogus data.")

        if n >= self.count:
            raise NameError("Index out of bounds.")

        self.data[n]['red'] = int(red)
        self.data[n]['green'] = int(green)
        self.data[n]['blue'] = int(blue)
        self.data[n]['white'] = int(white)

    # this is how the ws strip returns the pixel
    def getPixelColorRGBW(self, n):
        if n < 0:
            raise NameError("Cannot use negative indexes, the C style array in rpi_ws281x does not support it and returns bogus data.")

        if n >= self.count:
            raise NameError("Index out of bounds.")
            
        c = lambda: None
        setattr(c, 'w', self.data[n]['white'])
        setattr(c, 'r', self.data[n]['red'])
        setattr(c, 'g', self.data[n]['green'])
        setattr(c, 'b', self.data[n]['blue'])
        return c

    def getPixels(self):
        return self.data

    def __getitem__(self, index):
        return self.data[index]

    def numPixels(self):
        return len(self.data)