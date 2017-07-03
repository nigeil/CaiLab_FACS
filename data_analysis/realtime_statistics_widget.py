#!/bin/python
# Defines a widget that includes a set of plots that are updated in real-time
# and provide useful statistics/histograms of voltage values recorded from
# the microcontroller.


#import matplotlib as mpl
#import pylab as plt
from PyQt5 import QtGui, QtCore
import sys
import pyqtgraph as pg
import numpy as np
from collections import deque

class RealtimeStatisticsWidget(QtGui.QWidget):
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
    def update_plot(self):
        # update new histogram bar heights
        self.update_histogram_heights()
        # update the y_axis and redraw
        for i in range(0, 4):
            self.plots[i].setData(self.bins, self.heights[i], color=self.colors[i])

    # Class initialization
    def __init__(self, data_stream):
       # initialize super class ()
       super(RealtimeStatisticsWidget, self).__init__()

       # grab parameters and save to class
       self.data_stream = data_stream

       # initialize the widget
       self.colors = ["#ff0400", "#2dff38", "#0256f2", "#f2f202"]
       self.labels = ["Red", "Green", "Blue", "Yellow"]

       self.timer = pg.QtCore.QTimer()
       self.timer.timeout.connect(self.update_plot)
       self.timer.start(10)

       self.setWindowTitle("Real time histogram")
       self.layout = QtGui.QGridLayout()
       self.setLayout(self.layout)

       self.plotwidgets = [pg.PlotWidget(title=self.labels[i]) for i in range(0, 4)]
       grid_rows = [0,0,1,1]
       grid_cols = [0,1,0,1]
       for i in range(0, 4):
           self.layout.addWidget(self.plotwidgets[i], grid_rows[i], grid_cols[i])

       self.show()



       self.plots = [pg.PlotCurveItem(color=self.colors[i]) for i in range(0, 4)]
       self.axes = [self.plotwidgets[i].addItem(self.plots[i]) for i in range(0, 4)]
       self.update_plot()
       
       for p in self.plotwidgets:
            p.setLogMode(x=None, y=None)
            p.setLabel(axis="bottom", text="Binned voltage (mV)")
            p.setLabel(axis="left", text="Log count")

# testing
if __name__ == "__main__":
    def data_stream():
        return np.random.uniform(0,1200,(100,4)) 

    app = QtGui.QApplication(sys.argv)
    plot_widget = RealtimeStatisticsWidget(data_stream)
    sys.exit(app.exec_())

