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
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.graphics import *

class CardWidget(Widget):
    card_size = (Window.size[0]-40, Window.size[1]-40)
    card_pos = ((Window.size[0] - card_size[0])/4, (Window.size[1] - card_size[1])/4)#Centered in Window
    text_position = (card_size[0]/2, card_size[1]/2)

        
    def __init__(self):
        Widget.__init__(self)
        #Create a Scatter Widget and Add a Rectangle to it's Canvas
            #Let's worry about behavior on window resize later ...
        self.card_base = Scatter(size=CardWidget.card_size, pos=CardWidget.card_pos, do_rotation=False, do_translation_y=False, scale_min=.9, scale_max=1)
        self.shape = {'card_base_rect': Rectangle(size=self.card_base.size, pos=self.card_base.pos)}
        with self.card_base.canvas.before:
            Color(255,255,255)
        self.card_base.canvas.before.add(self.shape['card_base_rect'])
        self.card_base.bind(size=self.redraw_card_base)
        #self.card_base.canvas.before.add(Rectangle(size=CardWidget.card_size, pos=(self.pos[0]+20, self.pos[1]+20)))
        #Create a Label Widget
        self.card_label = Label(pos=CardWidget.text_position, size=(min(self.size)*0.2, min(self.size)*0.2), text='Hello', color=[0,0,0,1])
        
        #Add card_label as a child to the card_base, then card_base as a child to CardWidget
        self.card_base.add_widget(self.card_label)
        self.add_widget(self.card_base)
        
        #Intialize Animations
        self.card_anim = Animation(x=CardWidget.card_pos[0], y=CardWidget.card_pos[1],duration=.1)
        self.cardflip_animations = {'zoom_in':Animation(size=(CardWidget.card_size[0]/.5,CardWidget.card_size[1]/.5)), 
                                    'zoom_out':Animation(size=(CardWidget.card_size[0]*.7,CardWidget.card_size[1]*.7)),
                                    'pause':Animation(pos=self.card_base.pos, duration=.5)}
        
    def redraw_card_base(self, *args):
        self.card_base.canvas.before.remove(self.shape['card_base_rect'])
        self.shape['card_base_rect'] = Rectangle(size=self.card_base.size, pos=self.card_base.pos)
        self.card_base.canvas.before.add(self.shape['card_base_rect'])
        
    def flip_animation(self):
        print('card_base_size',self.card_base.size)
        self.cardflip_animations['zoom_out'].stop(self.card_base)
        self.cardflip_animations['zoom_out'].start(self.card_base)

        self.redraw_card_base()
        #self.cardflip_animations['pause'].start(self.card_base)
        #self.cardflip_animations['zoom_in'].start(self.card_base)
        
    def on_touch_up(self, touch):
        '''
        Goals:
            -If the card is released very close to the original position, it should play a flip animation.
            -When the card is released further, it should transition back to it's original position.
            -If the card is released at a point where half of it's face is offscreen, the card should
                transition off screen and another card should transition on screen.
        '''
        if self.card_base.pos[0] < 15 and self.card_base.pos[0] > -15:
            print("TROLOLOL")
            #Do flip
            self.flip_animation()
        elif self.card_base.pos[0] > CardWidget.card_size[0]/2 or self.card_base.pos[0] < -CardWidget.card_size[0]/2:
            #Do offscreen/onscreen transition
            pass
        else:
            #Do transition-to-origin
            self.card_anim.start(self.card_base)
        print(self.card_base.pos)
        
    
    def on_touch_down(self, touch):
        self.card_base.on_touch_down(touch)
        self.card_anim.stop(self.card_base)
    
    
        


class FlashcardApp(App):
    def build(self):
        return CardWidget()

if __name__== '__main__':
   FlashcardApp().run()