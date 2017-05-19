#!/bin/python
# Creates the gui interface for the cell sorting system by
# adding the widgets from the gui folder. No actual widget definitions
# are included in this file.

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.config import Config
# Configuration options
Config.set('graphics', 'window_state', 'maximized')

from gui.cell_number_input_box_widget import CellNumberInputBoxWidget
from gui.logging_inputs import LoggingInputs
from gui.start_stop_buttons_widget import StartStopButtonsWidget
from gui.voltage_threshold_slider_widget import VoltageThresholdSliderWidget
from gui.realtime_statistics_widget_kivy import RealtimeStatisticsWidget
from gui.update_button_widget import UpdateButtonWidget
from gui.save_button_widget import SaveButtonWidget
from gui.cell_counts_display_widget import CellCountsDisplayWidget
from gui.threshold_voltage_display_widget import ThresholdVoltageDisplayWidget
from data_analysis.realtime_plotting_widget import RealtimePlottingWidget
from microcontroller.microcontroller_comms import Microcontroller

import numpy as np


class MainWindow(App):
    def my_data_stream(self):
        return np.random.uniform(4,1200, (100,4))

    def build(self):
        # create the microcontroller object and schedule its data refresh
        self.mc = Microcontroller()
        #self.mc_refresh_clock = Clock.schedule_interval(lambda dt: self.mc.parse_all_data, 0.5)

        self.root_widget = BoxLayout(orientation="horizontal")
        
        # left panel items
        self.left_panel = BoxLayout(orientation="vertical", size_hint=(0.4, 1.0))
        # TODO: add in realtime statistics when fast USB is available for Teensy 3.6
        #self.realtime_stats = RealtimeStatisticsWidget(self.mc.get_voltage_buffer,
        #                                               size_hint=(1.0, 0.8))
        #self.realtime_stats = RealtimeStatisticsWidget(self.my_data_stream)
        self.cell_counts_display = CellCountsDisplayWidget(self.mc, size_hint=(1.0,0.2))
        self.threshold_voltage_display = ThresholdVoltageDisplayWidget(self.mc, 
                                                                       size_hint=(1.0,0.2))

        # middle panel items
        self.middle_panel = BoxLayout(orientation="vertical", size_hint=(0.2, 1.0))
        self.logging_inputs = LoggingInputs(size_hint=(1.0,0.75))
        self.start_stop = StartStopButtonsWidget(self.mc, self.cell_counts_display, 
                                                 self.threshold_voltage_display,
                                                 size_hint=(1.0,0.15))
        
        # right panel items
        self.right_panel = BoxLayout(orientation="vertical", size_hint=(0.4, 1.0))
        self.min_voltage_sliders = VoltageThresholdSliderWidget(title_text="Minimum Selection threshold (mV)", 
                                                                size_hint=(0.45, 1.0))
        self.max_voltage_sliders = VoltageThresholdSliderWidget(title_text="Maximum Selection threshold (mV)", 
                                                                size_hint=(0.45, 1.0))
        self.cell_counters = CellNumberInputBoxWidget(size_hint=(1.0,0.2))
        self.update_button = UpdateButtonWidget(self.mc, self.min_voltage_sliders, 
                                                self.max_voltage_sliders, self.cell_counters, 
                                                size_hint=(1.0, 0.15))
        
        # extra items
        ## save_button - middle panel
        self.save_button = SaveButtonWidget(self.mc, self.min_voltage_sliders, self.max_voltage_sliders, 
                                            self.cell_counters, self.logging_inputs, 
                                            size_hint=(1.0, 0.1))

        # add all items to respective panels in correct order
        ## left panel items
        #self.left_panel.add_widget(self.realtime_stats)
        self.left_panel.add_widget(BoxLayout(size_hint=(1.0, 0.8)))
        self.left_panel.add_widget(self.cell_counts_display)
        self.left_panel.add_widget(self.threshold_voltage_display)
        ## middle panel items
        self.middle_panel.add_widget(self.logging_inputs)
        self.middle_panel.add_widget(self.save_button)
        self.middle_panel.add_widget(self.start_stop)
        ## right panel items
        ### combine min/max voltage slider widgets into one box, side-by-side
        self.voltage_sliders = BoxLayout(orientation="horizontal", size_hint=(1.0, 0.65))
        self.voltage_sliders.add_widget(self.min_voltage_sliders)
        self.voltage_sliders.add_widget(BoxLayout(orientation="horizontal", size_hint=(0.1, 1.0)))
        self.voltage_sliders.add_widget(self.max_voltage_sliders)
        self.right_panel.add_widget(self.voltage_sliders)
        self.right_panel.add_widget(self.cell_counters)
        self.right_panel.add_widget(self.update_button)


        # final assembly to root widget
        self.root_widget.add_widget(self.left_panel)
        self.root_widget.add_widget(BoxLayout(orientation="vertical", size_hint=(0.03, 1.0)))
        self.root_widget.add_widget(self.middle_panel)
        self.root_widget.add_widget(BoxLayout(orientation="vertical", size_hint=(0.03, 1.0)))
        self.root_widget.add_widget(self.right_panel)

        return self.root_widget
'''
    def __init__(self, **kwargs):
        #super(App, self).__init__(**kwargs)
        App.__init__(self, **kwargs)
        # spawn a realtime plotting widget separately before return the main 
        # window back to the caller process
        realtime_plot = RealtimePlottingWidstats)
        plot_process = mp.Process(target=realtime_plot.run, args=(self.data_queue,))
        plot_process.start()
'''

if __name__ == "__main__":
    
    # Run it
    MainWindow().run()

