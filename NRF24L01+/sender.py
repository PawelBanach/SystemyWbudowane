# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import paho.mqtt.client as mqtt


client = mqtt.Client("python_sub") # if it does not work, change it to parameterless constructor ...

client.connect('localhost', 1883)

publisher = mqtt.Client("python_pub")
#publisher.connect('localhost', 1883)

def toFloat(val):
    try:
        return float(val)
    except:
        print('received no float value')

def on_connect(client, userdata, rc):
    print('Connected with result code ' + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('home/rgbled')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print 'Received message from mqtt server: Topic: ,' + msg.topic + 'Message: ' + str(msg.payload)
    radio.write(msg.payload)
    print("We sent the message of {}".format(msg.payload))
    if radio.isAckPayloadAvailable():
        returnedPL = []
        radio.read(returnedPL, radio.getDynamicPayloadSize())

        temperature = ""
        for n in returnedPL:
            if (n >= 32 and n <= 126):
                temperature += chr(n)
        
        publisher.connect('localhost', 1883)
        publisher.publish('home/temperature', toFloat(temperature))
        publisher.disconnect()
        print(toFloat(temperature))
    else:
        #print("No payload received")
        time.sleep(1)
    
client.on_connect = on_connect
client.on_message = on_message


pipes = [ [0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2] ]

GPIO.setmode(GPIO.BCM)
    
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPayloadSize(32)
radio.setChannel(0x70)

radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[1])
radio.printDetails()


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.


client.loop_forever()
