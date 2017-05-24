#!/bin/python
# Defines a self-contained widget with 4 sets  of logic radio buttons 
# that will be added to the final interface.

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
if (__name__ != "__main__"):
    from gui.logic_radio_button import LogicRadioButton

class LogicRadioButtonWidget(BoxLayout):
    # Class variables
    logic_states = [0,0,0,0]

    # Class helper functions
    def get_logic_states(self):
        self.parse_logic_states()
        return self.logic_states

    def set_title_text(self, new_text):
        self.title.text=(self.title_text + "\n" + str(new_text))

    def parse_logic_states(self):
        n_2s = 0 # number of buttons in the '2'/'AND' state
        
        for i in range(0, len(self.radio_buttons)):
            self.logic_states[i] = self.radio_buttons[i].get_logic_state()
            if (self.logic_states[i] == 2):
                n_2s += 1

        if (n_2s == 1): # can't use only one channel with AND
            print("[ERROR] only 1 channel has AND selected" +
                  " as a logical condition; [0,2,3,4] must be" +
                  " selected with AND. Defaulting to OR.")
            for i in range(0, len(self.radio_buttons)):
                if (self.logic_states[i] == 2):
                    self.logic_states[i] = 1
            


    def __init__(self, title_text="Logical conditions", **kwargs):
        # initialize super class (boxlayout)
        super(LogicRadioButtonWidget, self).__init__(orientation="vertical",**kwargs)

        # grab parameters and save to class
        self.title_text = title_text

        # create title label and add to boxlayout
        self.title = Label(text=self.title_text, size_hint=(1.0, 0.1))
        self.add_widget(self.title)

        # create radio buttons and add to secondary, horizontal boxlayout
        radio_buttons_layout = BoxLayout(orientation="horizontal", size_hint=(1.0,0.9))
        self.radio_buttons = []
        self.radio_button_labels = ["Red", "Green", "Blue", "Yellow"]
        for i in range(0, len(self.radio_button_labels)):
            self.radio_buttons.append(LogicRadioButton(self.radio_button_labels[i],
                                                       orientation="vertical"))
            radio_buttons_layout.add_widget(self.radio_buttons[i])
        self.add_widget(radio_buttons_layout)

# testing
if __name__ == "__main__":
    from kivy.app import App
    from logic_radio_button import LogicRadioButton

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = LogicRadioButtonWidget()
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
