import csv

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

# RULES:
# Get as close to 21 without going over
# 6 standard 52 decks are shuffled together 312 cards total
# cards are dealt from the bottom
# when ~60/75 cards remain in the stack the cards are shuffled
# Card values ace = 1/11, face cards = 10, other cards is pip

# The game:
# SETUP
# Dealer gives players and themself 1 face up
# Dealer gives players face up, dealer face down
# if first two cards == 21 BLACKJACK. player get 1.5x bet
# if dealer == 21 collect al bets

# THE PLAY
# players decide to "stand" == not ask for another card
#                   "hit"   == ask for another card
# After the players are finished dealer turns face down card over
# if total >= 17 dealer must "stand", else must "hit"
# if total includes an ace but is 21 >= x >= 17 must stand

# SPLITTING PAIRS
# if players first 2 cards are the same they can be split
# same bat must be made again for the second stack
# if double aces, 1 more card is allowed and no hitting
# if this results in BJ the payout is 2x not 1,5x

# DOUBLING DOWN
# if orignial 2 cards == 9/10/11 players can double their bet
# they will receive 1 card face down that will be turned when betting is finished


class Card_shuffle():
    pass

class Blackjack():
    pass

class Player():
    pass