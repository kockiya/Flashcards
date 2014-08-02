'''
Created on Jun 24, 2014

@author: Xuxion
'''

from deck import *

main_menu =  """
    -DECK SETTINGS-
        (s) Start studying!    (a) Add a card    (e) Edit selected card    (r) Remove selected card    (l) List cards in deck
        (m) Change deck mode   (g) Show greeting (y) Redo previous undo    (z) Undo last deck change   (f) Add questions from file
        
"""

mode_menu =  """-MODE OPTIONS-
        n) Go through cards normally
        o) Go through cards randomly
        x) Go through correct cards less frequently
"""

greeting = """
This is a simple flash card program with the following features:
    -Start
        -Start going through cards
    -Add a card
        -Add a card to the deck by entering the card's question
        and the corresponding answer when prompted
    -Edit selected card
        -Manually enter a new question/answer to replace the selected card
    -Remove selected the card
        -Removes the selected card from the deck
    -List cards in deck
        -Prints out a list of cards currently in the deck.
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
def show_selected(d):
    if len(d) != 0:
        print("\n----- Currently Selected Card -----\nQuestion: "+d.selected.get_question()[2:])
        print("Answer:   "+d.selected.get_answer()[2:]+"\n-----                         -----")
    else:
        print("----- Currently Selected Card -----\n(Nothing Selected Because Deck is Empty)\n-----                         -----")
    
    
    
def main():
    mode = None
    filename = None
    main_select = None
    d = Deck([])
    print(greeting)
    while(True):
        while True:
            show_selected(d)
            print(main_menu)
            main_select = str(input("Enter a command:"))
            if main_select in {'s','a','r','f','l','m','z','y','g', 'e', 'l'}:
                break
            print("Invalid command!\n")
        if main_select == 's':
            while True:
                if len(d) == 0:
                    print("There aren't any cards in the deck!")
                    break
                print("\n"+str(d.get_selected()))
                command = str(input())
                if command == '':
                    d.selected.flip()
                    print(d.get_selected())
                    command = str(input())
                    if command != '':
                        break
                else:
                    break
                d.selected.reset()
                d.next()
        elif main_select == 'a':
            question = "Q#"+str(input("Enter the question for the new card:"))
            answer = str(input("Enter the answer for the new card:"))
            if answer[:2] == "P#":
                answer = "P#"+answer
            else:
                answer = "A#"+answer
            d += Card(question, answer)
            print("\nAdded new card with question '{q}' and answer '{a}'".format(q=question[2:], a=answer[2:]))
        elif main_select == 'e':
            show_selected(d)
            if len(d) > 0:
                saved_question = d.selected.get_question()
                saved_answer = d.selected.get_answer()
                question = "Q#"+str(input("Enter the new question (Leave blank to keep):"))
                if question == 'Q#':
                    question = saved_question
                answer = str(input("Enter the answer for the new card (Leave blank to keep):"))
                if answer == '':
                    answer = saved_answer
                elif answer[:2] == "P#":
                    answer = "P#"+answer
                else:
                    answer = "A#"+answer
                d.set_selected(question, answer)
            else:
                print("Error - Cannot edit cards when the deck is empty")
        elif main_select == 'r':
            print("The following card is currently selected and will be removed:")
            show_selected(d)
            remove_confirm = str(input(("Enter 'y' to confirm removal:")))
            if remove_confirm.lower() == 'y':
                if d.remove():
                    print("The previously selected card was removed!")
                else:
                    print("Error - Could not remove selected card! Is the deck empty?")
            else:
                print("Because 'y' was not entered, the card was not removed")
        elif main_select == 'l':
            print("\nCurrent deck contents:")
            if len(d) == 0:
                print ("-- Empty --")
            for x in d:
                    print("---\nQuestion: '{q}'\nAnswer: '{a}'\n---".format(q=x[0], a=x[1]))
        elif main_select == 'f':
            filename = str(input("Enter the filename that contains the questions:"))
            file_result =  d.add_from_txt(filename)
            if file_result == False:
                print("Error - Could not processes the file! Make sure the file exists and follows the correct format")
            else:
                print("\nAdded the following cards to the deck:\n---")
                for x in file_result:
                    print("Question: '{q}'\nAnswer: '{a}'\n---".format(q=x[0], a=x[1]))
            
        elif main_select == 'm':
            print(mode_menu)
            new_mode = str(input("Enter the new mode"))
            if new_mode in {'n','o','x'}:
                mode = new_mode
            else:
                print("Error - Specified mode not recognized!")
        elif main_select == 'z':
            if d.undo():
                print("The last change to the deck has been undone")
            else:
                print("Error - No more undo's available!")
        elif main_select == 'y':
            if d.redo():
                print("The last undo has been undone!")
            else:
                print("Error - No more redo's available!")
        elif main_select == 'g':
            print(greeting)

if __name__ == '__main__':
    main()