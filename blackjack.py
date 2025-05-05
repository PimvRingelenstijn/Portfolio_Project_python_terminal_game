import json
import random
import time
import os
from terminal_message import terminal_message


#Blackjack class & methods
class Blackjack():
    # class setup with all required self.bj_* v
    def __init__(self, player_list):
        # open card_info.json and create usable card stack
        with open("card_info.json", "r") as file:
            self.card_deck_info = json.load(file)
        
        # other instance variables required
        self.bj_rounds_counter = 1      # instance int that counts num of rounds
        self.bj_minimum_card_stack_size = random.randint(60, 80)        # minimum size of card stack before reshuffle
        self.bj_current_players = player_list       # instance list of current player names
        self.bj_blank_card_template = ["- % -", "-----"]        # instance list with card visuals
        self.bust_players = 0

        # setup card stack and player info dict
        Blackjack.create_card_stack(self)
        Blackjack.set_players_info(self)
        
        # print setup message
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        print(terminal_message("Let's get started!"))
        time.sleep(.5)
        for i in range(4):
            print(terminal_message("The dealer shuffels cards."))
            time.sleep(1)
        x = input(terminal_message("The cards are shuffeled and the dealer adds a spacer card somewhere around the top 70 cards.\nPress enter to continue."))
    
    # create new 312 card list
    def create_card_stack(self):
        # create card stack of 6 * 52 cards (312 = regular casino card stack size)
        self.bj_card_stack = []
        for i in range(6):
            for card in self.card_deck_info.keys():
                self.bj_card_stack.append(card)
        random.shuffle(self.bj_card_stack)
        
    # create instance dict with info for use in game logic & highscores     
    def set_players_info(self):    
        # "Dealer" does not need all dict entries
        self.bj_player_info = {"Dealer":
            {"Cards": [], # holds current cards
             "Card Score": 0, # current card score
             "Print Message": [" Dealer", "", "", "", "", "", ""], # list used in creating terminal output
             "Turn": False # logic for dealer turn
             }
            }
        
        for player in self.bj_current_players:
            # add basic dict entries for players
            self.bj_player_info[player] = {
                "Balance": 100, # starting balance
                "Cards": [], # holds current cards
                "Card Score": 0, # current card score
                "Current Bet": 0, # current bet
                "Print Message": [], # list used in creating terminal output
                "Split Pair": False, # split pair logic
                "Double Down": False, # double down logic
                "Highest Round": 0, # max round if player continues after broke
                "Current Round": 0 # current round count
                }
            
            # add name + add whitespace if len(name) = equals for esthetic sake
            # in center_player_card_info this gets removed if len(name) is longest
            if len(player) % 2 == 0:
                self.bj_player_info[player]["Print Message"] = [" " + player, "", "", "", "", "", ""]
            else:
                self.bj_player_info[player]["Print Message"] = [player, "", "", "", "", "", ""]
            
    # clear data that needs to be reset per round
    def clear_players_info(self):
        for player, info in self.bj_player_info.items():
            self.max_line_len_single_player = 0
            self.bust_players = 0
            
            #removes player entries for split pair players
            if player.endswith("_split"):
                del self.bj_player_info[player]
                continue
            
            # resets print message Removes bet / No Blackjack! lines
            if len(player) % 2 == 0:
                self.bj_player_info[player]["Print Message"] = [" " + player, "", "", "", "", "", ""]
            else:
                self.bj_player_info[player]["Print Message"] = [player, "", "", "", "", "", ""]
            if player == "Dealer":
                info.update({
                    "Cards": [],
                    "Card Score": 0,
                    "Turn": False
                })
            else:
                info.update({
                    "Cards": [],
                    "Card Score": 0,
                    "Current Bet": 0,
                    "Split Pair": False,
                    "Double Down": False
                })


    # betting logic
    def betting(self):
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        print(terminal_message("It's time to place your bets!"))
        time.sleep(0.5)
        
        # Using while loop to make sure correct player input can be found
        # player_index is updated after correct input
        player_index = 0
        while player_index < len(self.bj_current_players):
            
            player = self.bj_current_players[player_index]
            balance = self.bj_player_info[player]["Balance"]
            # ask player for amount they want to bet
            ui_betting_amount = input(terminal_message(f"Player {player}, you currently have ${balance}.\nHow much do you want to bet?", True))

            # Catch non int inputs          
            try:
                ui_betting_amount_int = int(ui_betting_amount)
            except: 
                x = input("Error: Invalid Input!")
                continue
            
            # check bet size
            if ui_betting_amount_int < 10:
                x = input(terminal_message("Error: Bet too small!\nMin $10"))
                continue
            elif ui_betting_amount_int > self.bj_player_info[player]["Balance"] or ui_betting_amount_int > 500: 
                x = input(terminal_message("Error: Bet too large.\nMax $500"))
                continue
            
            # resolve betting amount 
            self.bj_player_info[player]["Balance"] -= ui_betting_amount_int
            self.bj_player_info[player]["Current Bet"] = ui_betting_amount_int
            
            # add bet to player print message
            self.bj_player_info[player]["Print Message"].append("Bet: $" + str(ui_betting_amount_int))
            
            # increase player index
            player_index += 1

    
    # creates card part ["Print Message"] for player
    def create_player_print_message(self, player, info, double_down = False):      
        # reset cards part of ["Print Message"] for player
        info["Print Message"][1:6] = ["", "", "", "", ""]
        
        # index for adding aditional whitespaces between cards
        card_index = 1
        for card in info["Cards"]:
            # split card name to be able to access single elements consistantly
            split_card = card.split(" ")
                
            # check if current card is hidden second dealer card
            if (player == "Dealer" and card_index == 2 and info["Turn"] == False and info["Print Message"][6].strip() != "BLACKJACK!") or (card_index == 3 and double_down):
                # create blank second dealer card as long as the dealer is not at play or dealer Blackjack
                for i in range(1, 6):
                    if i == 2 or i == 4:
                        info["Print Message"][i] += self.bj_blank_card_template[0]
                    else:
                        info["Print Message"][i] += self.bj_blank_card_template[1]
                return
                
            # continue for regular cards
            else:
                for i in range(1, 6):
                    # adds the value of the card to card display
                    if i == 2:
                        # Gives 10 cards the visual T for ease of card display
                        if split_card[0] == "10":
                            info["Print Message"][2] += self.bj_blank_card_template[0].replace("%", "T")
                        else:
                            info["Print Message"][2] += self.bj_blank_card_template[0].replace("%", card[0][0])
                    # adds the house of the card to card display
                    elif i == 4:
                        info["Print Message"][4] += self.bj_blank_card_template[0].replace("%", split_card[2][0])
                    # adds blanklines
                    else:
                        info["Print Message"][i] += self.bj_blank_card_template[1]
                
            # uses card_index to add whitespaces between cards
            if card_index < len(info["Cards"]):
                for i in range(1, 6):
                    info["Print Message"][i] += " "
                card_index += 1
            
             
    # logic for calculating card scores including blackjack and busted players
    def calculate_player_cards_score(self, player, info, double_down = False, split_pair = False):
        # reset card score
        info["Card Score"] = 0
            
        # loop through current cards
        for card in info["Cards"]:
            # check for correct ace value
            if card.startswith("Ace of") and card.endswith(" 1"):
                info["Card Score"] += 1
            else: 
                # find card value and add to current ["Card Score"]
                info["Card Score"] += self.card_deck_info[card]
            
        # Check if player score > 21 and see if an Ace is present
        if info["Card Score"] > 21:
            # loop through cards
            for i, card in enumerate(info["Cards"]):
                # if after a card change score drops below 21 exit loop
                if info["Card Score"] <= 21: continue
                # find ace card, change name for future scoring, remove 10 points from score
                # the name change has no effect on the card stack, that is tracked separatly
                elif card.startswith("Ace of") and not card.endswith("1"):
                    info["Cards"][i] += " 1"
                    info["Card Score"] -= 10
            if info["Card Score"] > 21:
                info["Print Message"][6] = "Busted!"
                return
        
        # add score value to print message
        if info["Card Score"] == 21 and len(info["Cards"]) == 2 and split_pair == False:
            info["Print Message"][6] += "BLACKJACK!"
        elif player == "Dealer" and info["Turn"] == False:
            # Check for double ace:
            if info["Cards"][0].startswith("Ace of") and info["Cards"][0].endswith(" 1"):
                info["Print Message"][6] = "Score: 11"
                info["Print Message"].append("No Blackjack!")
            # if first cardvalue < 10 add regular score
            elif self.card_deck_info[info["Cards"][0]] < 10:
                info["Print Message"][6] = "Score: " + str(self.card_deck_info[info["Cards"][0]])
            # if first cardvalue > 10 but no blackjack add score & no blackjack line
            else:
                info["Print Message"][6] = "Score: " + str(self.card_deck_info[info["Cards"][0]])
                info["Print Message"].append("No Blackjack!")
        # double down score
        elif double_down:
            info["Print Message"][6] = info["Print Message"][6].strip() + " + ?"
        # regular player score        
        else:
            info["Print Message"][6] = "Score: " + str(info["Card Score"])
            
        # add whitespace for esthetic reasons
        if len(info["Print Message"][6]) == 8:
            info["Print Message"][6] += " " 


    # block to check for special actions after game setup
    def special_setup_actions(self, player, info):
        # logic for allowing doubling down
        if info["Card Score"] in range(9,12) and player != "Dealer":
            info["Double Down"] = True
        
        # logic for allowing splitting pair
        if info["Cards"][0][0] == info["Cards"][1][0] and player != "Dealer":
            info["Split Pair"] = True


    # center player message info
    def center_player_card_info(self, player, info):    
        # center player info 
        max_line_len = 0
        # determine max line length
        for i in range(len(info["Print Message"])):
            if max_line_len < len(info["Print Message"][i]):
                max_line_len = len(info["Print Message"][i])
        
        # check if name is longest and longer than card line, and name = equals
        # if so remove whitespace added for esthetic reasons in create player print message
        if max_line_len == len(info["Print Message"][0]) and max_line_len != len(info["Print Message"][1]) and len(player) % 2 == 0:
            info["Print Message"][0] = info["Print Message"][0].strip()
            max_line_len -= 1
        
        # set max line len for singe player terminal output
        if max_line_len > self.max_line_len_single_player:
            self.max_line_len_single_player = max_line_len
        
        # center non longest lines
        for i in range(len(info["Print Message"])):
            if max_line_len == len(info["Print Message"][i]): continue
            else:
                len_diff = max_line_len - len(info["Print Message"][i])
                num_ws = round(int(len_diff / 2))
                if len_diff % 2 == 0:
                    info["Print Message"][i] = " " * num_ws + info["Print Message"][i] + " " * num_ws
                else: 
                    info["Print Message"][i] = " " * (num_ws + 1) + info["Print Message"][i] + " " * num_ws 


    # logic for starting new round
    def game_setup(self):
        # give each player 1 card, 2 times
        for i in range(2):
            for info in self.bj_player_info.values():
                next_card = self.bj_card_stack.pop()
                info["Cards"].append(next_card)
        # reset line length output for single player games
        self.max_line_len_single_player = 0


        # perform all setup tasks for all players
        for player, info in self.bj_player_info.items():
            Blackjack.calculate_player_cards_score(self, player, info)
            Blackjack.special_setup_actions(self, player, info)
            Blackjack.create_player_print_message(self, player, info)
            Blackjack.center_player_card_info(self, player, info)


    # terminal output if 1 player
    def single_player_terminal_output(self):
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        terminal_output_message_list = []
        
        # add centered round number to top of terminal output
        round_add = f"Round: {self.bj_rounds_counter}"
        round_diff = self.max_line_len_single_player - len(round_add)
        num_ws = round(int(round_diff / 2))
        if round_diff % 2 == 0:
            terminal_output_message_list.append(" " * num_ws + round_add + " " * num_ws)
        else:
            terminal_output_message_list.append(" " * (num_ws + 1) + round_add + " " * num_ws)
        terminal_output_message_list.append("-" * (self.max_line_len_single_player + 1))
            
        # loop through players to center output
        # use max line len from center_player_card_info
        for player, info in self.bj_player_info.items():
            # if player info is longest append and continue 
            if len(info["Print Message"][0]) == self.max_line_len_single_player:
                for i in range(len(info["Print Message"])):
                    terminal_output_message_list.append(info["Print Message"][i])
            # else add propriate num of whitespaces
            else:
                line_diff = self.max_line_len_single_player - len(info["Print Message"][0])
                num_ws = round(int(line_diff / 2))
                if line_diff % 2 == 0:
                    for i in range(len(info["Print Message"])):
                        terminal_output_message_list.append(" " * num_ws + info["Print Message"][i] + " " * num_ws)
                else: 
                    for i in range(len(info["Print Message"])):
                        terminal_output_message_list.append(" " * (num_ws + 1) + info["Print Message"][i] + " " * num_ws)
            
            # add blank line after dealer 
            if player == "Dealer":
                terminal_output_message_list.append("-" * (self.max_line_len_single_player + 1))

        # turn list into single string and print
        print(terminal_message("\n".join(terminal_output_message_list)))

         
    # terminal output if 1 < players  
    def multi_player_terminal_output(self):
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        terminal_output_message_list = []
        
        # determine max message length
        max_message_length = 0
        for player in self.bj_player_info:
            if player == "Dealer": continue
            max_message_length += len(self.bj_player_info[player]["Print Message"][0])
        max_message_length += 3 * (len(self.bj_player_info) - 2) # 3 = player seperater length " | "
        
        # add centered round number to top of terminal output
        round_add = f"ROUND: {self.bj_rounds_counter}"
        round_diff = max_message_length - len(round_add)
        num_ws = round(int(round_diff / 2))
        if round_diff % 2 == 0:
            terminal_output_message_list.append(" " * num_ws + round_add + " " * num_ws)
        else:
            terminal_output_message_list.append(" " * (num_ws + 1) + round_add + " " * num_ws)
        terminal_output_message_list.append(" " * int((max_message_length + 1)/4) + "-" * int((max_message_length + 1)/2) + " " * int((max_message_length + 1)/4)) 
        
        # center dealer info 
        len_dealer_info = len(self.bj_player_info["Dealer"]["Print Message"][0])
        len_dealer_diff = max_message_length - len_dealer_info
        num_ws_dealer = round(int(len_dealer_diff / 2))
        # append dealer info to output message
        if len_dealer_diff % 2 == 0:
            for i in range(len(self.bj_player_info["Dealer"]["Print Message"])):
                terminal_output_message_list.append(" " * num_ws_dealer + self.bj_player_info["Dealer"]["Print Message"][i] + " " * num_ws_dealer)
        else: 
            for i in range(len(self.bj_player_info["Dealer"]["Print Message"])):
                terminal_output_message_list.append(" " * num_ws_dealer + self.bj_player_info["Dealer"]["Print Message"][i] + " " * (num_ws_dealer +1))
        
        # add player print messages together
        # start at 2 to skip dealer
        player_index = 2
        players_print_message = []
        for player in self.bj_player_info:
            if player == "Dealer": continue
            for i in range(len(self.bj_player_info[player]["Print Message"])):
                try:
                    players_print_message[i] += self.bj_player_info[player]["Print Message"][i]
                except:
                    players_print_message.append(self.bj_player_info[player]["Print Message"][i])
                if player_index < len(self.bj_player_info):
                    players_print_message[i] += " | "
            player_index += 1
        
        # add line between dealer and players
        terminal_output_message_list.append("-" * (max_message_length))
        
        # add player lines to message
        for i in players_print_message:
            terminal_output_message_list.append(i)
        
        # turn message list into sting and print
        print(terminal_message("\n".join(terminal_output_message_list)))

    
    # terminal output depending on player size        
    def game_terminal_output(self):
        # mostly ease of use for creating clean terminal output
        if len(self.bj_player_info) == 2:
            Blackjack.single_player_terminal_output(self)
        else: Blackjack.multi_player_terminal_output(self)


    # resolved dealer blackjack with appropriate messages and player returns of blackjack
    def dealer_blackjack(self):
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        Blackjack.game_terminal_output(self)
        if len(self.bj_player_info) == 2:
            player = self.bj_current_players[0]
            if self.bj_player_info[player]["Print Message"][6].strip() == "BLACKJACK!":
                message_output = "\nLuckily you also have blackjack! Your bet is returned."
            else:
                message_output = "\nUnfortunately you don't have blackjack.\nYour bet is collected."
        else:
            players_blackjack = []
            for player in self.bj_current_players:
                if self.bj_player_info[player]["Print Message"][6].strip() == "BLACKJACK!":
                    players_blackjack.append(player)
            if len(players_blackjack) == 0:
                message_output = "\nUnfortunately no other players have blackjack.\nAll bets are collected."
            elif len(players_blackjack) == 1:
                message_output = "\nLuckily " + players_blackjack[0] + " also has blackjack! Their bet is returned.\nAll other bets are collected."
            else:
                message_output = (f"\nLuckily {len(players_blackjack)} players also have blackjack!\n")
                for i, player in enumerate(players_blackjack):
                    message_output += player
                    if i + 1 < len(players_blackjack):
                        message_output += ", "
                message_output += " get their bets back!\n\nAll other bets are collected."
        
        x = input(terminal_message("The dealer has blackjack!\n" + message_output, True))
    
    
    # logic that resolves player blackjack
    def player_blackjack(self, player):
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        Blackjack.game_terminal_output(self)
        message_output = (f"Congratulations {player}! You've got BLACKJACK!")
        if len(self.bj_player_info) > 2:
            message_output += ("\nYou can sit back and relax!")
        x = input(terminal_message(message_output, True))
    
    
    # logic for player actions
    def player_actions(self, player, double_down = False):
        # if double_down set correct bet size and remove from balance
        if double_down:
            # check if player to double down is split player and compensate for balance variable
            if player.endswith("_split"):
                split_player = player.split("_split")
                current_player = split_player[0]
            else:
                current_player = player
            
            # Remove balance from correct player
            self.bj_player_info[current_player]["Balance"] -= self.bj_player_info[player]["Current Bet"]
            self.bj_player_info[player]["Current Bet"] += self.bj_player_info[player]["Current Bet"]
            self.bj_player_info[player]["Print Message"][7] = "Bet: $" + str(self.bj_player_info[player]["Current Bet"])
        
        # take card from stack & add to player
        next_card = self.bj_card_stack.pop()
        self.bj_player_info[player]["Cards"].append(next_card)

        # calculate score, create message, center info
        Blackjack.calculate_player_cards_score(self, player, self.bj_player_info[player], double_down)
        Blackjack.create_player_print_message(self, player, self.bj_player_info[player], double_down)
        Blackjack.center_player_card_info(self, player, self.bj_player_info[player])

        # print to terminal
        Blackjack.game_terminal_output(self)


    # game logic for splitting pairs
    def player_action_split_pair(self, player):
        # reset player info
        self.bj_player_info[player]["Split Pair"] = False
        self.bj_player_info[player]["Double Down"] = False
        
        # create list with split player 
        split_pair_player_list = [player, player + "_split"]
        # create new split player in player_info dict
        self.bj_player_info[split_pair_player_list[1]] = {
                "Cards": [], 
                "Card Score": 0,
                "Current Bet": 0, 
                "Print Message": [],
                "Split Pair": False, 
                "Double Down": False
                }
        
        # set correct print message
        self.bj_player_info[split_pair_player_list[1]]["Print Message"] = [split_pair_player_list[1], "", "", "", "" ,"", ""]
        # add whitespace for correct terminal output
        for player_split in split_pair_player_list:
            if len(player_split) % 2 == 0:
                self.bj_player_info[player_split]["Print Message"][0] = " " + self.bj_player_info[player_split]["Print Message"][0]
             
        # give split_player one of players cards
        donated_card = self.bj_player_info[player]["Cards"].pop()
        self.bj_player_info[split_pair_player_list[1]]["Cards"].append(donated_card)
        
        # set correct bet for split_player and remove from player
        self.bj_player_info[split_pair_player_list[1]]["Current Bet"] = self.bj_player_info[player]["Current Bet"]
        self.bj_player_info[player]["Balance"] -= self.bj_player_info[player]["Current Bet"]
        self.bj_player_info[split_pair_player_list[1]]["Print Message"].append("Bet: $" + str(self.bj_player_info[split_pair_player_list[1]]["Current Bet"]))

        # give both new card
        for split_player in split_pair_player_list:
            next_card = self.bj_card_stack.pop()
            self.bj_player_info[split_player]["Cards"].append(next_card)
        
        # create restructured dictionary where player and player_split are next to eachother
        restructure_dict ={}
        for split_player, info in self.bj_player_info.items():
            if split_player in restructure_dict:
                continue
            if split_player in split_pair_player_list:
                for i in split_pair_player_list:
                    restructure_dict[i] = self.bj_player_info[i]
            else:
                restructure_dict[split_player] = info
        
        # set player_info as restructured dict
        self.bj_player_info = restructure_dict
        
        # check if split pair == aces
        double_aces = False
        if self.bj_player_info[player]["Cards"][0].startswith("Ace"):
            double_aces = True
            self.bj_player_info[player]["Cards"][0] = self.bj_player_info[player]["Cards"][0][:-2]
        
        # reset player info
        for split_player in split_pair_player_list:
            Blackjack.calculate_player_cards_score(self, split_player, self.bj_player_info[split_player], split_pair=True)
            Blackjack.special_setup_actions(self, split_player, self.bj_player_info[split_player])
            Blackjack.create_player_print_message(self, split_player, self.bj_player_info[split_player])
            Blackjack.center_player_card_info(self, split_player, self.bj_player_info[split_player])

        # if split pair was aces if so stop
        if double_aces:
            x = input(terminal_message("You've split your pair of aces!\nYou'll get 2 more cards!", True))
            Blackjack.game_terminal_output(self)
            x = input(terminal_message("Let's hope that what you've got is enough!", True))
            return
        # player turn if pair was not aces
        else:
            for i, split_player in enumerate(split_pair_player_list):
                Blackjack.player_turn(self, split_player, split_pair = True)
                
    
    # logic for running a player turn
    def player_turn(self, player, split_pair=False):
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        Blackjack.game_terminal_output(self)
        # intoduces player for their first turn
        message_output = (f"It's your turn {player}!\n")
        player_turn_count = 0
        
        # ask for player input with double down and split pair as options
        while True:
            # stops player anouncement after first turn
            if player_turn_count > 0:
                message_output = ""
            
            # check if player is busted and return
            if self.bj_player_info[player]["Print Message"][6].strip() == "Busted!":
                x = input(terminal_message("Your score is over 21!\nUnfortunatly you're bust, your bet is collected.", True))
                self.bust_players += 1
                return
            
            # options always available
            message_output += "What would you like to do?"
            message_output += "\n1. Hit\n2. Stand"
            
            # set balance variable for ease of use
            if player.endswith("_split"):
                split_player = player.split("_split")
                enough_balance = self.bj_player_info[split_player[0]]["Balance"] >= self.bj_player_info[player]["Current Bet"]
            else:
                enough_balance = self.bj_player_info[player]["Balance"] >= self.bj_player_info[player]["Current Bet"]
            
            # game logic for aditional options for first turn menu
            if player_turn_count == 0:
                if self.bj_player_info[player]["Double Down"] and enough_balance:
                    message_output += "\n3. Double Down"  
                    if self.bj_player_info[player]["Split Pair"] and split_pair == False and enough_balance:
                        message_output += "\n4. Split Pair"  
                elif self.bj_player_info[player]["Split Pair"] and split_pair == False and enough_balance:
                    message_output += "\n3. Split Pair"

            # ask for player input
            ui_player_turn = input(terminal_message(message_output, True))

            # Check for non int values
            try:
                ui_player_turn_int = int(ui_player_turn)
            except:
                x = input("Error: Invalid Input!")
                message_output = ""
                continue
            
            # if player can split pair but not double down (input == 3) and chooses this. 1 is added to input for next if/elif/else block
            if self.bj_player_info[player]["Double Down"] == False and self.bj_player_info[player]["Split Pair"] and ui_player_turn_int == 3 and enough_balance:
                ui_player_turn_int += 1

            # select correct player action
            if ui_player_turn_int == 1: # hit
                Blackjack.player_actions(self, player)
            elif ui_player_turn_int == 2: # stand
                card_score = self.bj_player_info[player]["Card Score"]
                x = input(terminal_message(f"You stand with a card score of {card_score}.\nLet's see if it is enough!", True))
                return
            elif ui_player_turn_int == 3 and self.bj_player_info[player]["Double Down"] and player_turn_count == 0 and enough_balance: # double down
                Blackjack.player_actions(self, player, double_down = True)
                x = input(terminal_message(f"Let's hope that your hidden card is the card you need!", True))
                return
            elif ui_player_turn_int == 4 and self.bj_player_info[player]["Split Pair"] and player_turn_count == 0 and split_pair == False and enough_balance: # split pair
                Blackjack.player_action_split_pair(self, player)
                return
            else:
                x = input("Error: Invalid Input!")
                message_output = ""
            
            player_turn_count += 1

    
    # logic for dealer turn
    def dealer_turn(self, skip_dealer=False):
        # set dealer turn to true
        self.bj_player_info["Dealer"]["Turn"] = True
        
        # skips dealer ouput if only 1 player and has blackjack
        if skip_dealer:
            return
        
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        Blackjack.game_terminal_output(self)
        x = input(terminal_message("It's the dealers Turn\nLets see their hole card!", True))
        
        #remove no blackjack! line if present
        if len(self.bj_player_info["Dealer"]["Print Message"]) == 8:
            del self.bj_player_info["Dealer"]["Print Message"][7]
        
        # determine dealer info
        Blackjack.calculate_player_cards_score(self, "Dealer", self.bj_player_info["Dealer"])
        Blackjack.create_player_print_message(self, "Dealer", self.bj_player_info["Dealer"])
        Blackjack.center_player_card_info(self, "Dealer", self.bj_player_info["Dealer"])
        
        
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        Blackjack.game_terminal_output(self)
        
        # logic for dealer turn and results
        # loops and prints while dealer score < 17
        cards_drawn = 0
        while self.bj_player_info["Dealer"]["Card Score"] < 17 and self.bj_player_info["Dealer"]["Card Score"] != "Busted!":
            if cards_drawn == 0:
                x = input(terminal_message("The dealer draws a card.", True))
                cards_drawn += 1
            else:
                x = input(terminal_message("The dealer draws another card.", True))
            next_card = self.bj_card_stack.pop()
            self.bj_player_info["Dealer"]["Cards"].append(next_card)
            Blackjack.calculate_player_cards_score(self, "Dealer", self.bj_player_info["Dealer"])
            Blackjack.create_player_print_message(self, "Dealer", self.bj_player_info["Dealer"])
            Blackjack.center_player_card_info(self, "Dealer", self.bj_player_info["Dealer"])
            Blackjack.game_terminal_output(self)
        if self.bj_player_info["Dealer"]["Card Score"] < 22:
            score = self.bj_player_info["Dealer"]["Card Score"]
            x = input(terminal_message(f"The dealers got a score of {score}!\nLet's see the results!", True))
        else:
            x = input(terminal_message(f"The dealers got BUSTED!!!\nLet's see the results!", True))
    
    
    # reveal double down card and info for required players
    def result_double_down(self):
        for player, info in self.bj_player_info.items():
            if player == "Dealer": continue
            elif info["Print Message"][6].strip().endswith(" + ?"):
                os.system("cls" if os.name == "nt" else "clear")        # clear terminal
                Blackjack.game_terminal_output(self)
                
                # select correct response for single/multiplayer
                if len(self.bj_player_info) == 2:
                    x = input(terminal_message(f"Let's see your hidden card!", True))
                else:
                    x = input(terminal_message(f"You still have a hidden card {player}.\nLet's see your final score!", True))
                
                # determine player output
                Blackjack.calculate_player_cards_score(self, player, info)
                Blackjack.create_player_print_message(self, player, info)
                Blackjack.center_player_card_info(self, player, info)
                
                # print player output
                os.system("cls" if os.name == "nt" else "clear")        # clear terminal
                Blackjack.game_terminal_output(self)
    
    
    # create round summary message
    def round_summary_message(self):
        # show resulting double down cards
        Blackjack.result_double_down(self) 
        
        # show round number
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        Blackjack.game_terminal_output(self)
        print(terminal_message(f"Results of round {self.bj_rounds_counter}."))
        
        # setup summary message
        # 0 = name, 1 = bet, 2 = blank, 3 = Win/lose/etc., 4 = blank, 5 = win/lost amount, 6 = new balance
        summary_message = ["", "", "", "", "", "", ""]
        
        # index for adding " | ", starts at 2 because skipped "Dealer"
        player_index = 2
        # loop through players to add to summary message and resolve winnings if any
        for player, info in self.bj_player_info.items():
            # Skip dealer
            if player == "Dealer": continue
            
            # increase current round count
            if not player.endswith("_split"):
                info["Current Round"] += 1
            
            # setup summary message
            summary_message_player = ["", "", "", "", "", "", ""]
            summary_message_player[0] += player
            summary_message_player[1] += "Bet: $" +str(info["Current Bet"])
            
            # if dealer blackjack
            if self.bj_player_info["Dealer"]["Print Message"][6].strip() == "BLACKJACK!":
                if info["Card Score"] == 21:
                    summary_message_player[3] += "PUSH"
                    bj_win_lost_amount = info["Current Bet"]
                else:
                    summary_message_player[3] += "LOSE"
                    bj_win_lost_amount = -1 * info["Current Bet"]
            # if player blackjack
            elif info["Print Message"][6].strip() == "BLACKJACK!":
                summary_message_player[3] += "BLACKJACK!"
                bj_win_lost_amount = int(info["Current Bet"] * 2.5)
            # if player wins (dealer == bust OR dealer != bust < player score)
            elif ((self.bj_player_info["Dealer"]["Card Score"] > 21 and info["Card Score"] <= 21) or 
                  (info["Card Score"] <= 21 and self.bj_player_info["Dealer"]["Card Score"] < info["Card Score"])):
                summary_message_player[3] += "WIN"
                bj_win_lost_amount = info["Current Bet"] * 2
            # if player == dealer
            elif info["Card Score"] <= 21 and self.bj_player_info["Dealer"]["Card Score"] == info["Card Score"]:
                summary_message_player[3] += "PUSH"
                bj_win_lost_amount = info["Current Bet"]
            # if player lose
            else:
                summary_message_player[3] += "LOSE"
                bj_win_lost_amount = -1 * info["Current Bet"]
            
            # add winnings to message and balance
            split_player_origin = player.split("_split")
            if bj_win_lost_amount >= 0:
                if summary_message_player[3] == "PUSH":
                    summary_message_player[5] += "Push: $" + str(bj_win_lost_amount)
                else:
                    summary_message_player[5] += "Won: $" + str(bj_win_lost_amount)
                if player.endswith("_split"):
                    self.bj_player_info[split_player_origin[0]]["Balance"] += bj_win_lost_amount
                else:
                    info["Balance"] += bj_win_lost_amount
            else:
                summary_message_player[5] += "Lost: $" + str(-1 * bj_win_lost_amount)
            
            # add balance to message
            if (player + "_split") in self.bj_player_info:
                summary_message_player[6] += "------"
            elif split_player_origin[0] != "" and split_player_origin[0] in self.bj_player_info:
                summary_message_player[6] += "Balance: $" + str(self.bj_player_info[split_player_origin[0]]["Balance"])
            else:
                summary_message_player[6] += "Balance: $" + str(info["Balance"])
            
            # code block to center summary message per player
            # determine max line length
            max_line_len = 0
            for i in range(len(summary_message_player)):
                if max_line_len < len(summary_message_player[i]):
                    max_line_len = len(summary_message_player[i])
            
            # center non longest lines
            for i in range(len(summary_message_player)):
                if max_line_len == len(summary_message_player[i]):
                    summary_message[i] += summary_message_player[i]
                elif i == 2 or i == 4:
                    summary_message[i] += "-" * max_line_len
                else:
                    len_diff = max_line_len - len(summary_message_player[i])
                    num_ws = round(int(len_diff / 2))
                    if len_diff % 2 == 0:
                        summary_message[i] += " " * num_ws + summary_message_player[i] + " " * num_ws
                    else: 
                        summary_message[i] += " " * (num_ws + 1) + summary_message_player[i] + " " * num_ws
                if player_index < len(self.bj_player_info):
                        summary_message[i] += " | "
        
        x = input(terminal_message("\n".join(summary_message), True)) 
            
    
    # update highscore
    def remove_player_and_update(self, player):
        os.system("cls" if os.name == "nt" else "clear")          # clear terminal
        
        # set highest round
        if self.bj_player_info[player]["Highest Round"] < self.bj_player_info[player]["Current Round"]:
            self.bj_player_info[player]["Highest Round"] = self.bj_player_info[player]["Current Round"]
        
        # open player highscore file
        with open("player_highscores.json", "r") as file:
            player_highscores = json.load(file)
        
        outro_message = f"Thanks for playing {player}"
        # skip if no new highscores
        if self.bj_player_info[player]["Balance"] <= player_highscores[player]["Highscore"] and self.bj_player_info[player]["Highest Round"] <= player_highscores[player]["Max Rounds"]:
            outro_message += "!\n\nSee you next time!"
            x = input(terminal_message(outro_message))
        else:
            outro_message += ", and congratulations! You've got a new record!!!"
            print(terminal_message(outro_message))
            outro_message = ""
            # new highscore
            if self.bj_player_info[player]["Balance"] > player_highscores[player]["Highscore"]:
                prev_hs = player_highscores[player]["Highscore"]
                new_hs = self.bj_player_info[player]["Balance"]
                # add to outro message
                outro_message += f"Your previous highscore was ${prev_hs}.\nBut this time you made ${new_hs}!!!"
                #update player highscore
                player_highscores[player]["Highscore"] = new_hs
                # add aditional line to message if both records broken
                if self.bj_player_info[player]["Highest Round"] > player_highscores[player]["Max Rounds"]:
                    outro_message += "\n\nAnd not only that!\n\n" 
            # new max round
            if self.bj_player_info[player]["Highest Round"] > player_highscores[player]["Max Rounds"]:
                prev_mr = player_highscores[player]["Max Rounds"]
                new_mr = self.bj_player_info[player]["Highest Round"]
                outro_message += f"Your previous rounds record was {prev_mr} rounds.\nBut this time you played {new_mr} rounds!!!"
                player_highscores[player]["Max Rounds"] = new_mr
            print(terminal_message(outro_message))
            x = input(terminal_message("Your new scores will be saved.\nGood luck beating them next time!", True))
        
        # remove players that quit
        self.bj_player_info.pop(player)
        self.bj_current_players.remove(player)
        
        # save new highscores
        with open("player_highscores.json", "w") as file:
            json.dump(player_highscores, file, indent=4)
    
            
    # menu for actions after each round        
    def final_menu(self):
        # create message + store broke players
        final_menu_message_summary = ""
        broke_players = []
        player_index_message = 1
        for player, info in self.bj_player_info.items():
            if player == "Dealer" or player.endswith("_split"): 
                player_index_message += 1
                continue
            balance = info["Balance"]
            final_menu_message_summary += (f"{player}\nBalance: ${balance}")
            if info["Balance"] < 10:
                broke_players.append(player)
            if player_index_message <  len(self.bj_player_info):
                final_menu_message_summary += "\n\n"
            player_index_message += 1
                
        
        # setup while loop for possible wrong input
        player_index = 0
        while player_index < len(self.bj_current_players):
            os.system("cls" if os.name == "nt" else "clear")          # clear terminal
            print(terminal_message("Current player balances:"))
            print(terminal_message(final_menu_message_summary))
            player = self.bj_current_players[player_index]
            
            # catch non int input
            ui_continue = input(terminal_message(f"{player}, do you want to continue?\n1. Yes\n2. No", True))
            try:
                ui_continue_int = int(ui_continue)
            except:
                x = input("Error: Invalid Input!")
                continue
            
            # code block for resolving input    
            if ui_continue_int == 1:
                # if player["balance"] = 0
                if player in broke_players:
                    print(terminal_message("Unfortunately, you don't have enough money to keep playing!\nBut you can try again!\n\nYour balance and round counter will be reset."))
                    if self.bj_player_info[player]["Highest Round"] < self.bj_player_info[player]["Current Round"]:
                        self.bj_player_info[player]["Highest Round"] = self.bj_player_info[player]["Current Round"]
                    self.bj_player_info[player]["Balance"] = 100
                    self.bj_player_info[player]["Current Round"] = 0
                player_index += 1
            elif ui_continue_int == 2:
                Blackjack.remove_player_and_update(self, player)
            else:
                x = input("Error: Invalid Input!")
                continue
        
        Blackjack.clear_players_info(self) 

    
    # game loop logic
    def main_gameplay_loop(self):
        # round setup
        Blackjack.betting(self)
        Blackjack.game_setup(self)
        Blackjack.game_terminal_output(self)
        
        # wait till user continues
        x = input("Press Enter to Continue\n")
        
        # Check dealer blackjack
        if self.bj_player_info["Dealer"]["Print Message"][6].strip() == "BLACKJACK!":
            Blackjack.dealer_blackjack(self)
        else:
            # loop through players while turn active
            player_index = 0
            while player_index < len(self.bj_current_players):
                player = self.bj_current_players[player_index]
                if self.bj_player_info[player]["Print Message"][6].strip() == "BLACKJACK!":
                    Blackjack.player_blackjack(self, player)
                else:
                    Blackjack.player_turn(self, player)
                player_index += 1
            # Skip unnecessary terminal output if only 1 player and has blackjack 
            if (len(self.bj_player_info) == 2 and self.bj_player_info[self.bj_current_players[0]]["Print Message"][6] == "BLACKJACK!") or self.bust_players == len(self.bj_current_players):
                Blackjack.dealer_turn(self, skip_dealer=True)
            else:
                Blackjack.dealer_turn(self)
                
        # summary of the round and choice menu
        Blackjack.round_summary_message(self)
        Blackjack.final_menu(self)
        
        # update round counter
        self.bj_rounds_counter += 1
        
        # if game continues long enough for minimum card stack to be reached card deck is remade
        if len(self.bj_card_stack) < self.bj_minimum_card_stack_size:
            Blackjack.create_card_stack(self) # create new card stack
            self.bj_minimum_card_stack_size = random.randint(60, 80) # reset random int
            
            # reshuffle terminal output
            os.system("cls" if os.name == "nt" else "clear")
            print(terminal_message("The dealer has drawn the spacer card.\nThe card stack must be reshuffeled."))
            time.sleep(1)
            for i in range(4):
                print(terminal_message("The dealer shuffels cards."))
                time.sleep(1)
            x = input(terminal_message("The cards are shuffeled and the dealer adds a spacer card somewhere around the top 70 cards.\nPress enter to continue."))

        # if no active players, return to main menu
        if len(self.bj_player_info) == 1:
            return False 
        else: 
            x = input(terminal_message("Let's go again!", True))
            return True   
