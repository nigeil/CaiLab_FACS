#!/bin/python
# Defines a widget that includes a set of plots that are updated in real-time
# and provide useful statistics/histograms of voltage values recorded from
# the microcontroller.

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import matplotlib as mpl
mpl.use('module://kivy.garden.matplotlib.backend_kivy')
import pylab as plt
import numpy as np
from collections import deque

class RealtimeStatisticsWidget(BoxLayout):
    # Class variables
    max_voltage = 3300 # mV
    bin_width = 10     # mV
    bins = np.arange(0, max_voltage, bin_width) # left side of bins
    heights = np.zeros((4,int(max_voltage/bin_width))) 
    refresh_rate = 2 # update plot every <refresh_rate> seconds
    run_state = False

    # Class helper functions

    # Given new data, update all of the histogram bar heights
    def update_histogram_heights(self,dt=0):
        # get the new data
        data = np.transpose(np.asarray(self.data_stream()))
        print(np.shape(data))
        # bins for histogram need to have last edge included
        modified_bins = self.bins
        modified_bins = np.append(modified_bins, self.max_voltage)
        for i in range(0, len(data)):
            self.heights[i] += np.histogram(data[i],modified_bins)[0]


    # given new values for all bars, redraws canvas
    def update_plot(self,dt):
        # update new histogram bar heights
        self.update_histogram_heights()
        # update the y_axis and redraw
        '''
        for i in range(0, 4):
            #self.ax[i].draw_artist(self.ax[i].patch)
            for rect, y in zip(self.bars[i], self.heights[i]):
                rect.set_height(y)
            #self.ax[i].draw_artist(self.bars[i])
        '''
        for i in range(0, 4):
            self.bars[i].set_data(self.bins, self.heights[i])
            ymin, ymax = self.ax[i].get_ylim()
            if (np.max(self.heights[i]) > ymax):
                pass
                #self.ax[i].set_ylim([0, ymax * 10])
        #self.fig.canvas.update()
        self.fig.canvas.draw()
        #self.fig.canvas.flush_events()

    # start/stop requesting data + plotting based on start/stop button state
    # True - running, False - paused
    def set_running_status(self, new_status):
        run_state = new_status
        if   (run_state == True):
            print("starting plot")
            self.clock = Clock.schedule_interval(self.update_plot, self.refresh_rate)
        elif (run_state == False):
            print("stopping plot")
            self.clock.cancel()

    # Class initialization
    def __init__(self, data_stream, **kwargs):
       # initialize super class ()
       super(RealtimeStatisticsWidget, self).__init__(**kwargs)

       # grab parameters and save to class
       self.data_stream = data_stream

       # initialize the plot
       self.fig, self.ax = plt.subplots(2,2,facecolor='#afafaf')
       self.ax = [item for sublist in self.ax for item in sublist] #flatten array
       self.colors = ["#ff0400", "#2dff38", "#0256f2", "#f2f202"]
       self.labels = ["Red", "Green", "Blue", "Yellow"]
       self.update_histogram_heights()
       self.bars = []

       for i in range(0, len(self.heights)):
           self.bars.append(self.ax[i].plot(self.bins, self.heights[i], 
                                           color=self.colors[i], 
                                           label=self.labels[i])[0])
           self.ax[i].set_yscale("log")
           self.ax[i].set_ylim([0, 1e5])
       
       self.ax[0].set_xlabel("Binned voltage (mV)")
       self.ax[0].set_ylabel("Log count")
       self.ax[0].set_title("4 channel real voltage histogram")
       plt.show(block=False)
     
     
       self.fig.canvas.draw()
       self.add_widget(self.fig.canvas)
       self.clock = Clock.schedule_interval(self.update_plot, self.refresh_rate)
       self.clock.cancel()
       #self.clock2 = Clock.schedule_interval(self.update_histogram_heights, 1/1000)

# testing
if __name__ == "__main__":
    from kivy.app import App

    def data_stream():
        return np.random.uniform(0,1200,(100,4)) 

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout()
            main_box = RealtimeStatisticsWidget(data_stream)
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
