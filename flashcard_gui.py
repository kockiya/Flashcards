'''
Created on Aug 7, 2014

@author: Xuxion


*Requires Kivy to run.

You can get it from the Kivy site and run this .py by dragging it to kivy.bat
after the installation is extracted.

Getting Kivy to work with eclipse, however, really exhausted my Googling abilities...
'''

from deck import *
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation, AnimationTransition
from kivy.graphics import *
from kivy.clock import Clock

class DeckWidget(Widget):
    def recalc_pos(self, *args):
        """
            Used whenever the Window size changes. The window size sometimes changes rapidly 
            from full screen when the program is first launched, so this is also ran .5 seconds after __init__.
            
        """
        #Window -> self.parent
        self.card_size = (self.parent.size[0]-40, float(self.parent.size[1]-40))
        self.card_pos = ((self.parent.size[0] - self.card_size[0])/4, (self.parent.size[1] - self.card_size[1])/4)#Centered in self.parent
        self.card_center = self.parent.center
        self.text_position = self.card_center
        self.text_content = str(self.deck.selected) if len(self.deck) > 0 else "(Add a card to begin)"
        self.widgets['card_text'].center = self.card_center
        self.widgets['card_text_ref'].center = self.card_center
        self.touch_move_counter = 0
        self.card_base.size = self.card_size
        
        self.zoom_out_size = (self.card_size[0]*.9,self.card_size[1]*.9)
        self.cardflip_animations = {'zoom_in':Animation(size=self.card_size,duration=.5), 
                                    'zoom_out':Animation(size=self.zoom_out_size, duration=.3),
                                    'text_zoom_in': Animation(font_size=15, duration=.5),
                                    'text_zoom_out':Animation(font_size=12, duration=.3),
                                    'zoom_in_out': (Animation(size=self.zoom_out_size, duration=.3)+Animation(size=self.card_size,duration=.5)),
                                    'flip_start': Animation(size=(0, self.zoom_out_size[1]),duration=.2),
                                    'flip_end': Animation(size=self.zoom_out_size,duration=.2),
                                    'is_playing': False,
                                    'down_success': False}
        
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
        
        
        self.redraw_card_base()
        
        
    def __init__(self, l=[]):
        self.deck = Deck(l)
        self.deck.add_from_txt("test.txt")
        Widget.__init__(self)
        self.card_size = (float(Window.size[0]-40), float(Window.size[1]-40))
        self.card_center = Window.center
        self.text_position = self.card_center
        self.text_content = str(self.deck.selected) if len(self.deck) > 0 else "(Add a card to begin)"

        #Creation of Scatter-Rectangle
        self.card_base = Scatter(size=self.card_size, center=self.card_center, do_rotation=False, do_translation_y=False, scale_min=.9, scale_max=1)
        self.shape = {'card_base_rect': Rectangle(size=self.card_base.size, center=self.card_base.center)}
        self.card_base.canvas.before.add(Color(255,255,255))
        self.card_base.canvas.before.add(self.shape['card_base_rect'])
    
        #Creation of Label Widget
        self.widgets = {'card_text':Label(center=self.card_center, size=(20,20), font_size=15, text=self.text_content, color=[0,0,0,1]),
                        'card_text_ref':Label(center=self.card_center, size=(20,20), font_size=15, text=self.text_content, color=[0,0,0,1])}
        #Bindings
        def update_text(*args):
            self.widgets['card_text'].center = self.card_base.center
        self.card_base.bind(size=self.redraw_card_base, center=update_text)
        Window.bind(on_resize=self.recalc_pos)
        
        self.add_widget(self.card_base)
        self.add_widget(self.widgets['card_text'],len(self.children))
        
        Clock.schedule_once(self.recalc_pos,.5)
    
    
    
    def change_card_text(self, new_text):
        self.text_content = new_text
        self.widgets['card_text'].text = self.text_content
        
    def update_selected_text(self):
        self.change_card_text(str(self.deck.get_selected()))
        
    def redraw_card_base(self, *args):
        """
            Redraws the card. I had issues with canvas ordering and the text would never be drawn on top of the rectangle
            as the rectangle seemed to be always put on top during an animation. So the label widget is removed and redrawn
            after the rectangle is removed and redrawn.
            
            This is called every time an animation occurs that modifies the rectangle size.
        """
        self.card_base.center = self.card_center
        self.remove_widget(self.widgets['card_text'])
        
        self.card_base.canvas.before.remove(self.shape['card_base_rect'])
        self.shape['card_base_rect'] = Rectangle(size=self.card_base.size, center=self.card_base.center)
        self.card_base.canvas.before.add(self.shape['card_base_rect'])
        
        self.widgets['card_text'] = Label(center=self.card_center, size=(20,20), font_size=self.widgets['card_text_ref'].font_size,
                                           text=self.text_content, color=[0,0,0,1])
        self.add_widget(self.widgets['card_text'])
        self.widgets['card_text'].center = self.card_center
 

        
    def flip_animation(self):
        """
            Plays a series of animations that will cause the rectangle to appear to flip. Local functions
            are defined for the purpose of being bound when certain animations are complete. This way
            I would be able to do things in the background after certain animations are complete
            (i.e. when card is at the apex of the flip animation and is hardly visible, I want to
            change the stuff on the card in the at_flip_end() function.)
        """
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
            self.deck.get_selected().flip()
            self.update_selected_text()
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
        """
            Similar to flip animation. When at the end of the first offscreen transition, I'd want to
            change the stuff on the card which could be done through the local  begin_entrance() functions
        """
        ret_to_center = self.offscreen_animations['grow']&self.offscreen_animations['from_side_to_center']
        z = self.offscreen_animations['shrink']&self.offscreen_animations['rightward_leave']
        y = self.offscreen_animations['shrink']&self.offscreen_animations['leftward_leave']
        
        def toggle_is_playing(*args):
            self.offscreen_animations['is_playing'] = False
        if right_mode:
            def begin_entrance_z(*args):
                self.deck.get_selected().reset()
                self.deck.prev(self.deck.mode)
                self.update_selected_text()
                self.card_base.center_x = -self.card_center[0]*.4
                ret_to_center.bind(on_complete=toggle_is_playing)
                ret_to_center.start(self.card_base)
            z.bind(on_complete=begin_entrance_z)
            z.start(self.card_base)
        else: #left mode
            def begin_entrance_y(*args):
                self.deck.get_selected().reset()
                self.deck.next(self.deck.mode)
                self.update_selected_text()
                self.card_base.center_x = self.card_center[0]*2.5
                ret_to_center.bind(on_complete=toggle_is_playing)
                ret_to_center.start(self.card_base)
            y.bind(on_complete=begin_entrance_y)
            y.start(self.card_base)
            
    def on_touch_up(self, touch):
        '''
        Goals:
            -If the card is touch-released very close (<5px) to the original position, it should play a flip animation.
            -When the card is released a bit further, it should transition back to the original position.
            -If the card is released at a point where half of it's face is offscreen, the card should
                transition off screen and another card should transition on screen.
        All of this should not be able to happen again if any animation is already playing.
        '''
        if self.card_base.center[0] < self.card_center[0]+5 and self.card_base.center[0] > self.card_center[0]-5:
            #Do flip animation
            if not self.cardflip_animations['is_playing'] and self.cardflip_animations['down_success']:
                self.cardflip_animations['is_playing'] = True
                self.flip_animation()
        elif self.card_base.center[0] > (self.card_center[0]*1.65):
            #Do offscreen/onscreen transition rightwards
            if not self.offscreen_animations['is_playing']:
                self.offscreen_animations['is_playing'] = True
                self.offscreen_animation(True)
        elif self.card_base.center[0] < (self.card_center[0]*.35):
            #Do offscreen/onscreen transition leftwards
            if self.deck.mode != None:
                self.card_snapback_animation.start(self.card_base)
            elif not self.offscreen_animations['is_playing']:
                self.offscreen_animations['is_playing'] = True
                self.offscreen_animation(False)
        else:
            #Do transition-to-origin animation
            self.card_snapback_animation.start(self.card_base)
        
        
        #Swipe Emulation - See DeckWidget.on_touch_move()
        if self.touch_move_counter < 7 and self.touch_move_counter > 1:
            x_difference = self.touch_move_current[0] - self.touch_move_init[0]
            y_difference = self.touch_move_current[1] - self.touch_move_init[1]
            if x_difference > 5 and x_difference > y_difference:
                if not self.offscreen_animations['is_playing'] and not self.cardflip_animations['is_playing']:
                    self.offscreen_animations['is_playing'] = True
                    self.offscreen_animation(True)
            elif x_difference < -5 and x_difference < y_difference:
                if not self.offscreen_animations['is_playing'] and not self.cardflip_animations['is_playing']:
                    self.offscreen_animations['is_playing'] = True
                    self.offscreen_animation(False)
        self.touch_move_counter = 0
        
        
    def on_touch_move(self, touch):
        """
            At the last minute, I noticed how my launcher on my android phone behaves when you swap
            the screens. Even if your finger doesn't cover a significant distance. If you swipe quickly
            with a clear direction yet very short distance, the screen will change.
            
            It's only when you move your finger slowly with a short distances will the screen bounce back to 
            the original position. I wanted to try emulating this to an extent; swiping fast should play
            the offscreen animations while swiping slow would cause the snapback animation effect.
            
            Also, the swipe must be bigger in the x-direction than it is in the y-direction.
        """
        if self.touch_move_counter == 0:
            self.touch_move_init = touch.pos
        else:
            self.touch_move_current = touch.pos
        self.touch_move_counter += 1
        
    def on_touch_down(self, touch):
        """
            Dictates what happens when the DeckWidget is clicked/touched but not released yet. 
            Scatter.on_touch_down() handles sliding (card_base is a Scatter). Also, I only want
            this to work if no animations are playing. 
        """
        if self.offscreen_animations['is_playing'] == False and self.cardflip_animations['is_playing'] == False:
            self.card_base.on_touch_down(touch)
            self.cardflip_animations['down_success'] = True
        else:
            self.cardflip_animations['down_success'] = False
        
        if not self.cardflip_animations['is_playing']:
            self.remove_widget(self.widgets['card_text'])
            self.widgets['card_text'] = Label(center=self.card_base.center, size=(20,20), font_size=15, text=self.text_content, color=[0,0,0,1])
            self.add_widget(self.widgets['card_text'])
            self.widgets['card_text'].center = self.card_base.center

        


class FlashcardApp(App):
    def build(self):
        return DeckWidget()

if __name__== '__main__':
   FlashcardApp().run()