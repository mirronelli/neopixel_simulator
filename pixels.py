from math import pow
class Pixels:
    def __init__(self, count, gamma = 2.8) -> None:
        self.count = count
        self.data = [{'red':0, 'green':0, 'blue': 0, 'white': 0} for _ in range(self.count)]
        self.create_gamma_table(gamma)

    def show(self):
        print(self.data)

    def setPixelColorRGB(self, n, red:int, green:int, blue:int, white:int = 0):
        self.data[n]['red'] = self.gamma_table[int(red)]
        self.data[n]['green'] = self.gamma_table[int(green)]
        self.data[n]['blue'] = self.gamma_table[int(blue)]
        self.data[n]['white'] = self.gamma_table[int(white)]

    def getPixelColorRGBW(self, n):
        return self.data[n]

    def getPixels(self):
        return self.data

    def __getitem__(self, index):
        return self.data[index]

    def create_gamma_table(self, gamma):
        self.gamma_table = [round(pow(i / 255, gamma) * 255 + 0.49999) for i in range(256)]

    def numPixels(self):
        return len(self.data)