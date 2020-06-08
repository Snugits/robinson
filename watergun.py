import time

from gpiozero import OutputDevice

class WaterGun(object):
    def __init__(self, gpio_num):
        self.gun = OutputDevice(gpio_num, active_high=False)

    def fire(self, shots_num):
        self.gun.on()
        time.sleep(shots_num)
        self.gun.off()