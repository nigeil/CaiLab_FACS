#!/bin/python
# Defines a set of 4 updateable labels that display the current voltage 
# thresholds for each channel as reported by the microcontroller

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class ThresholdVoltageDisplayWidget(BoxLayout):
    # Class variables
    threshold_voltages = [0,0,0,0]

    # Class helper functions
    def update_threshold_voltages(self, instance):
        self.threshold_voltages = self.mc.get_threshold_voltages()
        for i in range(0,4):
            self.threshold_voltage_labels[i].text = str(self.threshold_voltages[i])


    def __init__(self, mc, title_text="Presently set threshold voltages (mV)", **kwargs):
        # initialize super class (boxlayout)
        super(ThresholdVoltageDisplayWidget, self).__init__(orientation="vertical",**kwargs)

        # grab parameters and save to class
        self.title_text = title_text
        self.mc = mc

        # create title label and add to boxlayout
        self.add_widget(Label(text=self.title_text, size_hint=(1.0, 0.1)))

        # create sliders and add to secondary, horizontal boxlayout
        self.display_layout = BoxLayout(orientation="horizontal", size_hint=(1.0,0.9))
        self.displays = []
        self.box_labels = [Label(text=x) for x in ["Red", "Green", "Blue", "Yellow"]]
        self.threshold_voltage_labels = [Label(text=str(x)) for x in self.threshold_voltages]
        for i in range(0, len(self.box_labels)):
            box = BoxLayout(orientation="vertical")
            box.add_widget(self.box_labels[i])
            box.add_widget(self.threshold_voltage_labels[i])
            self.displays.append(box)
            self.display_layout.add_widget(self.displays[i])
        self.add_widget(self.display_layout)

# testing
if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = ThresholdVoltageDisplayWidget()
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
