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
from kivy.animation import Animation, AnimationTransition
from kivy.graphics import *
from kivy.clock import Clock

class CardWidget(Widget):
    def recalc_pos(self, *args):
        """
            Used whenever the Window size changes. The window size somtimes changes rapidly 
            from full screen when the program is first launched, so this is also ran .5 seconds after __init__.
            
        """
        
        #Window -> self.parent
        self.card_size = (self.parent.size[0]-40, float(self.parent.size[1]-40))
        self.card_pos = ((self.parent.size[0] - self.card_size[0])/4, (self.parent.size[1] - self.card_size[1])/4)#Centered in self.parent
        self.card_center = self.parent.center
        self.text_position = self.card_center
        self.widgets['card_text'].center = self.card_center
        self.widgets['card_text_ref'].center = self.card_center

        self.card_base.size = self.card_size
        
        self.zoom_out_size = (self.card_size[0]*.9,self.card_size[1]*.9)
        self.cardflip_animations = {'zoom_in':Animation(size=self.card_size,duration=.5), 
                                    'zoom_out':Animation(size=self.zoom_out_size, duration=.3),
                                    'text_zoom_in': Animation(font_size=15, duration=.01),
                                    'text_zoom_out':Animation(font_size=12, duration=.3),
                                    'zoom_in_out': (Animation(size=self.zoom_out_size, duration=.3)+Animation(size=self.card_size,duration=.5)),
                                    'flip_start': Animation(size=(0, self.zoom_out_size[1]),duration=.2),
                                    'flip_end': Animation(size=self.zoom_out_size,duration=.2),
                                    'is_playing': False}
        
        self.card_snapback_animation = Animation(center=self.card_center,duration=.1)
        
        self.offscreen_animations = {'rightward_leave': Animation(center_x=self.card_center[0]*3, duration=.2),
                                     'leftward_leave': Animation(center_x=-self.card_center[0], duration=.2),
                                     'from_side_to_center': Animation(center=self.card_center, duration=.15),
                                     'fade_out': Animation(opacity=.5,duration=.2),
                                     'fade_in': Animation(opacity=1, duration=.2),
                                     'shrink': Animation(size=(self.card_size[0]*.5, self.card_size[1]*.5), duration=.2),
                                     'grow': Animation(size=self.card_size, duration = .45),
                                     'is_playing':False
                                     }
        
        #def disable_trans(*args):
        #    self.card_base.do_translation_x = False
        #def enable_trans(*args):
        #    self.card_base.do_translation_x = True
        #self.cardflip_animations['zoom_out'].bind(on_start=disable_trans)
        #self.cardflip_animations['zoom_in'].bind(on_complete=enable_trans)
        
        
        self.redraw_card_base()
        
        
    def __init__(self):
        Widget.__init__(self)
        self.init_bool_pos = False
        self.card_size = (float(Window.size[0]-40), float(Window.size[1]-40))
        self.card_pos = ((Window.size[0] - self.card_size[0])/4, (Window.size[1] - self.card_size[1])/4)#Centered in Window
        self.card_center = Window.center
        self.text_position = self.card_center
        #Create a Scatter Widget and Add a Rectangle to it's Canvas
        self.card_base = Scatter(size=self.card_size, center=self.card_center, do_rotation=False, do_translation_y=False, scale_min=.9, scale_max=1)
        self.shape = {'card_base_rect': Rectangle(size=self.card_base.size, center=self.card_base.center)}
        with self.card_base.canvas.before:
            Color(255,255,255)
        self.card_base.canvas.before.add(self.shape['card_base_rect'])
        
        
        #Create a Label Widget
        self.widgets = {'card_text':Label(center=self.card_center, size=(20,20), font_size=15, text='Hello', color=[0,0,0,1]),
                        'card_text_ref':Label(center=self.card_center, size=(20,20), font_size=15, text='Hello', color=[0,0,0,1])}
        def update_text(*args):
            #if self.card_base.size[0] == self.card_size[0] and self.card_base.size[1] == self.card_size[1]:
            self.widgets['card_text'].center = self.card_base.center
            
        #Bindings
        self.card_base.bind(size=self.redraw_card_base, center=update_text)
        Window.bind(on_resize=self.recalc_pos)
        
        #Add card_label as a child to the card_base, then card_base as a child to self
        #self.card_base.add_widget(self.card_label)
        
        self.add_widget(self.card_base)
        self.add_widget(self.widgets['card_text'],len(self.children))
        
        #Animations are Initialized in recalc_pos()
            #recalc_pos() is scheduled because sometimes (randomly) the application will try to start in 
            #Full screen but will quickly resize to the default (800x600) which will screw up all coordinates
            #since they are relative until on_resize() is called
        Clock.schedule_once(lambda *args: self.recalc_pos(),.5)
        
    def redraw_card_base(self, *args):
        self.card_base.center = self.card_center
        self.remove_widget(self.widgets['card_text'])
        
        self.card_base.canvas.before.remove(self.shape['card_base_rect'])
        self.shape['card_base_rect'] = Rectangle(size=self.card_base.size, center=self.card_base.center)
        self.card_base.canvas.before.add(self.shape['card_base_rect'])
        
        self.widgets['card_text'] = Label(center=self.card_center, size=(20,20), font_size=self.widgets['card_text_ref'].font_size,
                                           text='Hello', color=[0,0,0,1])
        self.add_widget(self.widgets['card_text'])
        self.widgets['card_text'].center = self.card_center
 

        
    def flip_animation(self):
        #self.cardflip_animations['zoom_in_out'].start(self.card_base)
        card_zoom_a = self.cardflip_animations['zoom_out']
        card_zoom_b = self.cardflip_animations['zoom_in']
        text_zoom = self.cardflip_animations['text_zoom_out']+self.cardflip_animations['text_zoom_in']
        text_zoom.start(self.widgets['card_text_ref'])
        
        f_e = p = self.cardflip_animations['flip_end']
        f_s = self.cardflip_animations['flip_start']
        def toggle_is_playing(*args):
            self.cardflip_animations['is_playing'] = not self.cardflip_animations['is_playing']
            card_zoom_a.stop(self.card_base)
            card_zoom_b.stop(self.card_base)
            text_zoom.stop(self.card_base)
            f_e.stop(self.card_base)
            f_s.stop(self.card_base)
            card_zoom_b.unbind(on_complete=toggle_is_playing)
            card_zoom_a.unbind(on_complete=at_zoom_end)
        def final_zoom(*args):
            f_e.unbind(on_complete=final_zoom)
            card_zoom_b.start(self.card_base)
        def at_flip_end(*args):
            f_s.unbind(on_complete=at_flip_end)
            f_e.bind(on_complete=final_zoom)
            f_e.start(self.card_base)
        def at_zoom_end(*args):
            f_s.bind(on_complete=at_flip_end)
            f_s.start(self.card_base)
        
        card_zoom_b.bind(on_complete=toggle_is_playing)
        card_zoom_a.bind(on_complete=at_zoom_end)
        card_zoom_a.start(self.card_base)
        
        
        
        #(self.cardflip_animations['zoom_out']+self.cardflip_animations['zoom_in']).start(self.card_base)
    
    def offscreen_animation(self, right_mode):
        ret_to_center = self.offscreen_animations['grow']&self.offscreen_animations['from_side_to_center']
        z = self.offscreen_animations['shrink']&self.offscreen_animations['rightward_leave']
        y = self.offscreen_animations['shrink']&self.offscreen_animations['leftward_leave']
        
        def toggle_is_playing(*args):
            self.offscreen_animations['is_playing'] = False
            #ret_to_center.stop(self.card_base)
            #if right_mode:
            #    z.unbind(on_complete=begin_entrance_y)
            #else:
                #y.unbind(on_complete=begin_entrance_y)
            #ret_to_center.unbind(on_complete=toggle_is_playing)
        if right_mode:
            def begin_entrance_z(*args):
                self.card_base.center_x = -self.card_center[0]*.4
                ret_to_center.bind(on_complete=toggle_is_playing)
                ret_to_center.start(self.card_base)
            z.bind(on_complete=begin_entrance_z)
            z.start(self.card_base)
        else: #left mode
            def begin_entrance_y(*args):
                self.card_base.center_x = self.card_center[0]*2.5
                ret_to_center.bind(on_complete=toggle_is_playing)
                ret_to_center.start(self.card_base)
            y.bind(on_complete=begin_entrance_y)
            y.start(self.card_base)
            
    def on_touch_up(self, touch):
        '''
        Goals:
            -If the card is released very close to the original position, it should play a flip animation.
            -When the card is released further, it should transition back to it's original position.
            -If the card is released at a point where half of it's face is offscreen, the card should
                transition off screen and another card should transition on screen.
        '''
        if self.card_base.center[0] < self.card_center[0]+5 and self.card_base.center[0] > self.card_center[0]-5:
            #Do flip
            if not self.cardflip_animations['is_playing']:
                self.cardflip_animations['is_playing'] = True
                self.flip_animation()
        elif self.card_base.center[0] > (self.card_center[0]*1.65):
            #Do offscreen/onscreen transition rightwards
            self.offscreen_animations['is_playing'] = True
            self.offscreen_animation(True)
        elif self.card_base.center[0] < (self.card_center[0]*.35):
            #Do offscreen/onscreen transition leftwards
            self.offscreen_animations['is_playing'] = True
            self.offscreen_animation(False)
        else:
            #Do transition-to-origin
            self.card_snapback_animation.start(self.card_base)
        
    
    def on_touch_down(self, touch):
        #print('Card Text Center',self.widgets['card_text'].center)
        #print('Card_Center',self.card_center)
        #print('Card_base.center',self.card_base.center)
        #print()
        if self.offscreen_animations['is_playing'] == False and self.cardflip_animations['is_playing'] == False:
            self.card_base.on_touch_down(touch)
        self.remove_widget(self.widgets['card_text'])
        self.widgets['card_text'] = Label(center=self.card_base.center, size=(20,20), font_size=15, text='Hello', color=[0,0,0,1])
        self.add_widget(self.widgets['card_text'])
        self.widgets['card_text'].center = self.card_base.center
        
        #self.card_snapback_animation.stop(self.card_base)
    
    def on_resize(self):
        print('omgomg')
        


class FlashcardApp(App):
    def build(self):
        return CardWidget()

if __name__== '__main__':
   FlashcardApp().run()