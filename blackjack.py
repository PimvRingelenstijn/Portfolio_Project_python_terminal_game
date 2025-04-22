import csv
import random
import time
import os

# open card info file and turn it into usable dictionary
card_deck = {}
with open("card_information.csv") as card_info_file:
    reader = csv.reader(card_info_file)
    next(reader) #skip header
    for row in reader:
        card, value = row #card = row[0], value = row[1]
        card_deck[card] = int(value)  

## open player info file and turn it into usable dictionary
#players_info = {}
#with open("player_highscores.csv") as players_info_file:
#    reader = csv.reader(players_info_file)
#    next(reader)
#    for row in reader:
#        player, scores = row #player = row[0], scores = row[1]
#        players_info[player] = scores
players_highscores = {}

# create a list of 6 card decks & shuffle
full_blackjack_stack = []
for card in card_deck.keys():
    for i in range(6):
        full_blackjack_stack.append(card)
random.shuffle(full_blackjack_stack)

# method for clean terminal messages
def terminal_message(message):
    # Determine max scentence length
    len_message = 0
    split_message = message.split("\n")
    for scentence in split_message:
        if len_message < len(scentence):
            len_message = len(scentence)
    blank_line = "-" * len_message + "\n"
    return "\n" + blank_line + message + "\n" + blank_line

#Blackjack class & actions
class Blackjack():
    def __init__(self, player_list, game_type_int):
        self.card_stack = full_blackjack_stack
        self.discard_stack = []
        self.rounds_counter = 0
        self.minimum_card_stack_size = random.randint(60, 80) # minimum size of card stack before reshuffle
        self.card_scores = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11,}
        if game_type_int == 1:
            self.game_type = "regular"
        elif game_type_int == 2:
            self.game_type = "race"
        else: self.game_type = "duel"
        # create dict with balance, empty card list and card score for use during game
        self.active_players = player_list
        self.player_info = {"Dealer":{"Cards": [], "Card Score": 0}}
        for i in player_list:
            self.player_info[i] = {"Balance": 100, "Cards": [], "Card Score":0}
        Blackjack.clean_terminal_message_input(self)
    
    def clean_terminal_message_input(self):
        # line 1 is player name, 2/ 4/ 6 are blank lines, 3/5 are card info
        self.game_state_message = ["", "", "", "", "", "",]
    
    def player_cards_output(self):
        pass
    
    def game_state_terminal_message_output(self):
        # clears terminal output
        os.system('cls' if os.name == 'nt' else 'clear')
        for player, info in self.player_info.items():
            if player == "Dealer":
                if info["Cards Score"] == "BLACKJACK!":
                    self.dealer_blackjack = True
                
                           
    
    def betting(self):
        # clears terminal output
        os.system('cls' if os.name == 'nt' else 'clear')
        # dict for keeping track of bets
        self.active_bets = {}
        print(terminal_message("It's time to place your bets!"))
        time.sleep(0.5)
        # Using while loop to make sure correct input can be found
        player_index = 0
        while player_index < len(self.active_players):
            active_player = self.active_players[player_index]
            ui_betting_amount = input(terminal_message("""Player {name}, you currently have ${money}.
How much do you want to bet?""".format(name = active_player, money = self.player_info[active_player]["Balance"])))
            # Catch non int inputs          
            try:
                ui_betting_amount_int = int(ui_betting_amount)
            except: 
                print("\nInvalid input!\n")
                continue
            # check betting size
            if ui_betting_amount_int < 1:
                print("\nInvalid input!\n")
                continue
            elif ui_betting_amount_int > self.player_info[active_player]["Balance"] or ui_betting_amount_int > 500: 
                print("\nToo large bet!\n")
                continue
            # resolve betting amount & player index
            self.player_info[active_player]["Balance"] -= ui_betting_amount_int
            self.active_bets[active_player] = ui_betting_amount_int
            player_index += 1
    
    def calculate_players_cards_scores(self):
        for player, info in self.player_info.items():
            for card in info["Cards"]:
                card_info = card.split(" ")
                info["Card Score"] += self.card_scores[card_info[0]]
            if info["Card Score"] == 21:
                info["Card Score"] = "BLACKJACK!"
    
    
    def game_setup(self):
        for i in range(2):
            for player in self.player_info:
                next_card = self.card_stack.pop()
                self.discard_stack.append(next_card)
                self.player_info[player]["Cards"].append(next_card)
        Blackjack.calculate_players_cards_scores(self)
 
    def player_blackjack_payout(self):
        pass
    
    def game_result(self):
        pass
    
    def main_gameplay_loop(self):
        self.rounds_counter += 1
        self.dealer_blackjack = False
        Blackjack.betting(self)
        Blackjack.game_setup(self)
        if self.dealer_blackjack:
            pass
    
class Player():
    def __init__(self, name):
        basic_scores = {"Regular": 100, "Race": 100, "Duel": 100}
        players_highscores[name] = basic_scores
    
    def welcome_message(self, name):
        print("Welcome back {player}!".format(player = name))
        
    def highscore(self, name):
        pass
        

# Startup notification 
print(terminal_message("Welcome to the game of Blackjack?"))
time.sleep(1.5)


# While loop will repeat until user inputs 4 in menu
# ui_* is short for user_input_*
while True:
    # clears terminal output
    os.system('cls' if os.name == 'nt' else 'clear')
    # User choice
    return_to_main_menu = False
    ui_menu = input(terminal_message("What do you want to do?\n\n1. Play Blackjack\n2. View Rules\n3. View Highscores\n4. Quit Game"))
    
    # catch non int inputs
    try:
        ui_menu_int = int(ui_menu)
    except:
        print("\nInvalid input!\n")
        continue
    time.sleep(0.5)

    # If/else block after user input!
    if ui_menu_int == 1: #Play Blackjack
        #create while loop to return to if invalid input
        ui_game_type_int = 0
        active_players = []
        game_setup_menu = True
        
        #while input for game type selection and player count
        while game_setup_menu:
            # clears terminal output
            os.system('cls' if os.name == 'nt' else 'clear')
            # ask game type input
            ui_game_type = input(terminal_message("""Lets play a game of blackjack!\n\nWhat type of game do you want to play?\n1. Regular Blackjack
2. Race against the House\n3. Blackjack Duel (Multiplayer only)\n4. Return To Main Menu"""))
            # Check for int input
            try:
                ui_game_type_int = int(ui_game_type)
            except:
                print("\nInvalid input!\n")
                continue
            time.sleep(0.5)
            if ui_game_type_int == 4:
                return_to_main_menu = True
                break
            
            # ask amount of players input
            ui_amount_of_players = input(terminal_message("How many players are there?\n(enter number of players)"))
            # Check for int input
            try:
                ui_amount_of_players_int = int(ui_amount_of_players)
            except:
                print("\nInvalid input!\n")
                continue
            time.sleep(0.5)
            
            # lel, had to be done
            if ui_amount_of_players_int == 69:
                for i in range(10): 
                    print("nice")
                    time.sleep(0.1)

            
            # Add 1 single player
            if ui_amount_of_players_int == 1:
                player_name = input(terminal_message("Welcome player! What is your name?"))
                if player_name in players_highscores: 
                    Player.welcome_message(player_name)
                else: Player(player_name)
                active_players.append(player_name)            
            # add multiple players
            elif ui_amount_of_players_int > 1:
                for player_num in range(1, ui_amount_of_players_int + 1):
                    player_name = input(terminal_message("Welcome player {num}! What is your name?".format(num = player_num)))
                    if player_name in players_highscores: 
                        Player.welcome_message(player_name)
                    else: Player(player_name)
                    active_players.append(player_name)
                    time.sleep(0.5)
            # check for negative players
            else:
                print("\nInvalid Input!\n")
                continue
            
            # stops game setup menu while loop
            game_setup_menu = False

        # return to first while loop after game type input == 4
        if return_to_main_menu:
            continue
        
        # this will be the real gameplay loop!
        main_gameplay_loop = True
        print(terminal_message("Lets get started!"))
        time.sleep(1)
        main_game = Blackjack(active_players, ui_game_type_int)
        while main_gameplay_loop:
            main_game.main_gameplay_loop()
            
            
            


        
    elif ui_menu_int == 2: # View Rules
        print("these are the rules")
        
        
    elif ui_menu_int == 3: # View Highscores
        print("These are the highscores")
        
        
    elif ui_menu_int == 4: # Quit Game
        print("Thanks for playing!")
        break#exit while loop
        
    else: # \nInvalid input returns to start main menu while loop
        print("\nInvalid input!\n")


