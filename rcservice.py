import datetime as dt
from multiprocessing.connection import Client
import time
from effects.effect import Effect
from effects.effect_factory import create_effect
import paho.mqtt.client as paho
from suntime import Sun

class RCService():
    def __init__(self, pixels, mqtt_host, mqtt_topic, mqtt_client_name, time_fast_travel_mins = 0, time_fast_travel_period = 60) -> None:
        self.pixels = pixels
        self.mqtt_host = mqtt_host
        self.mqtt_topic = mqtt_topic
        self.mqtt_client_name = mqtt_client_name

        self.current_effect:Effect = None          # the current effect
        self.frame_delay = 1
        self.led_count = 0

        self.last_time_check = 0            # track the last time sunset and sunrise have been checked
        self.current_date = dt.date.min
        self.suspended_effect:Effect = None        # remembers the effect that gets suspended on sunrise until sunset
        self.calculateSunTimes()
        self.detectTimeState()

        self.sunrise_sunset_check_period = time_fast_travel_period
        self.minutes_jump = 0
        self.minutes_jump_increment = time_fast_travel_mins

    def calculateSunTimes(self, for_day=None):
        current_time = dt.datetime.utcnow()

        latitude = 48.08825194621209
        longitude = 17.126556342940308
        sun = Sun(latitude, longitude)
        self.sunrise = sun.get_sunrise_time(for_day).replace(tzinfo=None)
        self.sunset = sun.get_sunset_time(for_day).replace(tzinfo=None)

        print(f'Current Time:\t{current_time} UTC')
        print(f'Sunrise:\t{self.sunrise} UTC')
        print(f'Sunset: \t{self.sunset} UTC')


    def detectTimeState(self):
        current_time = dt.datetime.utcnow()
        self.waiting_for = "sunrise" if current_time < self.sunrise or current_time > self.sunset else "sunset"
        print(f"Waiting for {self.waiting_for}")


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.mqtt_topic)


    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print(message)
        command, effect_definition = message.split(":", 1)
        if command == "effect":
            new_effect, self.led_count, self.frame_delay = create_effect(self.pixels, effect_definition)
            self.set_effect(new_effect)
            self.frame_delay = self.frame_delay/1000


    def clear(self):
        """Clears the leds to black."""
        for x in range(0, self.pixels.numPixels()):
            self.pixels.setPixelColorRGB(x, 0, 0, 0, 0)
        self.pixels.show()
        pass


    def suspend_or_resume_effect(self):
        """ Suspends current effect on sunrise and resumes it on sunset. """

        current_perf_time = time.perf_counter()

        # only perform the check once in a minute to avoid all the pesky math
        if current_perf_time - self.last_time_check > self.sunrise_sunset_check_period:
            self.last_time_check = current_perf_time
            current_time = dt.datetime.utcnow()
            current_time = current_time + dt.timedelta(minutes=self.minutes_jump) # speedup time for debugging

            print(f"Checking sunset and sunrise at {current_time}")
            if self.waiting_for == "sunset" and current_time.time() > self.sunset.time():
                self.waiting_for = "sunrise"
                self.calculateSunTimes((current_time + dt.timedelta(days=1)).date())

                if self.suspended_effect is not None and self.current_effect is None:
                    print("Resuming effect")
                    self.set_effect(self.suspended_effect)

            elif self.waiting_for == "sunrise" and current_time > self.sunrise:
                print("Suspending effect")
                self.waiting_for = "sunset"
                self.suspended_effect = self.current_effect
                self.current_effect = None
                self.clear()

            self.minutes_jump += self.minutes_jump_increment  # speed up time for debugging


    def set_effect(self, effect:Effect):
        self.suspended_effect = None
        self.current_effect = effect
        effect.reset()


    def startServer(self) -> Client:
        client = paho.Client(self.mqtt_client_name)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.mqtt_host, )
        return client


    def run(self):
        client = self.startServer()
        while (True):
            try:
                client.loop(0.001)
                self.suspend_or_resume_effect()

                if self.current_effect:
                    self.current_effect.next_frame()
                    self.pixels.show()

                time.sleep(self.frame_delay)
            except KeyboardInterrupt:
                break


        client.disconnect()
        self.clear()
        print("shutting down")