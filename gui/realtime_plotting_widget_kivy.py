#!/bin/python
# Defines a kivy widget that includes a real-time plot of signal from all
# four color channels
# REQ: matplotlib kivy plugin (garden install matplotlib)

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import matplotlib as mpl
mpl.use('module://kivy.garden.matplotlib.backend_kivy')
import pylab as plt
import numpy as np


class RealtimePlottingWidget(BoxLayout):
    # Class variables

    # Class helper functions

    # given new values for all lines, redraws canvas
    def update_plot(self,dt):
        # get the new data
        data = self.data_stream()
        # update the y_axis and redraw
        self.ax.draw_artist(self.ax.patch)
        for i in range(0, 4):
            self.lines[i].set_ydata(data[i])
            self.ax.draw_artist(self.lines[i])
        self.fig.canvas.update()
        self.fig.canvas.flush_events()

    # Class initialization
    def __init__(self, data_stream, **kwargs):
       # initialize super class (boxlayout)
       super(RealtimePlottingWidget, self).__init__(**kwargs)

       # grab parameters and save to class
       self.data_stream = data_stream # pointer to data; modified externally

       # initialize the plot
       self.fig = plt.figure(facecolor='#ffffff')
       self.ax = self.fig.add_subplot(111)
       self.ax.set_axis_bgcolor('#afafaf')
       self.lines = []
       self.colors = ["#ff0400", "#2dff38", "#0256f2", "#f2f202"]
       self.labels = ["Red", "Green", "Blue", "Yellow"]
       data = self.data_stream()
       self.x_vals = (np.arange(0, len(data[0])))

       for i in range(0, len(data)):
           self.lines.append(self.ax.plot(self.x_vals, data[i], lw=4, 
                                          color=self.colors[i],
                                          label=self.labels[i], marker="")[0])
       
       self.ax.set_ylim([0,1.01])
       self.ax.set_xlabel("old data <----- new data")
       self.ax.set_ylabel("Voltage (V)")
       self.ax.set_title("4 channel real time voltages")
       self.ax.hold()
       plt.show()
       self.fig.canvas.draw()
       self.add_widget(self.fig.canvas)
       self.clock = Clock.schedule_interval(self.update_plot, 1/25.0)

# testing
if __name__ == "__main__":
    from kivy.app import App
    
    def data_stream():
        return np.random.uniform(0,0.8,(4,25)) 

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = RealtimePlottingWidget(data_stream)
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
