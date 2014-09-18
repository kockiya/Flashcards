'''
Created on Aug 7, 2014

@author: Xuxion


*Requires Kivy to run.

You can get it from the Kivy site and run this .py by dragging it to kivy.bat
after the installation is extracted.

Getting Kivy to work with eclipse, however, really exhausted my Googling abilities...
'''

from deck import *
from kivy.metrics import *
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation, AnimationTransition
from kivy.graphics import *
from kivy.uix.filechooser import *
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, TransitionBase
from kivy.properties import *
from kivy.uix.settings import SettingsWithNoMenu, SettingItem, SettingString
from deckwidget import DeckWidget
from fadingtextwidget import FadingTextWidget
from kivy.config import ConfigParser
from kivy.base import EventLoop
from kivy.event import EventDispatcher
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import os





class FlashcardAppManager(ScreenManager):
    s_manager = None
    deck_screen = None
    file_screen = None
    menu_screen = None
    deck_widget = None
    def __init__(self):
        ScreenManager.__init__(self)
        self.menu_screen = FlashcardAppManager.MenuScreen()
        self.add_widget(self.menu_screen)
        self.file_screen = FlashcardAppManager.FileScreen()
        self.add_widget(self.file_screen)
        self.deck_screen = FlashcardAppManager.DeckScreen()
        self.add_widget(self.deck_screen)
        self.add_card_screen = FlashcardAppManager.AddCardMenuScreen()
        self.add_widget(self.add_card_screen)
        self.edit_card_screen = FlashcardAppManager.EditCardMenuScreen()
        self.add_widget(self.edit_card_screen)
        
        FlashcardAppManager.s_manager = self
        FlashcardAppManager.deck_screen = self.deck_screen
        FlashcardAppManager.file_screen = self.file_screen
        FlashcardAppManager.menu_screen = self.menu_screen


    class FileScreen(Screen):
        def __init__(self):
            Screen.__init__(self)
            self.name = 'file'
            
            self.file_chooser = FileChooserListView(path=os.getcwd())
            self.file_chooser.bind(on_submit=self.add_cards)
            self.add_widget(self.file_chooser)
    
        def add_cards(self, *args):
            cards = FlashcardAppManager.deck_widget.deck.add_from_txt(self.file_chooser.selection[0])
            FlashcardAppManager.s_manager.current = "menu"
            if cards:
                FlashcardApp.fading_message.push_text("Successfully added "+str(len(cards))+" cards to the deck")
            else:
                FlashcardApp.fading_message.push_text("Failed to add cards from file")
            
                
    
            
    class SettingNewScreen(SettingItem):
        screen = StringProperty("")
        def on_release(self, *args):
            FlashcardAppManager.s_manager.current = FlashcardAppManager.SettingNewScreen.screen.get(self)
    
    class EditCardMenuScreen(Screen):
        question = ""
        answer = ""
        nquestion = ""
        nanswer = ""
        EditCardMenuConfig = None
        
        def update_qa(self, *args):
                FlashcardAppManager.EditCardMenuScreen.nquestion = self.config.get('edit', 'nquestion')
                FlashcardAppManager.EditCardMenuScreen.nanswer = self.config.get("edit", "nanswer")
                
        def __init__(self):
            Screen.__init__(self)
            
            self.name = "edit"
            
            self.config = ConfigParser()
            self.config.add_section("edit")
            self.config.set("edit", "question", "Question")
            self.config.set("edit", "answer", "Answer")
            self.config.set("edit", "nquestion", "Question")
            self.config.set("edit", "nanswer", "Answer")
            self.config.set("edit", "edit", "action")
            
            FlashcardAppManager.EditCardMenuScreen.question = self.config.get('edit', 'question')
            FlashcardAppManager.EditCardMenuScreen.answer = self.config.get('edit', 'answer')
            FlashcardAppManager.EditCardMenuScreen.nquestion = self.config.get('edit', 'nquestion')
            FlashcardAppManager.EditCardMenuScreen.nanswer = self.config.get('edit', 'nanswer')
            
            
                
            self.config.add_callback(self.update_qa, section="edit", key="nquestion")
            self.config.add_callback(self.update_qa, section="edit", key="nanswer")
            
            self.menu = SettingsWithNoMenu()
            
            
            self.menu.register_type("action", FlashcardAppManager.SettingDoAction)
            self.menu.add_json_panel("Add a card", self.config, os.path.join(os.path.dirname(__file__), 'edit_menu.json'))
            
            FlashcardAppManager.EditCardMenuScreen.EditCardMenuConfig = self.config
            
            self.add_widget(self.menu)
            
            def on_pre_enter(self, *args):
                FlashcardAppManager.EditCardMenuScreen.question = FlashcardAppManager.deck_widget.deck.get_selected().get_question()
                FlashcardAppManager.EditCardMenuScreen.answer = FlashcardAppManager.deck_widget.deck.get_selected().get_answer()
                self.config.set("edit", "question", FlashcardAppManager.EditCardMenuScreen.question)
                self.config.set("edit", "answer", FlashcardAppManager.EditCardMenuScreen.answer)
            
        
                
    class AddCardMenuScreen(Screen):
        question = ""
        answer = ""
        def __init__(self):
            Screen.__init__(self)
            self.name = "add"
            
            self.config = ConfigParser()
            self.config.add_section("add")
            self.config.set("add", "question", "Question")
            self.config.set("add", "answer", "Answer")
            self.config.set("add", "make", "action")
            self.config.add_callback(self.update_qa, section="add", key="question")
            self.config.add_callback(self.update_qa, section="add", key="answer")
            self.menu = SettingsWithNoMenu()
            
            
            self.menu.register_type("action", FlashcardAppManager.SettingDoAction)
            self.menu.add_json_panel("Add a card", self.config, os.path.join(os.path.dirname(__file__), 'add_menu.json'))
            
            self.add_widget(self.menu)
            
            
        def update_qa(self, *args):
            FlashcardAppManager.AddCardMenuScreen.question = self.config.get('add', 'question')
            FlashcardAppManager.AddCardMenuScreen.answer = self.config.get('add', 'answer')
            
    
    
    class SettingDoAction(SettingItem):
        action = StringProperty("")
        def on_action(self, instance, value):
            self.action_value = value
            
        def on_release(self):
            print(self.action_value)
            if self.action_value == 'add':
                FlashcardAppManager.deck_widget.deck += Card('Q#'+FlashcardAppManager.AddCardMenuScreen.question, 'A#'+FlashcardAppManager.AddCardMenuScreen.answer)
                FlashcardApp.fading_message.push_text("Successfully added the card to the deck")
            elif self.action_value == 'remove':
                if len(FlashcardAppManager.deck_widget.deck) > 0:
                    FlashcardAppManager.deck_widget.deck.remove()
                    FlashcardApp.fading_message.push_text("Successfully removed selected card")
                else:
                    FlashcardApp.fading_message.push_text("Nothing to remove because deck is empty")
            elif self.action_value == 'edit':
                if len(FlashcardAppManager.deck_widget.deck) > 0:
                    FlashcardAppManager.deck_widget.deck.edit_selected('Q#'+FlashcardAppManager.EditCardMenuScreen.nquestion, 'A#'+FlashcardAppManager.EditCardMenuScreen.nanswer)
                    FlashcardAppManager.EditCardMenuScreen.question = FlashcardAppManager.deck_widget.deck.get_selected().get_question()
                    FlashcardAppManager.EditCardMenuScreen.answer = FlashcardAppManager.deck_widget.deck.get_selected().get_answer()
                    FlashcardAppManager.EditCardMenuScreen.EditCardMenuConfig.set("edit", "question", FlashcardAppManager.EditCardMenuScreen.question)
                    FlashcardAppManager.EditCardMenuScreen.EditCardMenuConfig.set("edit", "answer", FlashcardAppManager.EditCardMenuScreen.answer)
                    FlashcardApp.fading_message.push_text("Successfully edited selected card")
                else:
                    FlashcardApp.fading_message.push_text("Nothing to edit because deck is empty")
            elif self.action_value == 'undo':
                if FlashcardAppManager.deck_widget.deck.can_undo():
                    FlashcardAppManager.deck_widget.deck.undo()
                    FlashcardApp.fading_message.push_text("Last change undone - {a} cards in deck".format(a=str(len(FlashcardAppManager.deck_widget.deck))))
                else:
                    FlashcardApp.fading_message.push_text("No undo's are available")
            elif self.action_value == 'redo':
                if FlashcardAppManager.deck_widget.deck.can_redo():
                    FlashcardAppManager.deck_widget.deck.redo()
                    FlashcardApp.fading_message.push_text("Last change redone - {a} cards in deck".format(a=str(len(FlashcardAppManager.deck_widget.deck))))
                else:
                    FlashcardApp.fading_message.push_text("No redo's are available")
                
    class MenuScreen(Screen):
        def __init__(self):
            Screen.__init__(self)
            self.name = 'menu'
            self.config = ConfigParser()
            self.config.add_section("deck")
            self.config.add_section("card")
            self.config.adddefaultsection("menu")
            self.config.set("deck", "start_studying", 1)
            self.config.set("deck", "change_deck_mode", "Normal")
            self.config.set("deck", "show_list", True)
            self.config.set("deck", "undo", True)
            self.config.set("deck", "redo", True)
            self.config.set("card", "add", "")
            self.config.set("card", "edit", True)
            self.config.set("card", "remove", True)
            
            self.config.add_callback(self.check_deck_locks, "deck", "redo")
            self.config.add_callback(self.check_deck_locks, "deck", "undo")
            
            self.config.add_callback(self.check_card_locks, "card", "edit")
            self.config.add_callback(self.check_card_locks, "card", "add")
            
            
            self.menu = SettingsWithNoMenu()
            self.menu.register_type("screen", FlashcardAppManager.SettingNewScreen)
            self.menu.register_type("action", FlashcardAppManager.SettingDoAction)
            self.menu.add_json_panel("Flashcards", self.config, os.path.join(os.path.dirname(__file__), 'menu.json'))
            
            self.add_widget(self.menu)
            
    
        def check_deck_locks(self, section, key, value):
            print(self.config.get(section, key))
        
        def check_card_locks(self, section, key, value):
            print()
    
    
    
    class DeckScreen(Screen):
        def __init__(self):
            Screen.__init__(self)
            self.name = 'deck'
            self.box_layout = BoxLayout(size=Window.size)
            self.add_widget(self.box_layout)
            
            FlashcardAppManager.deck_widget = DeckWidget()
            self.box_layout.add_widget(FlashcardAppManager.deck_widget)
            
        def on_pre_enter(self):
            FlashcardAppManager.deck_widget.recalc_pos()
            
        
class FlashcardApp(App):
    
    fading_message = FadingTextWidget(text="Hello", pos_hint={'x':0,'y':-.4}, font_size=sp(14))
    def build(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        fl = FloatLayout()
        fl.add_widget(FlashcardAppManager())
        fl.add_widget(FlashcardApp.fading_message)
        return fl

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            if FlashcardAppManager.s_manager.current != 'menu':
                FlashcardAppManager.s_manager.current = 'menu'
            else:
                App.get_running_app().stop()
        return True 
   

if __name__== '__main__':
   FlashcardApp().run()