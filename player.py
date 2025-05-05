import json

#player class with methods
class Player():
    def __init__(self, name, player_highscores):
        basic_scores = {"Highscore": 0, "Max Rounds": 0}
        player_highscores[name] = basic_scores
        #return player_highscores
    
    def welcome_message(name):
        print(f"Welcome back {name}")
        
    def highscore(name):
        pass
    
    def update_highscores(player_highscores):
        # update player_highscore file with new players
        with open("player_highscores.json", "w") as file:
            json.dump(player_highscores, file, indent=4)