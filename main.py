import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix import anchorlayout,boxlayout,image,button
from kivy.graphics import Line,Rectangle,Color

import pack.ui_main_screen as ui_main_screen

class MyApp(App):

    def build(self):
        root = self.buildMain()
        return root
    
    def buildMain(self):
        root = anchorlayout.AnchorLayout()
        root.add_widget(ui_main_screen.NodeView())
        return root
    
if __name__ == '__main__':
    MyApp().run()