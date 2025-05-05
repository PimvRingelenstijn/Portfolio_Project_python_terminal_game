import json
import time
import os
from terminal_message import terminal_message
from blackjack import Blackjack
from player import Player

if os.path.exists("player_highscores.json"):
    # load in player highscores if any are present
    with open("player_highscores.json", "r") as file:
        player_highscores = json.load(file)
    # if there is no score file make first dict
else:
    player_highscores = {}

# Startup notification 
os.system("cls" if os.name == "nt" else "clear")
print(terminal_message("Welcome to a game of Blackjack!"))
time.sleep(1.5)

# While loop will repeat until user inputs 4 in menu
# ui_* is short for user_input_*
while True:
    # clears terminal output
    os.system("cls" if os.name == "nt" else "clear")
    # User choice
    ui_menu = input(terminal_message("What would you like to do?\n\n1. Play Blackjack\n2. View Rules\n3. View Highscores\n4. Quit Game", True))
    
    # catch non int inputs
    try:
        ui_menu_int = int(ui_menu)
    except:
        x = input("Error: Invalid Input!")
        continue
    time.sleep(0.5)

    # If/else block after user input!
    if ui_menu_int == 1: #Play Blackjack
        # create while loop to return to if invalid input
        # create player list
        current_players = []
        game_setup_menu = True
        
        #while input for game type selection and player count
        while game_setup_menu:
            os.system("cls" if os.name == "nt" else "clear")        # clear terminal
            
            # ask amount of players input
            ui_amount_of_players = input(terminal_message("How many players are there?\n(Max 6)", True))
            
            # Check for int input
            try:
                ui_amount_of_players_int = int(ui_amount_of_players)
            except:
                x = input("Error: Invalid Input!")
                continue
            time.sleep(0.5)
            
            # lel, had to be done
            if ui_amount_of_players_int == 69:
                for i in range(10): 
                    print(terminal_message("nice"))
                    time.sleep(0.3)
                    continue
            if ui_amount_of_players_int > 6:
                x = input("Error: Too many players")
                continue

            # Add 1 single player
            if ui_amount_of_players_int == 1:
                player_name = input(terminal_message("Welcome player! What is your name?", True))
                if player_name in player_highscores: 
                    Player.welcome_message(player_name)
                else: Player(player_name, player_highscores)
                current_players.append(player_name)            
            # add multiple players
            elif ui_amount_of_players_int > 1:
                for player_num in range(1, ui_amount_of_players_int + 1):
                    player_name = input(terminal_message("Welcome player {num}! What is your name?".format(num = player_num), True))
                    if player_name in player_highscores: 
                        Player.welcome_message(player_name)
                    else: Player(player_name, player_highscores)
                    current_players.append(player_name)
                    time.sleep(0.5)
            # check for negative players
            else:
                x = input("Error: Invalid Input!")
                continue
            
            # stops game setup menu while loop
            game_setup_menu = False
        
        Player.update_highscores(player_highscores)
        
        # this will be the real gameplay loop!
        main_gameplay_loop_outside = True
        main_game = Blackjack(current_players)
        while main_gameplay_loop_outside:
            main_gameplay_loop_outside = main_game.main_gameplay_loop()
            
        x = input(terminal_message("Thnx for playing!"))    

        
    elif ui_menu_int == 2: # View Rules
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        x = input(terminal_message("""---The Rules Of Blackjack---\n\n--Goal--\nGet a card score as close to 21 as possible.\nIf you go over 21, you bust and lose the round.
\n--Card Values--\nNumber cards (2-10) = face value (10 = T)\nFace cards (J, Q, K) = 10 points\nAce (A) = 1 or 11 points (whichever is best)
\n--Basic Round Structure--\n1. Betting\n    Each player sets a bet between $10 - $500\n2. Round Setup\n    Each player is dealt two cards face up\n    The dealer is dealt two cards, one face up and one face down (hole card)
3. Player(s) turn\n    Each player can take one of 4 possible actions:\n    - Hit: Take another card\n    - Stand: Keep your current hand\n    If a players card score after setup is 9/10/11
    - Double Down: Double your bet and take only 1 more card face down\n    If both cards of a player are of the same value\n    - Split Pair: Split the card pair and place an equal bet on the second set.
      Both sets play individually for the current round.\n      If the split pair is aces, both sets take only 1 more card.\n4. Dealer Turn\n    After all player finish the dealer reveals their hole card
    Dealer must hit until their card score is 17 or higher, after which the dealer stands\n    If dealer busts, all remaining players win\n
--Round Ending--\nPlayer wins if:\n    Player gets blackjack (card score of first 2 cards equals 21) and dealer does not\n    Players card score is greater than dealers without going over 21
    Dealer busts and player does not\nPlayer ties (push):\n     Player score is equal to dealers score\n
--Resolve Betting--\nPlayer Blackjack: 3:2 ($10 bet = $25 return)\nPlayer Win: 1:1 ($10 bet = $20 return)\nPlayer Push: 1:0 ($10 bet = $10 return)\nPlayer Los: 0:0 ($10 bet = $0 return)
\nPress Enter To Return To Main Menu""", True))
        
        
    elif ui_menu_int == 3: # View Highscores
        
        
        player_max_score = {} 
        player_max_round = {}
        
        if len(player_highscores) == 0:
            print(terminal_message("Winning only matters while you are ahead.\nYour highest score will be the highest score you quit playing with, not the highest score you reach during a game!"))
            x = input(terminal_message("There are currently no highscores recorded!\nPlay some rounds and return later!", True))
            continue
        
        for player, info in player_highscores.items():
            player_max_score[player] = info["Highscore"]
            player_max_round[player] = info["Max Rounds"]
        
        sorted_max_score = dict(sorted(player_max_score.items(), key=lambda item: item[1], reverse=True))
        sorted_max_round = dict(sorted(player_max_round.items(), key=lambda item: item[1], reverse=True))
        
        highscore_message = "These are the current Highscores:\n\n"
        # highest score
        if len(sorted_max_score) < 10:
            set_sorted_max_score = {k: sorted_max_score[k] for k in list(sorted_max_score)[:len(sorted_max_score)]}
        else:
            set_sorted_max_score = {k: sorted_max_score[k] for k in list(sorted_max_score)[:10]}
        highscore_message += "Highest Score:\n"
        num = 1
        for player, info in set_sorted_max_score.items():
            highscore_message += f"-{num}- {player}: ${info}\n"
            num += 1
        
        # max round
        if len(sorted_max_round) < 10:
            set_sorted_max_round = {k: sorted_max_round[k] for k in list(sorted_max_round)[:len(sorted_max_round)]}
        else:
            set_sorted_max_round = {k: sorted_max_round[k] for k in list(sorted_max_round)[:10]}
        highscore_message += "\nHighest Round:\n"
        num = 1
        for player, info in set_sorted_max_round.items():
            highscore_message += f"-{num}- {player}: Round {info}\n"
            num += 1
        
        highscores_menu = True
        while highscores_menu:
            os.system("cls" if os.name == "nt" else "clear")
            print(terminal_message("Winning only matters while you are ahead.\nYour highscore will be the highest score you quit playing with,\nnot the highest score you reach during a game!"))# clear terminal
            print(terminal_message(highscore_message))
            ui_highscore = input(terminal_message("Is there any specific player highscore you want to look up?\n\nEnter player name for player highscore\nPress Enter to return to main menu",True))
            if ui_highscore == "":
                highscores_menu = False
            elif ui_highscore in player_highscores:
                player = ui_highscore
                highscore = player_highscores[player]["Highscore"]
                rounds = player_highscores[player]["Max Rounds"]
                x = input(terminal_message(f"The highscores of {player} are:\nHighest Score: ${highscore}\nHighest Round: {rounds}"))
            else:
                x = input(terminal_message(f"Error: Player = {ui_highscore} = not found!\nPlease try again!"))

    elif ui_menu_int == 4: # Quit Game
        os.system("cls" if os.name == "nt" else "clear")        # clear terminal
        print(terminal_message("Thanks for playing!"))
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
        break#exit while loop
    
        
    else: # Invalid input returns to start main menu while loop
        x = input("Error: Invalid Input!")


