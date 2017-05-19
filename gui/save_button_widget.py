#!/bin/python
# Defines a button that, when pressed, will save:
# i.) comments on the experimental procedure
# ii.) the current voltage selection thresholds
# iii.) the current desired cell counts
# iv.) compressed arrays of the actual voltage traces
# v.) how many cells were finally selected
# All of this is saved to files in the user-specified directory, overwriting 
# what might have been there before (save at will)

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import datetime
from numpy import savetxt

class SaveButton(Button):
    # Class variables
    save_dir = ""
    
    # Class helper functions

    # set the save directory
    def set_save_dir(self):
        self.save_dir = self.logging_inputs.get_save_directory()

    # create save string with all data except voltage traces
    def create_save_string(self):
        # collect information
        min_voltage_thresholds = self.min_voltage_sliders.get_slider_vals()
        max_voltage_thresholds = self.max_voltage_sliders.get_slider_vals()
        max_cell_counts = self.cell_counters.get_max_cell_vals()
        cells_selected = self.mc.get_current_cell_counts()
        comments = self.logging_inputs.get_log_data()
        
        # make a nice string out of it
        ret = ""
        ret += "=== BEGIN LOG ===\n"
        ret += comments
        ret += "\n== SETTINGS/STATS ==\n"
        ret += "Minimum threshold voltages (mV, [RGBY]): "
        ret += str(min_voltage_thresholds)
        ret += "Maximum threshold voltages (mV, [RGBY]): "
        ret += str(max_voltage_thresholds)
        ret += "\nNumber of cells to select (#, [RGBY]): " 
        ret += str(max_cell_counts)
        ret += "\nNumber of cells actually selected (#, [RGBY]): "
        ret += str(cells_selected) 
        ret += "\n=== END LOG ==="
        return ret

    # save everything to appropriate files
    def save_everything(self, instance):
        # get the save directory and set it locally
        self.set_save_dir()
        # make a log data string
        log_save_str = self.create_save_string()
        # get the voltage traces from the microcontroller-controller object
        # TODO: reimplement voltage tracking when Teensy 3.6 high-speed USB is done
        #voltage_traces = self.mc.get_voltage_storage()
        # get date to prepend to the filenames
        date = str(datetime.date.today().isoformat())

        # save the log data
        log_filename = (self.save_dir + date + "_log.txt")
        print("[DEBUG] log filename: " + str(log_filename))
        try:
            f = open(log_filename, "w")
        except IOError:
            print("[ERROR] unable to open file for writing: " + str(filename))
            return -1
        f.write(log_save_str)
        f.close()
        
        # save the voltage traces, in g-zip compressed csv format
        #voltage_traces_filename = (self.save_dir + date + "_voltage_traces.csv.gz")
        #print("[DEBUG] voltage traces filename: " + str(voltage_traces_filename))
        #voltage_traces_header = str("red,green,blue,yellow")
        #savetxt(voltage_traces_filename, voltage_traces, delimiter = ",") 



    # Class initialization
    def __init__(self, mc, min_voltage_sliders, max_voltage_sliders, 
                 cell_counters, logging_inputs, **kwargs):
        # initialize super class (button)
        super(SaveButton, self).__init__(**kwargs)

        # grab parameters and save to class
        self.mc = mc
        self.min_voltage_sliders = min_voltage_sliders
        self.max_voltage_sliders = max_voltage_sliders
        self.cell_counters = cell_counters
        self.logging_inputs = logging_inputs
        
        # set button label text
        self.text = "Save"
        
        # bind function to change button state based on running_status
        self.bind(on_press = self.save_everything)

    
# Main widget class (boxlayout with 1 button)
class SaveButtonWidget(BoxLayout):
    # Class variables

    # Class helper functions

    # Class initialization
    def __init__(self, mc, min_voltage_sliders, max_voltage_sliders, 
                 cell_counters, logging_inputs, **kwargs):
        # initialize super class (boxlayout)
        super(SaveButtonWidget, self).__init__(orientation="horizontal", 
                                                                 **kwargs)

        # create buttons and add to horizontal boxlayout
        self.save_button = SaveButton(mc, min_voltage_sliders, max_voltage_sliders, 
                                      cell_counters, logging_inputs)
        self.add_widget(self.save_button)

# testing, run this script alone to get a box with two buttons placed side-by-
# side; stop button press will stop the start button if running

if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = SaveButtonWidget()
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
