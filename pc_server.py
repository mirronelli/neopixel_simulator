from effects import common
from rcservice import RCService
from pixels import Pixels
pixels = Pixels(120, 2.8)

if __name__ == "__main__":
    server = RCService(pixels, "ubi", "neo", "pc", 120, 2)
    server.run()