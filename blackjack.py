import csv
import random

# create empty dictionary to read into
card_deck = {}

# open card info file and turn it into usable dictionary
with open('card_information.csv') as card_info_file:
    reader = csv.reader(card_info_file)
    next(reader) #skip header
    for row in reader:
        card, value = row #card = row[0], value = row[1]
        card_deck[card] = int(value)  
#print(card_deck)

# create a list of 6 card decks & shuffle
full_blackjack_stack = []
for card in card_deck.keys():
    for i in range(6):
        full_blackjack_stack.append(card)
random.shuffle(full_blackjack_stack)

#Blackjack class & actions
class Blackjack():
    def __init__(self):
        self.card_stack = full_blackjack_stack
        self.discard_stack = []
    
    def game_setup(self):
        pass
    
    def betting(self):
        pass
    
    def dealing(self):
        pass
    
    def hit(self):
        pass
        
    def stand(self):
        pass
    
    def dealers_turn(self):
        pass
    
    def split_pair(self):
        pass
    
    def double_down(self):
        pass
    
class Player():
    
    def __init__(self):
        pass

# Startup notification & while loop setup
print("""--------------------------------
Are you ready to play Blackjack?
--------------------------------""")
play_game = True

# While loop will repeat until user inputs 4 in menu
# ui_* is short for user_input_*
while play_game:
    #User choice
    print("""-----------------------
What do you want to do?""")
    ui_menu = input("""1. Play Blackjack
2. View Rules
3. View Highscores
4. Quit Game
-----------------------
""")
    
    # catch non int inputs
    try:
        ui_menu_int = int(ui_menu)
    except:
        print("Invalid input!\n")
        continue
    
    #If/else block after user input!
    
    if ui_menu_int == 1: #Play Blackjack
        #create while loop to return to if invalid input
        ui_game_input = True
        while ui_game_input:
            # ask game type input
            print("""------------------------------
lets play a game of blackjack!""")
            ui_game_type = input("""--------------------------------------
What type of game do you want to play?
1. Regular Blackjack
2. Race against the House
3. Blackjack Duel (Multiplayer only)\n
4. Return To Main Menu
--------------------------------------
""")
            # Check for int input
            try:
                ui_game_type_int = int(ui_game_type)
            except:
                print("Invalid input!\n")
                continue
            if ui_game_type_int == 4:
                break
            
            # ask amount of players input
            ui_amount_of_players = input("""---------------------------
How many players are there?
(enter number of players)
---------------------------
""")
            # Check for int input
            try:
                ui_amount_of_players_int = int(ui_amount_of_players)
            except:
                print("Invalid input!\n")
                continue
            if ui_amount_of_players_int == 69:
                print("nice")
                print("nice")
                print("nice")
            
            #start main game loop code thingy
            
        
    elif ui_menu_int == 2: # View Rules
        print("these are the rules")
        
        
    elif ui_menu_int == 3: # View Highscores
        print("These are the highscores")
        
        
    elif ui_menu_int == 4: # Quit Game
        print("Thanks for playing!")
        play_game = False #exit while loop
        
    else: # Invalid input returns to start main menu while loop
        print("Invalid input!\n")

