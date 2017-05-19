#!/bin/python
# Defines a text box + label widget for inputting the number of cells
# to select for each channel. Add 4 for R-G-B-Y channels.

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class CellNumberInputBox(BoxLayout):
    # Class variables
    initial_cell_number = 1000000
    cell_number = initial_cell_number # stores current number of cells to select

    # Class helper functions
    def get_cell_number(self):
        return self.cell_number
    
    # takes an input string (from text input box) and converts to an
    # integer >= 0 corresponding to the number of cells to select
    # whilst handling bad input values
    def parse_valid_cell_number(self, input_string):
        new_cell_number = 0
        # Convert string from input box to integer
        try:
            new_cell_number = int(input_string)
        # Catch non-useable strings 
        except ValueError:
            new_cell_number = 0
            print("[ERROR] value " + input_string + 
                  " cannot be converted to valid cell number (integer >= 0)")
        # Catch negative values
        if (new_cell_number < 0):
            new_cell_number = 0
            print("[ERROR] value " + input_string + 
                  " must be above/equal to zero when converted to integer")
        # return at end
        return new_cell_number

    # update the label upon text input box changes (bound function)
    def update_cell_number(self, instance, value):
        self.cell_number = self.parse_valid_cell_number(value)
        self.label.text = (self.label_text + "\n" + str(self.cell_number))

    # Class initialization
    def __init__(self, label_text, **kwargs):
        # initialize super class (boxlayout)
        super(CellNumberInputBox, self).__init__(**kwargs)

        # grab parameters and save to class
        self.label_text = label_text

        # create the input box and bind update function
        self.input_box = TextInput(text=str(self.initial_cell_number), 
                                   multiline=False, size_hint=(1.0,0.5))
        self.input_box.bind(text=self.update_cell_number)

        # create label with initial text
        self.label = Label(text=self.label_text + "\n" 
                           + str(self.initial_cell_number), size_hint=(1.0,0.5))

        # add widgets to box layout
        self.add_widget(self.input_box)
        self.add_widget(self.label)
        
# testing, run this script alone to create a set of four textinputs with 
# changing labels that remain integers >= 0

if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = BoxLayout(orientation="horizontal")
            main_box.add_widget(CellNumberInputBox(label_text="Red"))
            main_box.add_widget(CellNumberInputBox(label_text="Green"))
            main_box.add_widget(CellNumberInputBox(label_text="Blue"))
            main_box.add_widget(CellNumberInputBox(label_text="Yellow"))
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()

