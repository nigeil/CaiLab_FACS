#!/bin/python
# Defines a pair of buttons (start/stop) that allow control of program
# on/off state, after parameters are specified. This is added directly to
# the final interface.

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


# Classes StartButton and StopButton are linked together as
# the stop button will affect the start button's state.

class StartButton(Button):
    # Class variables
    running_status = False
    voltage_clock = None
    cell_count_clock = None
    logic_state_clock = None
    voltage_refresh_rate = 1.0/20000.0
    threshold_voltage_refresh_rate = 1.0/25.0
    cell_count_refresh_rate = 1.0/25.0
    logic_states_refresh_rate = 1.0/25.0
    
    # Class helper functions
    def get_running_status(self):
        return self.running_status
    
    def set_running_status(self, new_status):
        self.running_status = new_status
        if   (self.running_status == True):
            self.mc.send_run_state(True) # tell microcontroller to start sorting
            # TODO: reimplement voltage checking when fast USB is available for teensy 3.6
            #self.realtime_stats.set_running_status(True) # tell plotter to start plotting
            # start clocks to constantly poll data from the microcontroller while running
            #self.voltage_clock = Clock.schedule_interval(self.mc.parse_voltages,
            #                                             self.voltage_refresh_rate)
            
            self.cell_count_clock = Clock.schedule_interval(self.mc.parse_cell_counts,
                                                            self.cell_count_refresh_rate)
            self.cell_count_display_clock = Clock.schedule_interval(
                    self.cell_counts_display.update_cell_counts, self.cell_count_refresh_rate)
            self.threshold_voltage_clock = Clock.schedule_interval(self.mc.parse_threshold_voltages,
                                                            self.threshold_voltage_refresh_rate)
            self.threshold_voltage_display_clock = Clock.schedule_interval(
                    self.threshold_voltage_display.update_threshold_voltages, 
                    self.threshold_voltage_refresh_rate)
            self.logic_states_clock = Clock.schedule_interval(self.mc.parse_logic_states,
                                                            self.logic_states_refresh_rate)
            self.logic_states_display_clock = Clock.schedule_interval(
                        self.logic_states_display.update_logic_states, self.logic_states_refresh_rate)
            
            self.time_clock = Clock.schedule_interval(self.mc.parse_loop_time, self.logic_states_refresh_rate)
            def time_display(dt=0):
               print("[DEBUG] loop time: " + str(self.mc.get_current_loop_time()) + " us")
            self.time_display_clock = Clock.schedule_interval(time_display, self.logic_states_refresh_rate)
            
        elif (self.running_status == False):
            self.mc.send_run_state(False) # tell microcontroller to stop sorting
            #self.realtime_stats.set_running_status(False) # tell plotter to stop plotting
            # stop the clocks when stopped
            #self.voltage_clock.cancel()
            
            self.cell_count_clock.cancel()
            self.cell_count_display_clock.cancel()
            self.threshold_voltage_clock.cancel()
            self.threshold_voltage_display_clock.cancel()
            self.logic_states_clock.cancel()
            self.logic_states_display_clock.cancel()
            self.time_clock.cancel()
            self.time_display_clock.cancel()
             
        elif (self.running_status == "Paused"):
            self.mc.send_run_state("Paused")
            
            self.cell_count_clock.cancel()
            self.cell_count_display_clock.cancel()
            self.threshold_voltage_clock.cancel()
            self.threshold_voltage_display_clock.cancel()
            self.logic_states_clock.cancel()
            self.logic_states_display_clock.cancel()
            self.time_clock.cancel()
            self.time_display_clock.cancel()

    def set_text(self, new_text):
        self.text = new_text

    # change button state when pressed
    def start_press(self, instance):
        if (self.running_status == False):
            self.set_running_status(True)
            self.text = "Running..."
        elif (self.running_status == "Paused"):
            self.set_running_status(True)
            self.text = "Running..."
    
    # Class initialization
    #def __init__(self, mc, realtime_stats, **kwargs):
    def __init__(self, mc, cell_counts_display, threshold_voltage_display, 
                 logic_states_display, **kwargs):
        # initialize super class (button)
        super(StartButton, self).__init__(**kwargs)

        # grab parameters and save to class
        self.mc = mc                         # microcontroller object
        self.cell_counts_display = cell_counts_display
        self.threshold_voltage_display = threshold_voltage_display
        self.logic_states_display = logic_states_display
        #self.realtime_stats = realtime_stats # plotting object

        # set button label text
        self.text = "Start"
        
        # bind function to change button state based on running_status
        self.bind(on_press = self.start_press)

class StopButton(Button):
    # Class variables
    
    # Class helper functions
    
    # change start button state when pressed (halt operation)
    def stop_press(self, instance):
        self.running_status = self.start_button.get_running_status()
        if (self.running_status == True):
            self.start_button.set_running_status(False)
            self.start_button.set_text("Start")
    
    # Class initialization; start_button needs to be created first and passed
    # to the stop button
    def __init__(self, start_button, **kwargs):
        # initialize super class (button)
        super(StopButton, self).__init__(**kwargs)

        # get start_button and save as class pointer
        self.start_button = start_button
        
        # set button label text
        self.text = "Stop & reset"
        
        # bind function to change button state based on running_status
        self.bind(on_press = self.stop_press)

class PauseButton(Button):
    # Class variables
    
    # Class helper functions
    
    # change start button state when pressed (halt operation)
    def pause_press(self, instance):
        self.running_status = self.start_button.get_running_status()
        if (self.running_status == True):
            self.start_button.set_running_status("Paused")
            self.start_button.set_text("Resume")
    
    # Class initialization; start_button needs to be created first and passed
    # to the stop button
    def __init__(self, start_button, **kwargs):
        # initialize super class (button)
        super(PauseButton, self).__init__(**kwargs)

        # get start_button and save as class pointer
        self.start_button = start_button
        
        # set button label text
        self.text = "Pause"
        
        # bind function to change button state based on running_status
        self.bind(on_press = self.pause_press)


# Main widget class (boxlayout with two buttons side-by-side)
class StartStopButtonsWidget(BoxLayout):
    # Class variables

    # Class helper functions

    # Class initialization
    #def __init__(self, mc, realtime_stats, **kwargs):
    def __init__(self, mc, cell_counts_display, threshold_voltage_display,  
                 logic_states_display, **kwargs):
        # initialize super class (boxlayout)
        super(StartStopButtonsWidget, self).__init__(orientation="horizontal", 
                                                                 **kwargs)

        # create buttons and add to horizontal boxlayout
        #self.start_button = StartButton(mc, realtime_stats)
        self.start_button = StartButton(mc, cell_counts_display, threshold_voltage_display,
                                        logic_states_display)
        self.stop_button  = StopButton(self.start_button)
        self.pause_button = PauseButton(self.start_button)
        self.add_widget(self.start_button)
        self.add_widget(self.pause_button)
        self.add_widget(self.stop_button)

# testing, run this script alone to get a box with two buttons placed side-by-
# side; stop button press will stop the start button if running

if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = StartStopButtonsWidget()
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
