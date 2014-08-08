'''
Created on Aug 7, 2014

@author: Xuxion


*Requires Kivy to run.

You can get it from the Kivy site and run this .py by dragging it to kivy.bat
after the installation is extracted.

Getting Kivy to work with eclipse, however, really exhausted my Googling abilities...
'''


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window

class CardWidget(Widget):
    card_size = (Window.size[0]-40, Window.size[1]-40)
    card_pos = (Widget.x, Widget.y)
    text_position = (card_size[0]/2, card_size[1]/2)
    
    def __init__(self):
        Widget.__init__(self)
        
    def on_resize(self, width, height):
        card_size = (Window.size[0], Window.size[1])
        text_position = (card_size[0]/2, card_size[1]/2)
    
        


class FlashcardApp(App):
    def build(self):
        return CardWidget()

if __name__== '__main__':
   FlashcardApp().run()