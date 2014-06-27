###             CARD CLASS IMPLEMENTATION             ###
###                    Notes:                         ###
#        A card has two faces; one side
#        is a question, the other side
#        is the answer.
#

import re

from random import shuffle

class Card:
    prefix = {"P#", "A#", "Q#"}
    def __init__(self, question, answer, priority=1):
        """questions string must begin with 'Q#'
           text-answer string must begin with 'A#'
           picture-answer string must begin with 'P#'"""
        self._q = question
        self._a = answer
        self._face = self._q
        self._priority = priority
        assert self._a[:2] in Card.prefix
        
    def get_answer(self):
        return self._a
    
    def get_question(self):
        return self._q
    
    def get_priority(self):
        return self._priority
    
    def set_priority(self, priority):
        self._priority = priority
    
    def flip(self):
        self._face = self._q if self._face[:2] != "Q#" else self._a
    
    def reset(self):
        self._face = self._q
        
    def __str__(self):
        return self._face
    
    def __repr__(self):
        return "Card(" + self._q + ", " + self._a + ")"
        
###     DECK CLASS IMPLEMENTATION     ###
###            Notes:                 ###
#    A deck is a list of cards.
#    The deck can be traversed linearly
#    or it can be shuffled.
#

class Deck:
    def __init__(self, cards=[], selected=None):
        self._cards = cards
        self.cards = cards
        
        self.s_index = selected if selected != None else 0
        self.selected = self.cards[self.s_index] if self._cards != [] else None

        self.h_index = 0
        self.history = dict()
    
    def get_selected(self):
        return self.selected
    
    def __add__(self,right):
        if type(right) == Card:
            self.history[self.h_index] = self.__repr__()
            self.cards += [right]
            self.h_index += 1
            if(self.cards != []):
                self.selected = self.cards[self.s_index]
            return self
        elif type(right) == Deck:
            self.history[self.h_index] = self.__repr__()
            self.cards += right.cards
            self.h_index += 1
            if(self.cards != []):
                self.selected = self.cards[self.s_index]
            return self
        else:
            raise TypeError("Deck.__add__: Can only add Deck + Card or Deck + Deck")
    
    def __iter__(self):
        def deck_gen():
            p = self.cards
            for x in p:
                yield (x.get_question(),x.get_answer())
        return deck_gen()
    
    def select(self, index):
        self.s_index = index
        self.selected = self.cards[self.s_index]
    
        
    
    def next(self, mode=None):
        """
        modes:
        None - By default, goes through the cards in order.
        p - priority; Cards with correct answers will appear with less priority.
        r - random; Randomized.
        """
        if mode==None:
            if self.s_index < len(self.cards)-1:
                self.s_index += 1
            else:
                self.s_index = 0
            self.selected = self.cards[self.s_index]
    
    def remove(self, target=None):
        try:
            if target == None:
                self.history[self.h_index] = self.__repr__()
                self.cards.remove(self.selected)
                self.h_index += 1
            else:
                self.history[self.h_index] = self.__repr__()
                self.cards.remove(target)
                self.h_index += 1
            if len(self.cards) > 0:
                self.next()
            return True
        except ValueError:
            return False
        
    def __repr__(self):
        return "Deck(" + str(self.cards) + ","  + str(self.s_index) + ")"
    
    def add_from_txt(self, filename):
        """
        Scans text file for proper format; will add strings to instance deck. Returns True on success, False otherwise.
        """
        contents = None
        try:
            with open(filename, 'r') as f:
                contents = re.findall(r'Q#(?:[\S\s](?!A#))*[\S\s])((?:A#|P#)(?:[\S\s](?!Q#))*[\S\s])',f.read())
            if contents != None:
                for x in contents:
                    self += Card(x[0].rstrip('\n'),x[1].rstrip('\n'))
            return True
        except:
            print("Error processing file")
            return False
    
    def undo(self):
        if self.h_index > 0:
            self.h_index -= 1
            d = eval(self.history[self.h_index])
            self.cards = d.cards
            self.s_index = d.s_index
            self.selected = self.cards[self.s_index]
            return True
        else:
            return False
        
    def redo(self):
        if self.h_index < len(self.history):
            self.h_index += 1
            d = eval(self.history[self.h_index])
            self.s_index = d.s_index
            self.selected = self.cards[self.s_index]
            return True
        else:
            return False
        
    
if __name__ == '__main__':
    print("-----Testing Card class:")
    print("---Testing Card.__init__() ....")
    c = Card("Q#What is the capital of California?", "A#Sacramento")
    print("---Testing Card.__repr__() ...")
    print("-", c.__repr__())
    print("---Testing Card.__str__() ...")
    print("-", c)
    print("---Testing __str__ after Card.flip() ...")
    c.flip()
    print("-", c)
    print("---Testing __str__ after another Card.flip() ...")
    c.flip()
    print("-", c)
    print("---Testing __str__ after another Card.flip() ...")
    c.flip()
    print("-", c)
    print("---Testing Card.reset() ...")
    c.reset()
    print("-", c)
    print("---Testing Card.reset after Card.flip() ...")
    c.flip()
    c.reset()
    print("-", c)
    
    print("\n-----Testing Deck class:")
    print("---Testing Deck.__init__() with no parameters ....")
    d = Deck()
    print(d)
    cards = [Card("Q#What is the capital of California?", "A#Sacramento"),
             Card("Q#What is 2 + 2?", "A#4"),
             Card("Q#What is the opposite of hate?", "A#Love")]
    print("---Testing Deck.__init__() with list of Cards ....")
    d = Deck(cards)
    print(d)
    print("---Testing Deck.remove() on previous deck ....")
    d.remove()
    print(d)
    print("---Testing Deck.remove() on previous deck ....")
    d.remove()
    print(d)
    print("---Testing Deck.remove() on previous deck ....")
    d.remove()
    print(d)