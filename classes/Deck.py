import random
from classes.Card import Card


class Deck:

    # Generate and shuffle the deck
    def __init__(self):
        self.deck = []
        suits = ["H", "D", "C", "S"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "X", "J", "Q", "K", "A"]
        for suit in suits:
            for rank in ranks:
                name = suit + rank
                card = Card(
                    name=name, face="assets/" + name + ".gif", back="assets/B1.gif"
                )
                self.deck.append(card)
        random.shuffle(self.deck)
        return

    # Add a card to the player or dealer's hand
    def pop_deck(self):
        return self.deck.pop()
