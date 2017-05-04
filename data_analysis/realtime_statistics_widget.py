#!/bin/python
# Defines a widget that includes a set of plots that are updated in real-time
# and provide useful statistics/histograms of voltage values recorded from
# the microcontroller.


import matplotlib as mpl
import pylab as plt
import numpy as np
from collections import deque

class RealtimeStatisticsWidget():
    # Class variables
    max_voltage = 1200 # mV
    bin_width = 10     # mV
    bins = np.arange(0, max_voltage, bin_width) # left side of bins
    heights = [[],[],[],[]]

    # Class helper functions

    # Given new data, update all of the histogram bar heights
    def update_histogram_heights(self):
        # get the new data
        data = np.transpose(np.asarray(self.data_stream()))
        # bins for histogram need to have last edge included
        modified_bins = self.bins
        modified_bins = np.append(modified_bins, self.max_voltage)
        for i in range(0, len(data)):
            self.heights[i] = np.histogram(data[i],modified_bins)[0]


    # given new values for all bars, redraws canvas
    def update_plot(self,dt):
        # update new histogram bar heights
        self.update_histogram_heights()
        # update the y_axis and redraw
        #self.ax.draw_artist(self.ax.patch)
        for i in range(0, 4):
            for rect, y in zip(self.bars[i], self.heights[i]):
                rect.set_height(y)
            #self.ax.draw_artist(self.bars[i])
        self.fig.canvas.draw()
        #self.fig.canvas.update()
        #self.fig.canvas.flush_events()

    # Class initialization
    def __init__(self, data_stream):
       # initialize super class ()

       # grab parameters and save to class
       self.data_stream = data_stream

       # initialize the plot
       self.fig = plt.figure(facecolor='#ffffff')
       self.ax = self.fig.add_subplot(111)
       self.ax.set_facecolor('#afafaf')
       self.bars = []
       self.colors = ["#ff0400", "#2dff38", "#0256f2", "#f2f202"]
       self.labels = ["Red", "Green", "Blue", "Yellow"]
       self.update_histogram_heights()

       for i in range(0, len(self.heights)):
           self.bars.append(self.ax.bar(self.bins, self.heights[i],
                                          color=self.colors[i],
                                          label=self.labels[i]))
       
       self.ax.set_yscale("log")
       self.ax.set_xlabel("Binned voltage (mV)")
       self.ax.set_ylabel("Log count")
       self.ax.set_title("4 channel real voltage histogram")
       plt.show(block=False)
       self.fig.canvas.draw()

# testing
if __name__ == "__main__":
    def data_stream():
        return np.random.uniform(0,1200,(100,4)) 

    plot_widget = RealtimeStatisticsWidget(data_stream)
    i = 0
    while True:
        if (i % 10 == 0):
            plot_widget.update_plot(1/25)
        i = i + 1

