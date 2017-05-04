#!/bin/python
# Defines a pair of input boxes that allow the user to
# i.) log information about an experiment, and
# ii.) select a directory to save experiment logs to

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

import datetime

class LoggingInputs(BoxLayout):
    # Class variables
    log_data = ""
    save_directory = ("/home/nigelmic/data/Documents/biophysics"
                     +"/CaiLab-Nigel/src/cell-sorter/test_data/") # default
    current_time = datetime.datetime.now()

    # Class helper functions
    def set_log_data(self, instance, value):
        self.log_data = value
    def get_log_data(self):
        return self.log_data
    def set_save_directory(self, instance, value):
        self.save_directory = value
    def get_save_directory(self):
        return self.save_directory


    # Class initialization
    def __init__(self, **kwargs):
        # initialize super class (boxlayout)
        super(LoggingInputs, self).__init__(orientation="vertical", **kwargs)

        # create the log input box + label
        self.log_label = Label(text="Comments on experimental procedure", 
                               size_hint=(1.0,0.1))
        self.log_input_box = TextInput(text=self.current_time.isoformat() + "\n", 
                                       multiline=True, size_hint=(1.0,0.6))
        self.log_input_box.bind(text=self.set_log_data)

        # create the save directory input box + label
        self.save_label = Label(text="Save directory (not file)", 
                                size_hint=(1.0,0.1))
        self.save_input_box = TextInput(text=self.save_directory, 
                                        multiline=False, size_hint=(1.0,0.1))
        self.save_input_box.bind(text=self.set_save_directory)

        # add widgets to box layout
        self.add_widget(self.log_label)
        self.add_widget(self.log_input_box)
        self.add_widget(self.save_label)
        self.add_widget(self.save_input_box)
        
# testing, run this script alone to create a set of four textinputs with 
# changing labels that remain integers >= 0

if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            root_widget.add_widget(LoggingInputs())
            return root_widget
    MyApp().run()

