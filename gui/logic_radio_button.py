#!/bin/python
# Defines a set of radio buttons that will define whether PMT singals will be:
# ignored/logical OR'd/logical AND'd/logical NOT'd together with other signals

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

class LogicRadioButton(BoxLayout):
    # Class variables
    
    # possible states:
    # 0 -> off
    # 1 -> logical inclusive OR
    # 2 -> logical AND
    # 3 -> logical NOT
    logic_state = 0 
    logic_labels = ["IGNORE", "OR", "AND", "NOT"]

    # Class helper functions
    def get_logic_state(self):
        return self.logic_state
    
    # update the label and logic state upon text input box changes (bound function)
    def update_logic_state(self, instance, value):
        logic_label = instance.text 
        
        if (value == "down"): # button pressed, change logic state
            for i in range(0, len(self.logic_labels)):
                if (logic_label == self.logic_labels[i]):
                    self.logic_state = i
                    break

        elif (value == "normal"): # if no button is selected, default to IGNORE
            self.logic_state = 0
            logic_label = self.logic_labels[0]

        self.label.text = (self.label_text + "\n" + str(logic_label))

    # Class initialization
    def __init__(self, label_text, **kwargs):
        # initialize super class (boxlayout)
        super(LogicRadioButton, self).__init__(**kwargs)

        # grab parameters and save to class
        self.label_text = label_text

        # create the input box and bind update function
        self.radio_buttons = []
        for i in range(0, len(self.logic_labels)):
            self.radio_buttons.append(ToggleButton(text=self.logic_labels[i], 
                                                   group="logic_" + self.label_text,
                                                   size_hint=(1.0, 0.2)))
            self.radio_buttons[i].bind(state=self.update_logic_state)

        # create label with initial text
        self.label = Label(text=self.label_text + "\n" 
                           + str(self.logic_labels[0]), size_hint=(1.0,0.6))

        # add widgets to box layout
        self.add_widget(self.label)
        for b in self.radio_buttons:
            self.add_widget(b)
        
# testing, run this script alone to create a set of four textinputs with 
# changing labels that remain integers >= 0

if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = BoxLayout(orientation="horizontal")
            main_box.add_widget(LogicRadioButton(label_text="Red", orientation="vertical"))
            main_box.add_widget(LogicRadioButton(label_text="Green", orientation="vertical"))
            main_box.add_widget(LogicRadioButton(label_text="Blue", orientation="vertical"))
            main_box.add_widget(LogicRadioButton(label_text="Yellow", orientation="vertical"))
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()

