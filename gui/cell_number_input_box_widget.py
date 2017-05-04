#!/bin/python
# Defines a self-contained widget with 4 voltage threshold sliders
# that will be added to the final interface

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from gui.cell_number_input_box import CellNumberInputBox

class CellNumberInputBoxWidget(BoxLayout):
    # Class variables

    # Class helper functions
    def get_max_cell_vals(self):
        ret = []
        for input_box in self.input_boxes:
            ret.append(input_box.get_cell_number())
        return ret

    def __init__(self, title_text="Number of cells to select", **kwargs):
        # initialize super class (boxlayout)
        super(CellNumberInputBoxWidget, self).__init__(orientation="vertical",**kwargs)

        # grab parameters and save to class
        self.title_text = title_text

        # create title label and add to boxlayout
        self.add_widget(Label(text=self.title_text, size_hint=(1.0, 0.1)))

        # create sliders and add to secondary, horizontal boxlayout
        input_boxes_layout = BoxLayout(orientation="horizontal", size_hint=(1.0,0.9))
        self.input_boxes = []
        self.box_labels = ["Red", "Green", "Blue", "Yellow"]
        for i in range(0, len(self.box_labels)):
            self.input_boxes.append(CellNumberInputBox(self.box_labels[i],
                                                       orientation="vertical"))
            input_boxes_layout.add_widget(self.input_boxes[i])
        self.add_widget(input_boxes_layout)

# testing
if __name__ == "__main__":
    from kivy.app import App

    class MyApp(App):
        def build(self):
            root_widget = BoxLayout(orientation="vertical")
            main_box = CellNumberInputBoxesWidget()
            root_widget.add_widget(main_box)
            return root_widget
    MyApp().run()
