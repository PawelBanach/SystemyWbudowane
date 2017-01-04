# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)


r = GPIO.PWM(24, 100)
b = GPIO.PWM(20, 100)
g = GPIO.PWM(21, 100)
r.start(100)
b.start(10)
g.start(10)
input('Press return to stop:')
p.stop()
GPIO.cleanup()
