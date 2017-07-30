import matplotlib.pyplot as plt
import socket,sys

from kivy.graphics import *
#from kivy.core.window import Window
import numpy as np
import threading
import pickle
from kivy.clock import Clock

import bluetooth
from nxt.bluesock import BlueSock
import nxt.bluesock as bb
import nxt.motor as m
import bluetooth
import nxt.brick
import nxt.locator
import threading
import time
import testt

BRICK_ID = '00:16:53:13:C6:DE' # read from TextInput
#print(BRICK_ID)
#sock=BlueSock(BRICK_ID)
#brick = sock.connect()

def FPS():
    count=0
    start=time.time()
    while True:
        time.sleep(0.005)
        count+=1
        if count==100:
            print('FPS: '+str(count/(time.time()-start)))
            start=time.time()
            count=0

#threading.Thread(target=FPS).start()


def get_distance():
    One = nxt.sensor.Touch(brick, nxt.PORT_4)
    while True:
        if One.is_pressed() == True:
            print(One.is_pressed())

#time.sleep(5)
#get_distance()


list_of_devices = {}
names_of_devices = []
x = bluetooth.discover_devices()
for i in x:
    i_name = bluetooth.lookup_name(i)

    list_of_devices[str(i_name)] = i
    names_of_devices.append(i_name)
print(list_of_devices)
discover_constant = False

### List of devices
DEVICES = list_of_devices
print(DEVICES)