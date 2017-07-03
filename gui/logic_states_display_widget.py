#!/bin/python
# Defines a set of 4 updateable labels that display the logic states 
# that have been selected for each channel

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class LogicStatesDisplayWidget(BoxLayout):
    # Class variables
    logic_states = [0,0,0,0]

    # Class helper functions
    def update_logic_states(self, instance):
        self.logic_states = self.mc.get_logic_states()
        for i in range(0,4):
            the_state = ""
            if (self.logic_states[i] == 0):
                the_state = "IGNORE"
            elif (self.logic_states[i] == 1):
                the_state = "OR"
            elif (self.logic_states[i] == 2):
                the_state = "AND"
            elif (self.logic_states[i] == 3):
                the_state = "NOT"
            self.logic_state_labels[i].text = str(the_state)

    def __init__(self, mc, title_text="Present logic states", **kwargs):
        # initialize super class (boxlayout)
        super(LogicStatesDisplayWidget, self).__init__(orientation="vertical",**kwargs)

        # grab parameters and save to class
        self.title_text = title_text
        self.mc = mc

        # create title label and add to boxlayout
        self.add_widget(Label(text=self.title_text, size_hint=(1.0, 0.1)))

        # create sliders and add to secondary, horizontal boxlayout
        self.display_layout = BoxLayout(orientation="horizontal", size_hint=(1.0,0.9))
        self.displays = []
        self.box_labels = [Label(text=x) for x in ["Red", "Green", "Blue", "Yellow"]]
        self.logic_state_labels = [Label(text=str("IGNORE")) for x in self.logic_states]
        for i in range(0, len(self.box_labels)):
            box = BoxLayout(orientation="vertical")
            box.add_widget(self.box_labels[i])
            box.add_widget(self.logic_state_labels[i])
            self.displays.append(box)
            self.display_layout.add_widget(self.displays[i])
        self.add_widget(self.display_layout)

# testing
if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = LogicStatesDisplayWidget()
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
