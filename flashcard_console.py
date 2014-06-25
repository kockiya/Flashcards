'''
Created on Jun 24, 2014

@author: Xuxion
'''



main_menu =  
"""
    -DECK SETTINGS-
        s) Start studying!
        a) Add a card
        r) Remove selected card
        f) Add questions from file
        m) Change deck mode
        z) Undo last deck change
        y) Redo previous deck undo
        g) Show greeting
"""

mode_menu =  
"""-MODE OPTIONS-
        n) Go through cards normally
        o) Go through cards randomly
        x) Go through correct cards less frequently
"""

greeting = 
"""
This is a simple flash card program with the following features:
    -Start
        -Start going through cards
    -Add a card
        -Add a card to the deck by entering the card's question
        and the corresponding answer when prompted
    -Remove selected the card
        -Removes the selected card from the deck
    -Add questions from file
        -Generate cards from a text file. Questions are the characters that follow "Q#"
        and its corresponding answer are the characters that follow "A#". For a picture answer,
        instead of using A#, you can use P#
            Example:
                Q#What is the capital of California?A#SacrementoQ#What color is the sky?
                A#Blue Q#What's an example of an octagan?
                P#stopsign.jpg Q#What is my name?
                
                --Will Create cards of the form:
                Q-What is the capital of California?    | A-Sacramento
                Q-What color is the sky?                | A-Blue
                Q-What's an example of an octagan       | (stopsign.jpg appears)
    -Change deck mode
        -Go through cards normally
            -Go through cards normally in the order they are currently in the deck
        -Go through cards randomly
            -Go through cards in a random order
        -Go through correct cards less frequently
            -Cards that you get correct will appear less frequently. This gives 
            you a chance to focus on cards you get wrong.
    -Undo last deck change
        -Undo last add/remove
    -Redo previous deck undo
        -Redo previous undo
    -Show greeting
        -Show this message again
                
"""

def main():
    mode = None
    filename = None
    
    print(greeting)
    while(True):
        print(main_menu)
        