#!/bin/python
# Defines the Slider + Label construct for voltage threshold selection
# Add 4 of these to get R-G-B-Y channels 

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider

class VoltageThresholdSlider(BoxLayout):
    # Class variables (not including ones created in __init__) 
    slider_val = 400      # mV
    slider_val_min = 0    # mV
    slider_val_max = 3300 # mV

    # Class helper functions 
    def update_slider_val(self, instance, value):
        self.slider_val = round(float(value),2)
        self.label.text = (self.label_text + "\n" + "{0:.0f}".format(self.slider_val * 4))
        #self.label.text = self.label_text + "\n" + "{0:.2f}".format(self.slider_val)
        # TODO: send to microcontroller (?, maybe in controller script)

    def get_slider_val(self):
        return self.slider_val

    # Class initialization
    def __init__(self, label_text, **kwargs):
        # initialize super class (boxlayout)
        super(VoltageThresholdSlider, self).__init__(**kwargs)

        # grab parameters and save to class
        self.label_text = label_text 

        # create slider and its attached label
        self.slider = Slider(min=self.slider_val_min, max=self.slider_val_max, 
                             value=self.slider_val, orientation="vertical", 
                             size_hint=(1.0, 0.8))
        self.label = Label(text=label_text + "\n" + 
                                "{0:.0f}".format(self.slider_val), 
                                size_hint=(1.0, 0.2))

        # bind the update_slider_val function to the value of the slider
        # i.e. make the func. get called every time the value changes
        self.slider.bind(value=self.update_slider_val)
        
        # add slider and label to box layout
        self.add_widget(self.slider)
        self.add_widget(self.label)



# testing, run this script alone to create a box with 4 vertical slider/labels
if __name__ == "__main__":
    from kivy.app import App
    
    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            root_widget.add_widget(Label(text="Selection Threshold (mV)", size_hint=(1.0,0.1)))
            main_box = BoxLayout(orientation="horizontal")
            main_box.add_widget(VoltageThresholdSlider("Red",orientation="vertical"))
            main_box.add_widget(VoltageThresholdSlider("Green",orientation="vertical"))
            main_box.add_widget(VoltageThresholdSlider("Blue",orientation="vertical"))
            main_box.add_widget(VoltageThresholdSlider("Yellow",orientation="vertical"))
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
