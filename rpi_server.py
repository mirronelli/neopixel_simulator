from datetime import date, datetime, timedelta
import time
from rpi_ws281x import PixelStrip, ws
from effects import snake, rainbowBursts, rainbowLine, redGreen, common, two_color
from effects.effect import Effect
from effects.effect_factory import create_all_list, create_effect
import paho.mqtt.client as paho
from suntime import Sun

class NeoPixelServer():
    def __init__(self) -> None:
        self.LED_COUNT = 204        # Number of LED pixels.
        self.LED_PIN = 12           # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA = 10           # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL = 0
        self.LED_STRIP = ws.SK6812_STRIP_GRBW

        self.pixels = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL, self.LED_STRIP)
        self.pixels.setGamma(common.create_gamma_table(2.8))
        self.pixels.begin()

        self.current_effect:Effect = None          # the current effect
        self.frame_delay = 1
        self.led_count = 0

        self.last_time_check = 0            # track the last time sunset and sunrise have been checked
        self.current_date = date.min
        self.suspended_effect:Effect = None        # remembers the effect that gets suspended on sunrise until sunset
        self.calculateSunTimes()
        self.detectTimeState()

        self.minutes_jump = 0
        self.minutes_jump_increment = 0

    def calculateSunTimes(self, for_day=None):
        current_time = datetime.utcnow()

        latitude = 48.08825194621209
        longitude = 17.126556342940308
        sun = Sun(latitude, longitude)
        self.sunrise = sun.get_sunrise_time(for_day).replace(tzinfo=None)
        self.sunset = sun.get_sunset_time(for_day).replace(tzinfo=None)

        print(f'Current Time:\t{current_time} UTC')
        print(f'Sunrise:\t{self.sunrise} UTC')
        print(f'Sunset: \t{self.sunset} UTC')


    def detectTimeState(self):
        current_time = datetime.utcnow()
        self.waiting_for = "sunrise" if current_time < self.sunrise or current_time > self.sunset else "sunset"
        print(f"Waiting for {self.waiting_for}")


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("neo")


    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print(message)
        command, effect_definition = message.split(":", 1)
        if command == "effect":
            self.current_effect, self.led_count, self.frame_delay = create_effect(self.pixels, effect_definition)
            self.current_effect.reset()
            self.frame_delay = self.frame_delay/1000


    def clear(self):
        """Clears the leds to black."""
        for x in range(0, self.pixels.numPixels()):
            self.pixels.setPixelColorRGB(x, 0, 0, 0, 0)
        self.pixels.show()
        pass


    def suspendOrResume(self):
        """ Suspends current effect on sunrise and resumes it on sunset. """

        current_perf_time = time.perf_counter()

        # only perform the check once in a minute to avoid all the pesky math
        if current_perf_time - self.last_time_check > 60:
            self.last_time_check = current_perf_time
            current_time = datetime.utcnow()
            current_time = current_time + timedelta(minutes=self.minutes_jump) # speedup time for debugging

            print(f"Checking sunset and sunrise at {current_time}")
            if self.waiting_for == "sunset" and current_time.time() > self.sunset.time():
                self.waiting_for = "sunrise"
                self.calculateSunTimes((current_time + timedelta(days=1)).date())

                if self.suspended_effect is not None:
                    print("Resuming effect")
                    self.current_effect = self.suspended_effect
                    self.current_effect.reset()
                    self.suspended_effect = None

            elif self.waiting_for == "sunrise" and current_time > self.sunrise:
                print("Suspending effect")
                self.waiting_for = "sunset"
                self.suspended_effect = self.current_effect
                self.current_effect = None
                self.clear()

            self.minutes_jump += self.minutes_jump_increment  # speed up time for debugging


    def run(self):
        client = paho.Client("rpi")
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect("ubi", )

        while (True):
            try:
                client.loop(0.001)
                self.suspendOrResume()

                if self.current_effect:
                    self.current_effect.next_frame()
                    self.pixels.show()

                time.sleep(self.frame_delay)
            except KeyboardInterrupt:
                break


        client.disconnect()
        self.clear()
        print("shutting down")

if __name__ == "__main__":
    server = NeoPixelServer()
    server.run()
