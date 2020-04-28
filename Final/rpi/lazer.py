#!/usr/bin/env python

# Control Lasermodule from Raspberry Pi
# https://raspberrytips.nl/laser-module-aansturen-via-gpio/

import RPi.GPIO as GPIO
import time

LaserGPIO = 17 # --> PIN11/GPIO17

def start():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LaserGPIO, GPIO.OUT)
    GPIO.output(LaserGPIO, GPIO.HIGH)

def fire():
    print('Laser=on')
    #GPIO.setmode(GPIO.BCM)
    GPIO.setup(LaserGPIO, GPIO.OUT)
    GPIO.output(LaserGPIO, GPIO.HIGH) # led on
    time.sleep(1.0)
    pass
          
def cease_fire():
    print('Laser=off')
    GPIO.setup(LaserGPIO, GPIO.OUT)
    GPIO.output(LaserGPIO, GPIO.LOW) # led off
    time.sleep(1.0)

def destroy():
    GPIO.output(LaserGPIO, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        start()
        time.sleep(2.0)
        cease_fire()

    except KeyboardInterrupt:
        destroy()
