#!/bin/python
# Tests how fast the microcontroller can read all channels and return
# to the top of the loop.

import serial
import time
import re
import numpy as np
import io

t_list = []
voltages_list = []
i = 0
n_itr = 10000

mc = serial.Serial('/dev/ttyACM0', timeout=1.0, rtscts=True)
#mc = serial.Serial('/dev/ttyACM0', 250000, timeout=10.0, rtscts=True)
print("[STATUS] teensy found")
sio = io.TextIOWrapper(io.BufferedRWPair(mc, mc))

while (i < n_itr):
    dat = sio.readline()
    print("[DEBUG] dat = " + str(dat))
    if dat is not '':
        t = re.findall(r'TIME: (.*?) RUNSTATE:',dat)
        if (t not in[[], None]):
            t = int(t[0])
            t_list.append(t)
            print(t)
            i += 1
        voltages = re.findall(r'CURR_VOLTAGES: (.*?) THRESH_VOLTAGES:', dat)
        if (voltages not in [[], None]):
            voltages = np.fromstring(voltages[0], sep=' ')
            voltages_list.append(voltages)
            i += 1

t_list = np.array(t_list)
t_mean = np.mean(t_list)
t_stddev = np.std(t_list)

voltages_list = np.array(voltages_list)
voltages_mean = np.mean(voltages_list, axis=0)
voltages_stddev = np.std(voltages_list, axis=0)

print("avg. time +/- stddev: " + str(t_mean) + " +/- " + str(t_stddev) + "us")
print("avg .voltages +/- stddev: " + str(voltages_mean) + " +/- " + str(voltages_stddev) + " mV")

