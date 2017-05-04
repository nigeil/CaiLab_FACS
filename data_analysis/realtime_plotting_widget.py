#!/bin/python
# Defines a kivy widget that includes a real-time plot of signal from all
# four color channels


import matplotlib as mpl
import pylab as plt
import numpy as np
from collections import deque
import time

class RealtimePlottingWidget():
    # Class variables

    # Class helper functions

    # given new values for all lines, redraws canvas
    def update_plot(self,dt, data_queue):
        # get the new data
        data = np.transpose(np.asarray(data_queue.get()))
        # update the y_axis and redraw
        self.ax.draw_artist(self.ax.patch)
        for i in range(0, 4):
            self.lines[i].set_ydata(data[i])
            self.ax.draw_artist(self.lines[i])
        #self.fig.canvas.draw()
        self.fig.canvas.update()
        self.fig.canvas.flush_events()

    # Class initialization
    def __init__(self):
       # initialize super class ()

       # initialize the plot
       self.fig = plt.figure(facecolor='#ffffff')
       self.ax = self.fig.add_subplot(111)
       self.ax.set_facecolor('#afafaf')
       self.lines = []
       self.colors = ["#ff0400", "#2dff38", "#0256f2", "#f2f202"]
       self.labels = ["Red", "Green", "Blue", "Yellow"]
       data = np.zeros((4,100))
       self.x_vals = (np.arange(0, len(data[0])))

       for i in range(0, len(data)):
           self.lines.append(self.ax.plot(self.x_vals, data[i], lw=1, 
                                          color=self.colors[i],
                                          label=self.labels[i], marker="")[0])
       
       self.ax.set_ylim([0,1250])
       self.ax.set_xlabel("old data <----- new data")
       self.ax.set_ylabel("Voltage (mV)")
       self.ax.set_title("4 channel real time voltages")
       #self.ax.hold()
       plt.show(block=False)
       self.fig.canvas.draw()

    # override the run method
    def run(self, data_queue):
        interval = 1./30. #shoot for 30 fps
        while True:
            self.update_plot(interval,data_queue)
            time.sleep(interval)


# testing
if __name__ == "__main__":
    def data_stream():
        return np.random.uniform(0,1200,(100,4)) 

    plot_widget = RealtimePlottingWidget(data_stream)
    plot_widget.run()

