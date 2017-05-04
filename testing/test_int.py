#!/bin/python
# Tests byte-by-byte integer communication with microcontroller

import serial
from struct import *
from array import *
from time import sleep

def int_to_bytes(the_int):
    return pack("<I", the_int)
    
def bytes_to_int(the_bytes):
    return unpack(">I", the_bytes)[0]

mc = serial.Serial("/dev/ttyACM0", timeout=0)
true_value = 12345678 
true_float = 3.574
print(int_to_bytes(true_value))
for i in range(0, 10):
    sleep(1)

    mc.write(int_to_bytes(true_value))
    mc.write(int_to_bytes(int(true_float * 1000)))
    
    if (i == 0 or i == 1):
        continue

    returned_bytes = mc.read(4)
    print(returned_bytes)
    print(bytes_to_int(returned_bytes))

    response = mc.readline()
    print(response)
    response = mc.readline()
    print(response)

