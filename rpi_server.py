import time
from rpi_ws281x import PixelStrip, ws
from effects import snake, rainbowBursts, rainbowLine, redGreen, common, two_color
from effects.effect_factory import create_all_list, create_effect
import paho.mqtt.client as paho

LED_COUNT = 204         # Number of LED pixels.
LED_PIN = 12           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.SK6812_STRIP_GRBW

pixels = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
pixels.setGamma(common.create_gamma_table(2.2))
pixels.begin()

pixels = None
new_effect = None
current_effect = None
frame_delay = 0
led_count = 0

def pause(milis):
    time.sleep(milis/1000)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("neo")


def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(message)
    command, effect_definition = message.split(":", 1)
    if command == "effect":
        new_effect, led_count, frame_delay = create_effect(pixels, effect_definition)


client = paho.Client("rpi")
client.on_connect = on_connect
client.on_message = on_message
client.connect("ubi", )

client.loop_start()
while (True):
    if new_effect:
        current_effect = new_effect
        new_effect = None

    if current_effect:
        current_effect.next_frame()
        pixels.show()
    time.sleep(frame_delay)

client.loop_stop()





# effects = create_all_list(pixels)
# while True:
#    for effect in reversed(effects):
#        effect.reset()
#        for i in range(1000):
#            effect.next_frame()
#            pixels.show()
#            pause(SLEEP)

# effect = two_color.TwoColor(pixels, 255, 255, 0, 0, 0, 255)
# #effect = snake.Snake(pixels, 10, 10, 255, 255, 0, 0)
# effect.reset()
# while True:
#     effect.next_frame()
#     pixels.show()

