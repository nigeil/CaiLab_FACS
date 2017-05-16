#!/bin/python
# defines the class that handles microcontroller communications, with relevent
# setter/getter functions. Also handles data buffering and storage.

import serial
from collections import deque
from struct import *

class Microcontroller():
    # Class variables
    ## most recent values
    current_voltages = [0, 0, 0, 0]
    current_cell_counts = [0, 0, 0, 0] 
    current_loop_time = 0
    threshold_voltages = [0, 0, 0, 0]    
    max_cell_counts = [0, 0, 0, 0] 
    ## buffered values
    voltage_buffer = deque([], maxlen=20000)
    cell_count_buffer = deque([], maxlen=20000)
    loop_time_buffer = deque([], maxlen=20000)
    ## all values recieved
    voltage_storage = []
    cell_count_storage = []
    loop_time_storage = []
    ## other data
    debug_data = ""
    ## conversion factor for voltages (everything should be expressed in mV)
    voltage_div_factor = 1000.0

    # Class helper functions
    def bytes_to_int(self, the_bytes):
        return unpack(">I", the_bytes)[0]

    def int_to_bytes(self, the_int):
        return pack(">I", the_int)

    def many_bytes_to_ints(self, the_bytes):
        return unpack(">IIII", the_bytes)

    def get_current_voltages(self):
        return self.current_voltages

    def get_voltage_buffer(self):
        return self.voltage_buffer

    def get_voltage_storage(self):
        return self.voltage_storage

    def get_current_cell_counts(self):
        return self.current_cell_counts

    def get_cell_count_buffer(self):
        return self.cell_count_buffer
    
    def get_cell_count_storage(self):
        return self.cell_count_storage

    def get_current_loop_time(self):
        return self.current_loop_time

    def get_loop_time_buffer(self):
        return self.loop_time_buffer

    def get_loop_time_storage(self):
        return self.loop_time_storage

    def get_threshold_voltages(self):
        return self.threshold_voltages

    def get_max_cell_counts(self):
        return self.max_cell_counts

    def get_debug_data(self):
        return self.debug_data

    def parse_data(self, id_requested):
        # send request for specific piece of data
        self.microcontroller.write(self.int_to_bytes(id_requested))
        
        # parse the response (data)
        data_buf = self.microcontroller.read(size=1)
        if data_buf is b'':
            return

        data_id = unpack("<B", data_buf)[0]
        # recieved current voltages
        if (data_id == 1):
            in_bytes = self.microcontroller.read(size=4*4)
            self.current_voltages = self.many_bytes_to_ints(in_bytes) 
            self.voltage_buffer.append(self.current_voltages)
            self.voltage_storage.append(self.current_voltages)
            #print("[DEBUG] parsed voltages; size of buffer = " + str(len(self.voltage_buffer)))
        # recieved current cell counts
        elif (data_id == 2):
            in_bytes = self.microcontroller.read(size=4*4)
            self.current_cell_counts = self.many_bytes_to_ints(in_bytes) 
            self.cell_count_buffer.append(self.current_cell_counts)
            self.cell_count_storage.append(self.current_cell_counts)
        # recieved loop time
        elif (data_id == 3):
            in_bytes = self.microcontroller.read(size=4)
            self.current_loop_time = self.bytes_to_int(in_bytes)
            self.loop_time_buffer.append(self.current_loop_time)
            self.loop_time_storage.append(self.current_loop_time)
        # recieved threshold voltages 
        elif (data_id == 4):
            in_bytes = self.microcontroller.read(size=4*4)
            self.threshold_voltages = self.many_bytes_to_ints(in_bytes)
        # recieved max cell counts 
        elif (data_id == 5):
            in_bytes = self.microcontroller.read(size=4*4)
            self.max_cell_counts = self.many_bytes_to_ints(in_bytes)
        # recieved debug data
        elif (data_id == 255):
            self.debug_data = self.microcontroller.readline()
    
    def parse_all_data(self, dt=0):
        for i in [10,20,30,40,50]: # request data codes
            self.parse_data(i)

    def parse_voltages(self, dt=0):
        self.parse_data(10)
    
    def parse_cell_counts(self, dt=0):
        self.parse_data(20)
    
    def parse_threshold_voltages(self, dt=0):
        self.parse_data(40)

    def send_run_state(self, state):
        if   (state == True):
            self.microcontroller.write(self.int_to_bytes(0))
            self.microcontroller.write(self.int_to_bytes(1)) # on
            self.microcontroller.flush()
        elif (state == False):
            self.microcontroller.write(self.int_to_bytes(0))
            self.microcontroller.write(self.int_to_bytes(0)) # off
            self.microcontroller.flush()
        else:
            return -1

    def send_threshold_voltages(self, threshold_voltages):
        # send data_id to microcontroller
        self.microcontroller.write(self.int_to_bytes(1))
        
        # convert floats to ints and send
        for i in range(0, 4):    
            send_me = self.int_to_bytes(int(threshold_voltages[i]))
            self.microcontroller.write(send_me)
        self.microcontroller.flush()
        return
    
    def send_max_cell_counts(self, cell_counts):
        # send data_id to microcontroller
        self.microcontroller.write(self.int_to_bytes(2))
        
        # convert floats to ints and send
        for i in range(0, 4):    
            send_me = self.int_to_bytes(int(cell_counts[i]))
            self.microcontroller.write(send_me)
        self.microcontroller.flush()
        return

    # Class initialization
    def __init__(self):
        self.microcontroller = serial.Serial('/dev/ttyACM0', timeout=0.001, rtscts=True)
        self.microcontroller.reset_input_buffer()
        self.microcontroller.reset_output_buffer()


# testing
if __name__ == "__main__":
    import numpy as np
    import time

    mc = Microcontroller()
    new_voltages = [200,400,300,450] 
    new_cell_counts = [500,200,300,400]
    print(new_voltages, new_cell_counts)
    mc.send_run_state(True)
    for i in range(0, 400):
        if i==10:
            mc.send_threshold_voltages(new_voltages)
        if i==30:
            mc.send_max_cell_counts(new_cell_counts)
        mc.parse_data(10)
        mc.parse_data(20)
        mc.parse_data(30)
        mc.parse_data(40)
        mc.parse_data(50)
        
        print("Voltages           (mV): " + str(mc.get_current_voltages()))
        print("Threshold voltages (mV): " + str(mc.get_threshold_voltages()))
        print("Cell counts        (#) : " + str(mc.get_current_cell_counts()))
        print("Max cell counts    (#) : " + str(mc.get_max_cell_counts()))
        print("Loop time          (us): " + str(mc.get_current_loop_time()))
        print("Voltage buffer: " + str(mc.get_voltage_buffer()))
       
        debug = str(mc.get_debug_data())
            #if('ID0' not in debug.split(" ")):
        print(debug)
    mc.send_run_state(False)
