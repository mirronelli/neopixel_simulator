from effects import common
from rcservice import RCService

try:
    from rpi_ws281x import PixelStrip, ws
    LED_STRIP = ws.SK6812_STRIP_GRBW
    LED_COUNT = 204        # Number of LED pixels.
    LED_PIN = 12           # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10           # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0
    pixels = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    pixels.setGamma(common.create_gamma_table(2.8))
    pixels.begin()
except:
    from pixels import Pixels
    pixels = Pixels(120, 2.8)

if __name__ == "__main__":
    server = RCService(pixels, "ubi", "neo", "rpi", 120, 2)
    server.run()