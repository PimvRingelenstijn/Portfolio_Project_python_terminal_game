import csv

# create empty dictionary to read into
card_deck = {}

# open card info file and turn it into usable dictionary
with open('card_information.csv') as card_info_file:
    reader = csv.reader(card_info_file)
    next(reader) #skip header
    for row in reader:
        card, value = row #card = row[0], value = row[1]
        card_values[card] = int(value)  

print(card_deck)
