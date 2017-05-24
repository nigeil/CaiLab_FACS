#!/bin/python
# Defines a button that, when pressed, will send over new threshold voltage
# values and cell selection count values to the microcontroller. It will then
# request this information from the microcontroller itself to verify that the
# new values have taken effect.

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class UpdateButton(Button):
    # Class variables
    
    # Class helper functions

    # send over voltage/cell count values when pressed
    def send_values(self, instance):
        # sending
        min_voltage_thresholds = self.min_voltage_sliders.get_slider_vals()
        max_voltage_thresholds = self.max_voltage_sliders.get_slider_vals()
        max_cell_counts = self.cell_counters.get_max_cell_vals()
        logic_states = self.logic_radio_buttons.get_logic_states()

        self.mc.send_threshold_voltages(min_voltage_thresholds, 
                                        max_voltage_thresholds)
        self.mc.send_max_cell_counts(max_cell_counts)
        self.mc.send_logic_states(logic_states)
        
        # TODO: check that new values from mc are == to what we set
        self.mc.parse_all_data()
        return


    # Class initialization
    def __init__(self, mc, min_voltage_sliders, max_voltage_sliders,
                 cell_counters, logic_radio_buttons, **kwargs):
        # initialize super class (button)
        super(UpdateButton, self).__init__(**kwargs)

        # grab parameters and save to class
        self.mc = mc
        self.min_voltage_sliders = min_voltage_sliders
        self.max_voltage_sliders = max_voltage_sliders
        self.cell_counters = cell_counters
        self.logic_radio_buttons = logic_radio_buttons
        
        # set button label text
        self.text = "Send values"
        
        # bind function to change button state based on running_status
        self.bind(on_press = self.send_values)

    
# Main widget class (boxlayout with two buttons side-by-side)
class UpdateButtonWidget(BoxLayout):
    # Class variables

    # Class helper functions

    # Class initialization
    def __init__(self, mc, min_voltage_sliders, max_voltage_sliders, 
                 cell_counters, logic_radio_buttons, **kwargs):
        # initialize super class (boxlayout)
        super(UpdateButtonWidget, self).__init__(orientation="horizontal", 
                                                                 **kwargs)

        # create buttons and add to horizontal boxlayout
        self.update_button = UpdateButton(mc, min_voltage_sliders, 
                                          max_voltage_sliders, cell_counters,
                                          logic_radio_buttons)
        self.add_widget(self.update_button)

# testing, run this script alone to get a box with two buttons placed side-by-
# side; stop button press will stop the start button if running

if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = UpdateButtonWidget()
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
