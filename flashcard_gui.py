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


class TestWidget(Widget):
    pass
        


class FlashcardApp(App):
    def build(self):
        return TestWidget()

if __name__== '__main__':
   FlashcardApp().run()