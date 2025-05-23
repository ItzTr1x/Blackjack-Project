from classes.GUI import GUI
import tkinter as tk
from classes.GameData import GameData


class Hand:
    def __init__(self, window, is_dealer):
        self.cards = []
        self.window = window
        self.is_dealer = is_dealer
        if self.is_dealer:
            self.window.addText("cards_frame", "Dealer's Cards:", row=3, col=0, width=5)
            self.drow = 4
        else:
            self.window.addText("cards_frame", "Player's Cards:", row=0, col=0, width=5)
            self.drow = 1

    def add(self, card, is_visible):
        self.cards.append(card)
        self.calculate()
        return self.display(is_visible)

    def display(self, is_visible=False):
        if self.is_dealer and not is_visible:
            return self.show_back(self.cards[-1], len(self.cards) - 1)
        else:
            return self.show_face(self.cards[-1], len(self.cards) - 1)

    def show_back(self, card, index):
        return self.window.addImage(
            "cards_frame", card.back, 47, 72, caption="**", row=self.drow, col=index
        )

    def show_face(self, card, index):
        return self.window.addImage(
            "cards_frame",
            card.face,
            47,
            72,
            caption=card.name,
            row=self.drow,
            col=index,
        )

    def calculate(self):
        self.value = 0

        for card in self.cards:
            self.value += card.value

        flag = True
        while self.value > 21 and flag:
            flag = False
            for card in self.cards:
                if card.value == 11:
                    flag = True
                    card.value = 1
                    break
