from gpiozero import LED
from detector import Detector
from watergun import WaterGun
from os import environ

if 'GPIO_LED' not in environ:
    print("[ERROR] You must provide GPIO_LED env variable. Pin number for LED BCM numbering")
    exit(1)

if 'GPIO_GUN' not in environ:
    print("[ERROR] You must provide GPIO_GUN env variable. Pin number for Water Gun BCM numbering")
    exit(1)

if 'PATH_TO_MODEL' not in environ:
    print("[ERROR] You must provide PATH_TO_MODEL env variable. Path to .tflite file")
    exit(1)

if 'THRESHOLD' not in environ or environ.get('THRESHOLD') == 0:
    print("[ERROR] You must provide THRESHOLD env variable. For detect object 1 threshold should be above zero, otherwise under zero")
    exit(1)


def main():
    bulb = LED(environ.get('GPIO_LED'))
    water_gun = WaterGun(environ.get('GPIO_GUN'))

    with Detector(environ.get('PATH_TO_MODEL')) as detector:
        while detector.check():
            if detector.is_detect():
                bulb.blink(.5, .3)
                water_gun.fire(1)
            else:
                bulb.off()


if __name__ == '__main__':
    main()
