#!/bin/python
# Testing how fast a python script can add data to a deque
# as a simulation of real-time data buffering from a microcontroller

import time
import numpy as np
from collections import deque

def get_data():
    return np.random.randint(0,800, size=(4))

# testing
# Result: ~ 4.7us +/- 0.01us
# On an AMD Kaveri A10-7850K @ 4.3GHz, Linux 4.9.8-zen
if __name__ == "__main__":
    n_itr = 100000
    n_tests = 10
    avg_time_per_itr = 0
    std_dev_per_itr = 0
    times = []


    for j in range(0, n_tests):
        ring_buffer = deque([], maxlen=1000)
        time0 = time.clock()
        for i in range(0, n_itr):
            ring_buffer.append(get_data())
        times.append(time.clock() - time0)
    
    avg_time_per_itr = np.mean((np.array(times) / n_itr) * 1e6)
    std_dev_per_itr = np.std((np.array(times) / n_itr) * 1e6)
    print("Average time per iteration: " + str(avg_time_per_itr) + " +/- " 
          + str(std_dev_per_itr) + " us")

