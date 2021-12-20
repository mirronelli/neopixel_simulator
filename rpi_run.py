import time
from rpi_ws281x import PixelStrip, ws
from effects import snake, rainbowBursts, rainbowLine, redGreen, common
from effects.effect_factory import create_all_list

LED_COUNT = 95         # Number of LED pixels.
LED_PIN = 12           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.SK6812_STRIP_GRBW
SLEEP = 100

pixels = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
pixels.setGamma(common.create_gamma_table(2.2))
pixels.begin()

effects = create_all_list(pixels)

def pause(milis):
    time.sleep(milis/1000)

while True:
   for effect in reversed(effects):
       effect.reset()
       for i in range(1000):
           effect.next_frame()
           pixels.show()
           pause(10)