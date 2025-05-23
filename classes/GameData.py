import json


class GameData:
    FILENAME = "game_data.json"
    stats = {"wins": 0, "losses": 0}

    def __init__(self):
        self.load()

    # Load game data from a JSON file
    def load(self):
        try:
            with open(self.FILENAME, "r") as file:
                json_data = json.load(file)
                self.stats = json_data
                return
        except FileNotFoundError:
            # If the file doesn't exist, initialize default stats
            return {"wins": 0, "losses": 0}

    # Save game data to a JSON file
    def save(self):
        with open(self.FILENAME, "w") as file:
            json.dump(self.stats, file)

    def increment(self, datapoint):
        self.stats[datapoint] = self.stats[datapoint] + 1

    # Reset game stats
    def reset(self):
        self.stats["wins"] = 0
        self.stats["losses"] = 0
        self.save()

    def display(self):
        return self.stats
