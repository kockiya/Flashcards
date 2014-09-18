'''
Created on Sep 17, 2014

@author: Xuxion
'''
from kivy.metrics import *
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation, AnimationTransition
from kivy.graphics import *
from kivy.clock import Clock
from kivy.properties import *
from kivy.app import App
from kivy.animation import Animation, AnimationTransition

class FadingTextWidget(Label):
    def __init__(self, **kwargs):
        Label.__init__(self)
        for x in kwargs.items():
            setattr(self, x[0], x[1])
        
        if not hasattr(self, "text_color"):
            self.text_color = (1, 1, 1, 1)
        if not hasattr(self, "back_color"):
            self.back_color = (0, int("4a",16)/255, int("64",16)/255, .8)
        if not hasattr(self, "text"):
            self.text = "Hello World"
        if not hasattr(self, "duration"):
            self.duration = 4
        if not hasattr(self, "pad_x"):
            self.pad_x = 15
        if not hasattr(self, "pad_y"):
            self.pad_y = 5
        
        self.pos = (0,0)
        self.opacity = 0
        self.color = self.text_color
        
        self.rect = InstructionGroup()
        self.rect.add(Color(*self.back_color))
        self.rect.add(Rectangle(pos_hint=self.pos_hint, pos=(self.center_x-self.texture_size[0]/2, self.center_y-self.texture_size[1]/2),
                                 size=(self.texture_size[0]+10, self.texture_size[1])))

        self.canvas.before.add(self.rect)
        self.bind(texture_size=self.draw_rect)
        
        self.anim = {'fade_in':Animation(opacity=1, duration=.4), 'fade_out':Animation(opacity=0)}
        
        self.clock_fade_in = Clock.create_trigger(self.fade_in)
        self.clock_fade_out = Clock.create_trigger(self.fade_out, self.duration)
        
    def draw_rect(self, *args):
        self.rect.clear()
        self.rect.add(Color(*self.back_color))
        new_size_x = self.texture_size[0]+self.pad_x
        new_size_y = self.texture_size[1]+self.pad_y
        
        self.rect.add(Rectangle(pos_hint=self.pos_hint, pos=(self.center_x-new_size_x/2, self.center_y-new_size_y/2),
                                 size=(new_size_x, new_size_y)))
            
    def push_text(self, text=""):
        '''
        When this function is called, the label text will be changed. This function will
        also restart the fading animation (and cancel it if it is already underway)
        '''
        self.draw_rect()
        self.anim['fade_out'].stop(self.canvas)
        self.clock_fade_out.cancel()
        self.text = text
        self.fade_in()
    
    
    def fade_out(self, *args):
        self.anim['fade_out'].start(self.canvas)
        
    def fade_in(self, *args):
        self.anim['fade_in'].start(self.canvas)
        self.clock_fade_out()


if __name__== '__main__':
    class FadingTextApp(App):
        def build(self):
            fl = FloatLayout(size=Window.size)
            f = FadingTextWidget(text="Hello to the world asdasdadsa", pos_hint={'x':0,'y':-.4})
            fl.add_widget(f)
            
            return fl
    FadingTextApp().run()