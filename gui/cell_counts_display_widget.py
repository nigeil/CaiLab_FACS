#!/bin/python
# Defines a set of 4 updateable labels that display the number of cells
# that have been selected for each channel

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class CellCountsDisplayWidget(BoxLayout):
    # Class variables
    cell_counts = [0,0,0,0]

    # Class helper functions
    def update_cell_counts(self, instance):
        self.cell_counts = self.mc.get_current_cell_counts()
        for i in range(0,4):
            self.cell_count_labels[i].text = str(self.cell_counts[i])


    def __init__(self, mc, title_text="Present number of cells selected (#)", **kwargs):
        # initialize super class (boxlayout)
        super(CellCountsDisplayWidget, self).__init__(orientation="vertical",**kwargs)

        # grab parameters and save to class
        self.title_text = title_text
        self.mc = mc

        # create title label and add to boxlayout
        self.add_widget(Label(text=self.title_text, size_hint=(1.0, 0.1)))

        # create sliders and add to secondary, horizontal boxlayout
        self.display_layout = BoxLayout(orientation="horizontal", size_hint=(1.0,0.9))
        self.displays = []
        self.box_labels = [Label(text=x) for x in ["Red", "Green", "Blue", "Yellow"]]
        self.cell_count_labels = [Label(text=str(x)) for x in self.cell_counts]
        for i in range(0, len(self.box_labels)):
            box = BoxLayout(orientation="vertical")
            box.add_widget(self.box_labels[i])
            box.add_widget(self.cell_count_labels[i])
            self.displays.append(box)
            self.display_layout.add_widget(self.displays[i])
        self.add_widget(self.display_layout)

# testing
if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = CellCountDisplayWidget()
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
