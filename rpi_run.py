import time
from rpi_ws281x import Color, PixelStrip, ws
from effects import snake, rainbowBursts, rainbowLine, redGreen

LED_COUNT = 95         # Number of LED pixels.
LED_PIN = 12           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.SK6812_STRIP_RGBW
SLEEP = 100

pixels = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
pixels.begin()

effects = [
    rainbowLine.RainbowLine(pixels, 255),
    snake.Snake(pixels, 20, 5, 255, 0, 0, 0),
    rainbowBursts.RainbowBursts(pixels, 255, 20),
]

while True:
    for effect in effects:
        effect.reset()
        for i in range(1000):
            effect.next_frame()
            pixels.show()
            time.sleep(10)