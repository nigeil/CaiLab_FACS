#!/bin/python
# Defines a self-contained widget with 4 voltage threshold sliders
# that will be added to the final interface

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from gui.voltage_threshold_slider import VoltageThresholdSlider

class VoltageThresholdSliderWidget(BoxLayout):
    # Class variables

    # Class helper functions
    def get_slider_vals(self):
        ret = []
        for slider in self.sliders:
            ret.append(slider.get_slider_val())
        #ret = list(reversed(ret))
        return ret

    def __init__(self, title_text="Selection Threshold (mV)", **kwargs):
        # initialize super class (boxlayout)
        super(VoltageThresholdSliderWidget, self).__init__(orientation="vertical", 
                                                                         **kwargs)

        # grab parameters and save to class
        self.title_text = title_text

        # create title label and add to boxlayout
        self.add_widget(Label(text=self.title_text, size_hint=(1.0, 0.1)))

        # create sliders and add to secondary, horizontal boxlayout
        slider_layout = BoxLayout(orientation="horizontal", size_hint=(1.0,0.9))
        self.sliders = []
        self.slider_labels = ["Red", "Green", "Blue", "Yellow"]
        for i in range(0, len(self.slider_labels)):
            self.sliders.append(VoltageThresholdSlider(self.slider_labels[i],
                                                       orientation="vertical"))
            slider_layout.add_widget(self.sliders[i])
        self.add_widget(slider_layout)

# testing, run this script alone to get a box with 4 vertical slider/labels
if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = VoltageThresholdSliderWidget()
            root_widget.add_widget(main_box)
            print("[DEBUG] slider vals = " + str(main_box.get_slider_vals()))
            return root_widget
    MyApp().run()
