# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-000008b7592f/w1_slave'

def temp_raw():

    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():

    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()

    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def toFloat(val):
    try:
        return float(val)
    except:
        print('received no float value')

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

redRGBValue = GPIO.PWM(24, 100)
blueRGBValue = GPIO.PWM(20, 100)
greenRGBValue = GPIO.PWM(21, 100)

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPayloadSize(32)
radio.setChannel(0x70)


radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.printDetails()

radio.startListening()

while True:
    ackPL = [1]
    while not radio.available(0):
        time.sleep(1/2)

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())

    string = ""
    for n in receivedMessage:
        # Decode into standard unicode set
        if (n >= 32 and n <= 126):
            string += chr(n)
    print('received RGB setup:' + string)
    colors = string.split(':')
    print(colors)
    redRGBColor = toFloat(colors[1])
    greenRGBColor = toFloat(colors[3])
    blueRGBColor = toFloat(colors[5])
#    print(redRGBColor)
#    print(greenRGBColor)
#    print(blueRGBColor)
    
    redRGBValue.start(redRGBColor)
    blueRGBValue.start(blueRGBColor)
    greenRGBValue.start(greenRGBColor)

    temperature = list(str(read_temp()))
    temperature = [ord(elem) for elem in temperature]
    print(temperature)
    radio.writeAckPayload(1, temperature, len(temperature))
#    print("Loaded payload reply of {}".format(ackPL))
    









        
